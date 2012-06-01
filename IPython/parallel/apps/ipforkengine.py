from IPython.parallel.apps.ipengineapp import IPEngineApp
from multiprocessing import Process
#import sage.all
import numpy
import zmq
import sys

context = zmq.Context()
rep = context.socket(zmq.REP)
rep.connect("tcp://127.0.0.1:%s" % (sys.argv[1],))
while True:
    rep.recv()
    new = IPEngineApp.instance()
    new.initialize(["--profile-dir", sys.argv[2]])
    #new.engine.user_ns = {"sage": sage.all}
    new.engine.user_ns = {"numpy": numpy}
    p = Process(target=new.start)
    p.start()
    rep.send(str(p.pid))
