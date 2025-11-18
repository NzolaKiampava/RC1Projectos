# Implementação de Cliente/Servidor Web Simples - Lab 2 RCI

## 📋 Conteúdo da Pasta

```
webserver/
├── webserver.py          # Servidor web simples em Python
├── webclient.py          # Cliente web em Python
├── index.html           # Página HTML de teste
├── MEMORANDO.md         # Análise completa dos testes
├── start_webserver.sh   # Script para iniciar o servidor
└── README.md            # Este arquivo
```

## 🎯 Objetivo

Este laboratório implementa um servidor web simples e um cliente web para estudar:
- Protocolo HTTP/1.0
- Comunicação TCP cliente-servidor
- Análise de pacotes de rede
- Interação entre camadas de aplicação e transporte

## 🚀 Como Usar

### Pré-requisitos
- Python 2.7+ ou Python 3.x
- Acesso a máquina virtual com IP 192.168.56.21 (servidor)
- Máquinas cliente com IPs 192.168.56.22-23

### 1. Iniciar o Servidor

Na máquina servidor (webserver):

```bash
# Opção 1: Direto com Python
python webserver.py 6789

# Opção 2: Usando script
chmod +x start_webserver.sh
./start_webserver.sh 6789
```

Saída esperada:
```
WebServer iniciado na porta 6789
Aguardando conexões...
```

### 2. Testar com Telnet

Na máquina cliente (client1 ou client2):

```bash
telnet 192.168.56.21 6789
```

Depois, digite a requisição HTTP:

```
GET /index.html HTTP/1.0
Host: 192.168.56.21:6789

```

(Pressione Enter duas vezes após a requisição)

### 3. Testar com Cliente Web

Na máquina cliente:

```bash
python webclient.py 192.168.56.21 6789 /index.html
```

## 📊 Análise de Pacotes

### Usando Wireshark

1. Iniciar captura de pacotes:
```bash
sudo wireshark &
```

2. Selecionar interface eth1 (rede privada 192.168.56.x)

3. Filtrar por: `tcp.port == 6789`

4. Executar testes (telnet ou cliente web)

### Usando tcpdump

```bash
# Capturar em arquivo
sudo tcpdump -i eth1 -w captura_telnet.pcap tcp port 6789

# Exibir em tempo real
sudo tcpdump -i eth1 -n tcp port 6789

# Analisar arquivo salvo
tcpdump -r captura_telnet.pcap -A
```

## 📝 Documentação

Consulte o arquivo **MEMORANDO.md** para:
- Análise detalhada dos pacotes TCP com telnet
- Análise detalhada dos pacotes TCP com cliente web
- Comparação entre os dois métodos
- Estrutura de pacotes HTTP
- Conclusões e notas técnicas

## 🔧 Estrutura do Protocolo HTTP

### Requisição HTTP GET

```
GET /index.html HTTP/1.0
Host: 192.168.56.21:6789
Connection: close

```

### Resposta HTTP 200 OK

```
HTTP/1.0 200 OK
Content-Type: text/html
Content-Length: 1234
Connection: close

[HTML content aqui]
```

## 📌 Endereços IP

| Máquina | IP | Porta | Serviço |
|---------|-----|--------|---------|
| webserver | 192.168.56.21 | 6789 | HTTP |
| client1 | 192.168.56.22 | - | Cliente |
| client2 | 192.168.56.23 | - | Cliente |

## 🐛 Troubleshooting

### Erro: Connection refused
- Verificar se o servidor está rodando: `netstat -tuln | grep 6789`
- Verificar firewall: `sudo ufw allow 6789`

### Erro: Name resolution error no telnet
- Usar IP ao invés de hostname: `telnet 192.168.56.21 6789`
- Verificar conectividade: `ping 192.168.56.21`

### Arquivo não encontrado
- Confirmar que index.html está no mesmo diretório do servidor
- Usar caminho absoluto se necessário

## 📚 Referências

- [RFC 7230 - HTTP/1.1](https://tools.ietf.org/html/rfc7230)
- [RFC 793 - TCP](https://tools.ietf.org/html/rfc793)
- [Python Socket Documentation](https://docs.python.org/3/library/socket.html)
- [Wireshark User Guide](https://www.wireshark.org/docs/)

## ✅ Checklist de Testes

- [ ] Servidor inicia com sucesso
- [ ] Cliente consegue conectar com telnet
- [ ] Cliente consegue enviar requisição HTTP via telnet
- [ ] Servidor responde corretamente via telnet
- [ ] Cliente Python conecta e recebe resposta
- [ ] Captura de pacotes com Wireshark funciona
- [ ] Análise de pacotes completa (veja MEMORANDO.md)

---

**Laboratório 2 - Aplicações Web e HTTP | RCI 2024**
