from IPython.parallel.apps.ipengineapp import IPEngineApp, launch_new_instance
#import sage.all
import numpy

def make_server():
    # listen on socket
    import socket
    from multiprocessing import Process
    host = 'localhost'
    backlog = 5
    size = 1024
    try:
        s = socket_on_open_port()
        s.listen(backlog)
        print "started socket on port:", s.getsockname()[1]
        with open("/tmp/ipsocket", "w") as f:
            f.write(str(s.getsockname()[1]))
        while True:
            client, address = s.accept()
            data = client.recv(size).split(',')
            if data:
                print numpy
                new = IPEngineApp.instance()
                new.initialize(data)
                #new.engine.user_ns = {"sage": sage.all}
                new.engine.user_ns = {"numpy": numpy}
                p = Process(target=new.start)
                p.start()
                print "Process %d started" % p.pid
            client.send(str(p.pid))
            client.close()
    except KeyboardInterrupt:
        s.close()
        print "\nclosed socket"

def socket_on_open_port():
        import socket
        s = socket.socket()
        s.bind(("localhost",0))
        return s

make_server()
