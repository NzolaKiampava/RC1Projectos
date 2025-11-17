#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import os

def parse_request(request):
    """Parse HTTP request and extract the requested file path"""
    lines = request.split('\r\n')
    if len(lines) < 1:
        return None
    
    parts = lines[0].split()
    if len(parts) < 2:
        return None
    
    method = parts[0]
    path = parts[1]
    
    return method, path

def read_file(filepath):
    """Read file content, handling relative paths"""
    # Remove leading slash and ensure safe path
    if filepath.startswith('/'):
        filepath = filepath[1:]
    
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print("Error reading file: {}".format(str(e)))
        return None

def build_response(status_code, status_text, content=""):
    """Build HTTP response"""
    response = "HTTP/1.0 {} {}\r\n".format(status_code, status_text)
    response += "Content-Type: text/html\r\n"
    response += "Content-Length: {}\r\n".format(len(content))
    response += "Connection: close\r\n"
    response += "\r\n"
    response += content
    return response

def main():
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 6789
    
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind and listen
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)
    
    print("WebServer iniciado na porta {}".format(port))
    print("Aguardando conexões...")
    
    try:
        while True:
            # Accept connection
            client_socket, client_address = server_socket.accept()
            print("\nConexão recebida de: {}:{}".format(client_address[0], client_address[1]))
            
            # Receive request
            request = client_socket.recv(4096).decode('utf-8')
            print("Request recebido:")
            print(request)
            print("-" * 50)
            
            # Parse request
            result = parse_request(request)
            if result is None:
                response = build_response(400, "Bad Request")
                client_socket.sendall(response.encode('utf-8'))
            else:
                method, path = result
                
                if method != "GET":
                    response = build_response(501, "Not Implemented")
                    client_socket.sendall(response.encode('utf-8'))
                else:
                    # Handle default path
                    if path == "/":
                        path = "/index.html"
                    
                    # Read file
                    content = read_file(path)
                    
                    if content is None:
                        response = build_response(404, "Not Found")
                        client_socket.sendall(response.encode('utf-8'))
                    else:
                        response = build_response(200, "OK", content)
                        client_socket.sendall(response.encode('utf-8'))
            
            client_socket.close()
            print("Conexão fechada\n")
    
    except KeyboardInterrupt:
        print("\nServidor interrompido pelo utilizador")
    finally:
        server_socket.close()
        print("Socket do servidor fechado")

if __name__ == "__main__":
    main()
