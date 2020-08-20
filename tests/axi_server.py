import os
import cocotb
from cocotb.result import TestFailure
from cocotb.result import TestSuccess
from cocotb.clock import Clock
from cocotb.triggers import Timer
from cocotb.drivers.amba import AXI4LiteMaster
from cocotb.drivers.amba import AXIProtocolError

import zmq
import struct

CLK_PERIOD_NS = 10
POLL_PERIOD_NS = 1000

MODULE_PATH = os.path.join(os.path.dirname(__file__), os.pardir, "hdl")
MODULE_PATH = os.path.abspath(MODULE_PATH)


def setup_dut(dut):
    '''Anything needed before accessing the AXI slave (dut)'''
    cocotb.fork(Clock(dut.clk, CLK_PERIOD_NS, units='ns').start())


@cocotb.test()
async def axi_server(dut):
    '''
    Runs a cocotb "test" that listens on a zeromq socket for read/write commands
    and forwards these to an AXI Lite slave (dut)
    '''

    # Reset the simulated AXI slave and attach to a cocotb AXI master interface
    dut.rst <= 1
    dut.test_id <= 0
    axim = AXI4LiteMaster(dut, "AXIML", dut.clk)
    setup_dut(dut)
    await Timer(CLK_PERIOD_NS * 10, units='ns')
    dut.rst <= 0

    # Setup zeromq socket
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind('tcp://*:7777')

    while True: # Serve until client requests termination or ctrl+c
        try:
            msg = socket.recv(flags=zmq.NOBLOCK)
            cmd,addr,data = struct.unpack('III',msg)
            if cmd == 0:
                data = await axim.read(addr)
                reply = struct.pack('III',cmd,addr,data)
                socket.send(reply)
            elif cmd == 1:
                await axim.write(addr,data)
                reply = struct.pack('III',cmd,addr,data)
                socket.send(reply)
            elif cmd == 2:    
                reply = struct.pack('III',cmd,addr,data)
                socket.send(reply)
                dut._log.info('axi_server exiting gracefully')
                return
            else:
                raise TestFailure('Unknown axi_server command %i'%cmd)
        except zmq.Again as e:
            pass #no cmd
        await Timer(POLL_PERIOD_NS, units='ns')
