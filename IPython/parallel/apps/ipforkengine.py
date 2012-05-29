from IPython.parallel.apps.ipengineapp import IPEngineApp, launch_new_instance

def make_server():
    # listen on socket
    import socket
    from multiprocessing import Process
    host = 'localhost'
    port = 51337
    #port = find_open_port()
    #todo: add communication so that socket can be at a random open port
    backlog = 5
    size = 1024
    try:
        s = socket.socket()
        s.bind((host,port))
        s.listen(backlog)
        print "started socket on port:", s.getsockname()[1]
        while 1:
            client, address = s.accept()
            data = client.recv(size).split(',')
            if data:
                p=Process(target=launch_new_instance, args=(data,))
                p.start()
            client.send(str(p.pid))
            client.close()
    except KeyboardInterrupt:
        s.close()
        print "\nclosed socket"

def find_open_port():
        import socket
        s = socket.socket()
        s.bind(("localhost",0))
        port = s.getsockname()[1]
        s.close()
        return port

make_server()
