# -*- coding: utf-8 -*-
import socket
import os


def get_response(request):
    request = request.decode()
    try:
        method, uri, protocol = request.split('\n')[0].split(' ')
    except ValueError:
        return "HTTP/1.1 200 OK\r\n\r\n".encode()

    if method != "GET":
        return "HTTP/1.1 405 Method Not Allowed\r\n\r\n".encode()

    if uri == "/":
        user_agent = request.split('\n')[2]
        content = user_agent[12:]
        return ("HTTP/1.1 200 OK\r\n\r\n" + 'Hello mister!\nYou are {}'.format(content)).encode()

    elif uri.startswith("/media/"):

        if uri == "/media/":
            response = "HTTP/1.1 200 OK\r\n\r\n"

            for f in os.listdir('/home/lizanoskova/track17-autumn/technotrack-web1-autumn-2017/httpserver/files'):
                response += (f + "\n")

            return response.encode()

        else:

            response = "HTTP/1.1 200 OK\r\n\r\n".encode()
            file_path = os.path.join("/home/lizanoskova/track17-autumn/technotrack-web1-autumn-2017/httpserver/files",
                                     uri.split('/media/')[1])
            if (os.path.exists(file_path)):
                with open(file_path, 'rb') as f:
                    response += f.read() + "\n".encode()
            else:
                return "HTTP/1.1 404 Not found\r\n\r\n".encode() + "No such file\n".encode()

            return response

    elif uri == "/test/":
        return request.encode()

    return "HTTP/1.1 404 Not found\r\n\r\n".encode()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(('localhost', 8000))  # привязываем к сокету номер порта и название хоста
server_socket.listen(0)  #устанавливаем количество соединений, которые могут находиться в очереди

print 'Started'

while 1:
    try:
        (client_socket, address) = server_socket.accept()
        print 'Got new client', client_socket.getsockname()  # при подключении нового клиента печатаем его IP
        request_string = client_socket.recv(2048)  #получаем данные от клиента : максимальный размер 2048
        client_socket.send(get_response(request_string))  # посылаем ответ
        client_socket.close()
    except KeyboardInterrupt:  # останавливаем программу сочетанием клавиш
        print 'Stopped'
        server_socket.close()  # закрываем сокет
        exit()
