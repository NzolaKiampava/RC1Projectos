#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys

def webclient(server_ip, server_port, filepath):
    """Cliente web que envia requisição HTTP GET"""
    
    # Create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        print("Conectando a {}:{}".format(server_ip, server_port))
        client_socket.connect((server_ip, int(server_port)))
        print("Conectado com sucesso!")
        print("-" * 50)
        
        # Build HTTP request
        request = "GET {} HTTP/1.0\r\n".format(filepath)
        request += "Host: {}:{}\r\n".format(server_ip, server_port)
        request += "Connection: close\r\n"
        request += "\r\n"
        
        print("Enviando requisição:")
        print(request)
        print("-" * 50)
        
        # Send request
        client_socket.sendall(request.encode('utf-8'))
        
        # Receive response
        print("Resposta do servidor:")
        print("-" * 50)
        
        response = b""
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            response += chunk
        
        print(response.decode('utf-8', errors='ignore'))
        print("-" * 50)
        
    except socket.error as e:
        print("Erro de conexão: {}".format(str(e)))
    except Exception as e:
        print("Erro: {}".format(str(e)))
    finally:
        client_socket.close()
        print("Conexão fechada")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python webclient.py <server_ip> <server_port> <filepath>")
        print("Exemplo: python webclient.py 192.168.56.21 6789 /index.html")
        sys.exit(1)
    
    server_ip = sys.argv[1]
    server_port = sys.argv[2]
    filepath = sys.argv[3]
    
    webclient(server_ip, server_port, filepath)
