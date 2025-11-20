# -*- coding: utf-8 -*-

"""
Lab3 - Servidor e Cliente Web

Estudante: Nzola Kiampava
Docente: João Costa (joaojdacosta@gmail.com)
Outubro, 2024.
"""

from socket import *  # importa o módulo socket
import sys  # Por forma a terminar o programa

# Cria um socket do servidor TCP
# (AF_INET é utilizado para o protocolo IPv4)
# (SOCK_STREAM é utilizado para o TCP)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Atribui o número de porta
serverPort = 6789

# TODO #1: Vincular o socket ao endereço e porta do servidor
serverSocket.bind(('', serverPort))

# TODO #2: Escutar, no máximo, 1 conexão por vez
serverSocket.listen(1)

# O servidor deve estar Up, em execução e à escuta
# por novas conexões
while True:
    print('O servidor está pronto para receber')

    # TODO #3: Configurar uma nova conexão do cliente
    connectionSocket, addr = serverSocket.accept()

    try:
        # TODO #4: Receber a mensagem de solicitação do cliente
        message = connectionSocket.recv(1024).decode()

        # Extrai o caminho do objeto pedido
        filename = message.split()[1]

        # Abre o ficheiro solicitado
        f = open(filename[1:])

        # Lê todo o conteúdo do ficheiro
        outputdata = f.read()

        # TODO #5: Enviar a linha de cabeçalho de resposta HTTP
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

        # Envia o conteúdo do ficheiro solicitado
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())

        connectionSocket.send("\r\n".encode())

        # Fecha o socket de conexão do cliente
        connectionSocket.close()

    except IOError:
        # TODO #6: Enviar mensagem de resposta HTTP para ficheiro não encontrado
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>\r\n".encode())

        # TODO #7: Fechar o socket de conexão do cliente
        connectionSocket.close()

# Fecha o socket do servidor
serverSocket.close()
sys.exit()  # Encerra o programa após enviar os dados correspondentes.
