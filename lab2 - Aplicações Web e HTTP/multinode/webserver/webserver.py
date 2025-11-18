#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import os
import sys

def send_response(client_socket, status_code, status_message, content_type, body):
    """Envia resposta HTTP para o cliente"""
    try:
        response = "HTTP/1.1 %d %s\r\n" % (status_code, status_message)
        response += "Content-Type: %s; charset=utf-8\r\n" % content_type
        
        # Codifica o body em UTF-8
        if isinstance(body, str):
            body_bytes = body.encode('utf-8')
        else:
            body_bytes = body
        
        response += "Content-Length: %d\r\n" % len(body_bytes)
        response += "Connection: close\r\n"
        response += "\r\n"
        
        # Envia headers como UTF-8
        client_socket.sendall(response.encode('utf-8'))
        # Envia body
        client_socket.sendall(body_bytes)
        
        print("Resposta %d %s enviada" % (status_code, status_message))
    except Exception as e:
        print("Erro ao enviar resposta: %s" % e)

def handle_client(client_socket, client_address):
    """Processa requisição do cliente"""
    try:
        # Recebe dados do cliente
        request_data = client_socket.recv(1024).decode('utf-8', errors='ignore')
        
        if not request_data:
            client_socket.close()
            return
        
        print("Conexão recebida de: %s:%d" % (client_address[0], client_address[1]))
        print("Request recebido:")
        print(request_data[:200])
        print("-" * 50)
        
        # Parse da requisição
        request_lines = request_data.split('\r\n')
        request_line = request_lines[0].split()
        
        if len(request_line) < 2:
            error_html = "<html><body><h1>400 Bad Request</h1></body></html>"
            send_response(client_socket, 400, "Bad Request", "text/html", error_html)
            client_socket.close()
            return
        
        method = request_line[0]
        path = request_line[1]
        
        print("Método: %s, Caminho: %s" % (method, path))
        
        if method != 'GET':
            error_html = "<html><body><h1>501 Method Not Implemented</h1></body></html>"
            send_response(client_socket, 501, "Method Not Implemented", "text/html", error_html)
            client_socket.close()
            return
        
        if path == '/':
            path = '/index.html'
        
        # Caminho do arquivo
        doc_root = os.path.dirname(__file__)
        file_path = os.path.join(doc_root, path.lstrip('/'))
        
        print("Procurando arquivo: %s" % file_path)
        
        if not os.path.exists(file_path):
            error_html = "<html><body><h1>404 Not Found</h1><p>Arquivo não encontrado</p></body></html>"
            send_response(client_socket, 404, "Not Found", "text/html", error_html)
            client_socket.close()
            return
        
        if not os.path.isfile(file_path):
            error_html = "<html><body><h1>400 Invalid Request</h1></body></html>"
            send_response(client_socket, 400, "Bad Request", "text/html", error_html)
            client_socket.close()
            return
        
        # Lê o arquivo
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Detecta tipo de conteúdo
        if file_path.endswith('.html'):
            content_type = "text/html"
        elif file_path.endswith('.txt'):
            content_type = "text/plain"
        else:
            content_type = "text/plain"
        
        send_response(client_socket, 200, "OK", content_type, file_content)
        
    except Exception as e:
        print("Erro ao processar cliente: %s" % e)
        error_html = "<html><body><h1>500 Internal Server Error</h1></body></html>"
        send_response(client_socket, 500, "Internal Server Error", "text/html", error_html)
    finally:
        print("Socket do servidor fechado")
        client_socket.close()

def main():
    """Função principal do servidor"""
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 6789
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    
    print("WebServer iniciado na porta %d" % port)
    print("Aguardando conexões...")
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            handle_client(client_socket, client_address)
    except KeyboardInterrupt:
        print("\nServidor interrompido pelo usuário")
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()