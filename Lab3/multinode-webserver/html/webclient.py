# -*- coding: utf-8 -*-
"""
Lab3 - Servidor e Cliente Web

Estudante: Nzola Kiampava
Docente: João Costa (joaojdacosta@gmail.com)
Outubro, 2024.
"""

from socket import *
import sys

if len(sys.argv) != 4:
    print('Uso: python webclient.py <server_host> <server_port> <filename>')
    sys.exit()

serverHost = sys.argv[1]
serverPort = int(sys.argv[2])
filename = sys.argv[3]

clientSocket = socket(AF_INET, SOCK_STREAM)

try:
    clientSocket.connect((serverHost, serverPort))

    # Substituindo f-string por .format()
    request = "GET {} HTTP/1.1\r\nHost: {}\r\n\r\n".format(filename, serverHost)

    print("Enviando requisição: {}".format(request.strip().replace('\r\n', ' ')))
    clientSocket.send(request.encode())

    print("\n--- Resposta do Servidor ---\n")
    response = b''
    while True:
        chunk = clientSocket.recv(1024)
        if not chunk:
            break
        response += chunk

    print(response.decode())

except ConnectionRefusedError:
    print("Erro: Conexão recusada. Verifique se o servidor está ativo em {}:{}".format(serverHost, serverPort))

except Exception as e:
    print("Ocorreu um erro: {}".format(e))

finally:
    clientSocket.close()

sys.exit()
