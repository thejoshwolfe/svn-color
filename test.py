#!/usr/bin/env python

import subprocess
import os

def test(args, simulated_output):
  print("\n\n>>> svn " + " ".join(args))
  cmd = [os.path.join(os.path.dirname(__file__), "svn-color.py"), "--__test__"] + args
  process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
  process.communicate(simulated_output)

test(["st"], """\
A       added.txt
M       modified.txt
D       deleted.txt
""")
