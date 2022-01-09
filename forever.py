#!/usr/bin/python
from subprocess import Popen

while True:
    print("\nStarting")
    p = Popen("python3 index.py", shell=True)
    p.wait()