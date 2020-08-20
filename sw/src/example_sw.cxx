#include <zmq.hpp>

#define READ 0
#define WRITE 1
#define DONE 2

typedef struct {
    unsigned int cmd, addr, data;
} msg;

unsigned int zmq_axi(zmq::socket_t &socket, unsigned int cmd, unsigned int addr = 0, unsigned int data = 0) {
    zmq::message_t zm(sizeof(msg));
    msg *m = (msg*)zm.data();
    m->cmd = cmd;
    m->addr = addr;
    m->data = data;
  
    socket.send(zm,0);
    socket.recv(&zm,0);
    
    m = (msg*) zm.data();
    return m->data;
}

int main(int argc, char **argv) {
    
    zmq::context_t context;
    zmq::socket_t socket(context, ZMQ_PAIR);

    socket.connect("tcp://127.0.0.1:7777");
    printf("Connected to cocotb axi_server\n");    
        
    unsigned int a = zmq_axi(socket,READ,0);
    zmq_axi(socket,WRITE,0,123456789);
    unsigned int b = zmq_axi(socket,READ,0);
    zmq_axi(socket,DONE);
    
    printf("Before: %u After: %u\n",a,b);
    
    return 0;
}
