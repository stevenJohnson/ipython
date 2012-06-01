#!/usr/bin/env python

import subprocess
import sys
import paramiko
import os
import os.path
import shutil
import zmq
import tempfile
from IPython.core.profiledir import ProfileDir
from IPython.core.application import BaseIPythonApplication

null = open(os.devnull, "w")
trusted_profile = ProfileDir.create_profile_dir_by_name(BaseIPythonApplication.ipython_dir.default_value, "sagecell").location
print "Starting controller..."
subprocess.Popen(["ipcontroller", "--profile-dir", trusted_profile], stderr=null, stdout=null)
context = zmq.Context()
req = context.socket(zmq.REQ)
port = req.bind_to_random_port("tcp://127.0.0.1")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("localhost", username=sys.argv[1] if len(sys.argv) > 1 else None)
untrusted_profile = ssh.exec_command("python -c 'import tempfile, os; x = tempfile.mkdtemp(); print x; os.rmdir(x)'")[1].read().strip()
while not os.path.exists("%s/security/ipcontroller-engine.json" % (trusted_profile,)):
    pass
if len(sys.argv) > 1:
    subprocess.Popen(["scp", "-qr", trusted_profile, "%s@localhost:%s" % (sys.argv[1], untrusted_profile)]).wait()
ssh.exec_command("sage '%s/ipforkengine.py' %d '%s' 2>'%s'" %
        (os.getcwd(), port, untrusted_profile if len(sys.argv) > 1 else trusted_profile, "/tmp/log.txt" if "--debug" in sys.argv else os.devnull))
sys.stdout.write("Loading Sage...")
sys.stdout.flush()
req.send("")
req.recv()
print "done!\n\nPress Enter to start a new engine."
try:
    while True:
        raw_input()
        req.send("")
        sys.stdout.write("Engine opened on PID %s" % (req.recv(),))
except KeyboardInterrupt:
    pass
finally:
    null.close()
    shutil.rmtree(trusted_profile)
    ssh.exec_command("rm -r '%s'" % untrusted_profile)[1].read()
    ssh.close()
    print
