import socket
import threading
import time

# --- Configurações de Rede ---
UDP_IP = "127.0.0.1"  # Endereço de escuta para UDP
UDP_PORT = 9000       # Porta de escuta para UDP
TCP_IP = "127.0.0.1"  # Endereço de escuta para TCP
TCP_BASE_PORT = 9001  # Porta base para a escuta TCP dos clientes

# --- Estruturas de Dados ---
# Armazena os clientes conectados: {SeqNum: (IP, PortTCP)}
clientes_registados = {}
proximo_seqnum = 1
LOCK_CLIENTES = threading.Lock()

def listener_udp():
    """Ouve pedidos de adesão de clientes via UDP."""
    global proximo_seqnum
    
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_udp.bind((UDP_IP, UDP_PORT))
    print(f"Servidor UDP a escutar em {UDP_IP}:{UDP_PORT}")

    while True:
        try:
            # Recebe dados do cliente UDP
            data, addr = sock_udp.recvfrom(1024)
            mensagem = data.decode()

            if "ADESAO" in mensagem:
                # Espera-se que a mensagem seja "ADESAO <IP>,<PortTCP>"
                partes = mensagem.split()
                if len(partes) < 2:
                    continue
                
                # Extrai o tuplo <IP, PortTCP> do pedido do cliente
                client_ip, client_port_str = partes[1].split(',')
                client_port_tcp = int(client_port_str)
                
                with LOCK_CLIENTES:
                    # 1. Gera SeqNum e armazena
                    seqnum_cliente = proximo_seqnum
                    proximo_seqnum += 1
                    
                    clientes_registados[seqnum_cliente] = (client_ip, client_port_tcp)
                    
                    # 2. Envia <Status, SeqNum> de volta ao cliente (via UDP)
                    resposta = f"OK {seqnum_cliente}"
                    sock_udp.sendto(resposta.encode(), addr)
                    print(f"Cliente {client_ip}:{client_port_tcp} registado com SeqNum={seqnum_cliente}")

                    # 3. Envia <IP, PortTCP, SeqNum> de TODOS os clientes para o cliente recém-registado
                    # Converte a lista de clientes para uma string para envio
                    lista_clientes_str = ""
                    for seq, (ip, porta) in clientes_registados.items():
                        # Exclui o próprio cliente da lista (pode ser ajustado)
                        if seq != seqnum_cliente:
                            lista_clientes_str += f"{ip},{porta},{seq};"

                    if lista_clientes_str:
                        # O tuplo é uma lista separada por ';'
                        print(f"Enviando lista de peers para o Cliente {seqnum_cliente}...")
                        sock_udp.sendto(lista_clientes_str.encode(), addr)
                
        except Exception as e:
            print(f"Erro no listener UDP: {e}")
            break

# --- Thread principal para o Servidor ---
if __name__ == "__main__":
    # Inicia a escuta UDP numa thread separada
    udp_thread = threading.Thread(target=listener_udp)
    udp_thread.start()

    # O servidor fica em loop ou pode gerir outras tarefas aqui
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nServidor a encerrar.")
        # É necessário implementar um mecanismo para parar a thread UDP de forma elegante
        # Por simplicidade, CTRL+C irá encerrar a execução.