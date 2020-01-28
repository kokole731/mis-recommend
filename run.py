"""
input[int]: 5 mid
output[json]: 8 recommend meetings
"""

from socket import *
import json

from root.parse.handle import Parse

HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)


while True:

    print('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('...connected from:', addr)

    try:
        data = tcpCliSock.recv(BUFSIZ)
        data = eval(data)
        print("input: " + str(data))
        input_data = []
        for i in data.values():
            input_data.append(i)

        parse = Parse(input_data)
        rst_list = parse.get_result()
        index = 0
        rst_dict = {}

        for i in rst_list:
            rst_dict[index] = i
            index += 1
        print("output: " + str(rst_dict))
        tcpCliSock.send(json.dumps(rst_dict).encode())
        tcpCliSock.close()
    except Exception:
        tcpCliSock.close()
        continue






