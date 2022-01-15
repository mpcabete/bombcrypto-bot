#!/usr/bin/python
from subprocess import Popen

while True:
    print("\nStarting")
    p = Popen("python index.py", shell=True)
    p.wait()