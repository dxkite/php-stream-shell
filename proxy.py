# encoding = utf8
# coding:utf-8

import socket
import urllib.parse
import requests 
import base64

from multiprocessing import Process


def proxy_client(client_socket):
    """
    处理代理请求
    """
    request_data = client_socket.recv(1024)
    # print("request data:", request_data)
    header,body=request_data.decode("UTF-8").split("\r\n\r\n",1);
    params = str(urllib.parse.unquote(body))
    params = params.split('&')
    post_param =  {
        'password':'dxkite'
    }
    for param in params :
        name,value = param.split('=',1)
        if name == 'code':
            post_param['code'] = base64.b64encode(('<?php '+value+' ?>').encode('UTF-8'))
        else:
            post_param[name] = value
    print(post_param)
    res=requests.post('http://suda.atd3.org/assets/eval/eval2.php',post_param)
    response_body=res.text
    # 构造响应数据
    response_start_line = "HTTP/1.1 200 OK\r\n"
    response_headers = "Server: Stream Proxy\r\n"
    response = response_start_line + response_headers + "\r\n" + response_body

    # 向客户端返回响应数据
    client_socket.send(bytes(response, "utf-8"))
    # 关闭客户端连接
    client_socket.close()


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("", 8888))
    server_socket.listen(128)
    print('listen 8888 ...');
    while True:
        client_socket, client_address = server_socket.accept()
        handle_client_process = Process(target=proxy_client, args=(client_socket,))
        handle_client_process.start()
        client_socket.close()