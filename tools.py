#!/usr/bin/env python
# -*- coding: utf-8 -*-
def command_run(command,timeout=10):
    import subprocess
    import time
    proc = subprocess.Popen(command,bufsize=0,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    poll_seconds = .250
    deadline = time.time() + timeout
    while time.time() < deadline and proc.poll() == None:
        time.sleep(poll_seconds)
    if proc.poll() == None:
        proc.terminate()
        return None
    return proc.returncode

def string(value):
    """
    >>> string(2)
    '2'
    """
    try:
        return str(value)
    except UnicodeEncodeError:
        return value

if __name__ == '__main__':
    print(command_run('dir'))
