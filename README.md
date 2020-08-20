# AXI Server Demo

A cocotb test based on the AXI Lite Demo in cocotb that runs a simple ZMQ server
so that software running on the host can connect to the cocotb test and perform
register reads and writes in real (simulated) time.


## Overview

* ``hdl`` contains files copied from the cocotb AXI Lite Demo that model a 
simple AXI slave device. See [the source](https://github.com/cocotb/cocotb/tree/master/examples/axi_lite_slave).

* ``tests`` contains the cocotb test that implements the ZMQ AXI server logic.

* ``sw`` contains an example C++ program that connects to the cocotb simulation
to perform register reads and writes.

## Usage

1. With cocotb setup, run the `Makefile` in `tests` to start the ZMQ AXI server.
This will look like a normal cocotb test, but will not exit.

2. Build and run the `example_sw` from `sw`. This will connect to the cocotb
test and write one of the registers with the cocotb AXI master, then instruct
cocotb to exit.
