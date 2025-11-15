import socket
import threading
import time

# --- Configurações de Rede ---
SERVER_IP = "127.0.0.1"
SERVER_UDP_PORT = 9000

# O cliente deve ouvir numa porta TCP específica para receber mensagens
# (A porta real deve ser atribuída dinamicamente ou fixada para o teste)
CLIENT_TCP_PORT = 0 # 0 permite que o SO escolha uma porta livre
CLIENT_IP = "127.0.0.1"
MEU_SEQNUM = -1
PEERS = [] # Lista de tuplos de outros clientes: [(IP, PortTCP, SeqNum)]

def listener_tcp():
    """Ouve conexões TCP de outros clientes para trocar mensagens."""
    global CLIENT_TCP_PORT
    
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.bind((CLIENT_IP, CLIENT_TCP_PORT))
    
    # Obtém a porta real atribuída pelo SO
    CLIENT_TCP_PORT = sock_tcp.getsockname()[1]
    
    sock_tcp.listen(5)
    print(f"Cliente a escutar em {CLIENT_IP}:{CLIENT_TCP_PORT} para comunicação TCP.")
    
    while True:
        try:
            conn, addr = sock_tcp.accept()
            print(f"Conexão TCP estabelecida com {addr}")
            
            data = conn.recv(1024)
            if data:
                print(f"Mensagem recebida de {addr}: {data.decode()}")
            conn.close()
        except Exception as e:
            # Isso pode ocorrer ao encerrar o programa
            # print(f"Erro no listener TCP: {e}") 
            break

def conversar_tcp(peer_ip, peer_port, mensagem):
    """Conecta-se a um cliente peer via TCP para enviar uma mensagem."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((peer_ip, peer_port))
        sock.sendall(mensagem.encode())
        print(f"Mensagem enviada para {peer_ip}:{peer_port}")
        sock.close()
    except Exception as e:
        print(f"Erro ao conectar-se ou enviar mensagem ao peer {peer_ip}:{peer_port}: {e}")

def main_cliente():
    """Lógica principal do cliente: adesão UDP e início da comunicação."""
    global MEU_SEQNUM, CLIENT_TCP_PORT, PEERS

    # 1. Inicia o Listener TCP
    tcp_thread = threading.Thread(target=listener_tcp)
    tcp_thread.start()
    
    # Aguarda a thread iniciar e obter a porta real
    time.sleep(0.5)

    # 2. Solicita Adesão ao Servidor via UDP
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Envia o tuplo <IP, PortTCP> do cliente
    pedido_adesao = f"ADESAO {CLIENT_IP},{CLIENT_TCP_PORT}"
    sock_udp.sendto(pedido_adesao.encode(), (SERVER_IP, SERVER_UDP_PORT))
    print(f"Pedido de adesão UDP enviado: {pedido_adesao}")

    # 3. Recebe a resposta do servidor (<Status, SeqNum> e lista de peers)
    try:
        # Recebe <Status, SeqNum>
        data_status, _ = sock_udp.recvfrom(1024)
        status_msg = data_status.decode()
        status, seqnum_str = status_msg.split()
        
        if status == "OK":
            MEU_SEQNUM = int(seqnum_str)
            print(f"Adesão bem-sucedida. Meu SeqNum é: {MEU_SEQNUM}")
            
            # Recebe lista de peers (se houver)
            data_peers, _ = sock_udp.recvfrom(1024)
            peers_str = data_peers.decode()
            
            if peers_str:
                # Processa a string de peers
                peers_list = peers_str.split(';')
                for peer in peers_list:
                    if peer:
                        ip, port, seq = peer.split(',')
                        PEERS.append((ip, int(port), int(seq)))
                print(f"Peers recebidos: {PEERS}")
            
            # 4. Inicia a troca de mensagens TCP (Desafio)
            if PEERS:
                # Tenta conversar com o primeiro peer
                peer_ip, peer_port, peer_seq = PEERS[0]
                mensagem = f"Olá do Cliente {MEU_SEQNUM}!"
                conversar_tcp(peer_ip, peer_port, mensagem)
                
        else:
            print(f"Adesão falhou. Status: {status}")

    except Exception as e:
        print(f"Erro na comunicação UDP com o servidor: {e}")
    finally:
        sock_udp.close()
        
# --- Execução ---
if __name__ == "__main__":
    main_cliente()