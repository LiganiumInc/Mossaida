import shlex, subprocess

import requests

def load_lottieur(url):
    r=requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()


def exe_cmd(command_line):
    args = shlex.split(command_line)
    print(args)
    p = subprocess.Popen(args)    
