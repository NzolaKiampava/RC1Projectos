# Memorando: Implementação de Cliente/Servidor Web Simples

**Disciplina:** Redes de Comunicação e Internet (RCI)  
**Laboratório:** 2 - Aplicações Web e HTTP  
**Data:** Novembro 2024  

---

## 1. Objetivo

Implementar um servidor web simples e um cliente web para estudar o protocolo HTTP e a comunicação TCP entre cliente e servidor.

---

## 2. Arquivos Implementados

### 2.1 Servidor Web (`webserver.py`)
- **Função:** Aceita conexões TCP na porta 6789 e responde a requisições HTTP GET
- **Porta:** 6789
- **Protocolo:** HTTP/1.0
- **Funcionalidades:**
  - Parsing de requisições HTTP
  - Leitura de arquivos do servidor
  - Resposta com status codes (200, 400, 404, 501)
  - Suporte a múltiplas conexões

### 2.2 Cliente Web (`webclient.py`)
- **Função:** Cliente que envia requisições HTTP GET para o servidor
- **Uso:** `python webclient.py <server_ip> <server_port> <filepath>`
- **Funcionalidades:**
  - Conexão TCP com o servidor
  - Construção de requisição HTTP GET
  - Recebimento e exibição da resposta completa

### 2.3 Arquivo HTML (`index.html`)
- Página de teste com informações sobre o servidor e como utilizá-lo

---

## 3. Teste com Telnet

### 3.1 Comando Executado
```
telnet 192.168.56.21 6789
```

### 3.2 Análise de Pacotes TCP com Telnet

**Captura de tela:** [INSERIR CAPTURA DE TELA AQUI]

#### Análise Detalhada:

1. **Estabelecimento da Conexão TCP (Three-way Handshake)**
   - **SYN:** Cliente envia pacote SYN para o servidor na porta 6789
   - **SYN-ACK:** Servidor responde com SYN-ACK
   - **ACK:** Cliente envia ACK confirmando a conexão
   - **Resultado:** Conexão TCP estabelecida com sucesso

2. **Transmissão da Requisição HTTP**
   - O cliente envia a requisição HTTP GET em texto puro
   - A requisição é segmentada em pacotes TCP (típico: MSS ~1460 bytes)
   - Cada pacote TCP inclui:
     - IP Source: 192.168.56.22 (ou outro cliente)
     - IP Destination: 192.168.56.21 (servidor)
     - TCP Source Port: porta efêmera (>1024)
     - TCP Destination Port: 6789
     - Sequence Number e Acknowledgment Number
     - Flags: PSH (push), ACK

3. **Recebimento da Resposta HTTP**
   - Servidor responde com pacotes contendo a resposta HTTP
   - HTTP headers são enviados primeiro (status, content-type, content-length)
   - Corpo da resposta (HTML) é enviado em seguida
   - Cada pacote é confirmado com ACK do cliente

4. **Encerramento da Conexão TCP (Four-way Handshake)**
   - **FIN:** Uma das partes envia FIN para indicar fim da transmissão
   - **ACK:** A outra parte confirma com ACK
   - **FIN:** A segunda parte também envia FIN
   - **ACK:** Primeira parte confirma com ACK
   - **Resultado:** Conexão TCP fechada

#### Observações com Telnet:
- Com telnet, o usuário escreve manualmente a requisição HTTP
- Permite observar passo-a-passo a comunicação
- Útil para depuração e compreensão do protocolo
- A conexão permanece aberta enquanto o telnet estiver conectado
- O servidor fecha a conexão após a resposta (HTTP/1.0 Connection: close)

---

## 4. Teste com Cliente Web Python

### 4.1 Comando Executado
```
python webclient.py 192.168.56.21 6789 /index.html
```

### 4.2 Análise de Pacotes TCP com Cliente Web

**Captura de tela:** [INSERIR CAPTURA DE TELA AQUI]

#### Análise Detalhada:

1. **Estabelecimento da Conexão TCP (Three-way Handshake)**
   - Idêntico ao telnet
   - SYN → SYN-ACK → ACK

2. **Transmissão Automática da Requisição HTTP**
   - O cliente Python constrói automaticamente a requisição HTTP
   - Requisição típica:
     ```
     GET /index.html HTTP/1.0
     Host: 192.168.56.21:6789
     Connection: close
     ```
   - Headers são incluídos automaticamente (sem entrada manual do usuário)
   - Todo o conteúdo é enviado em um fluxo contínuo

3. **Recebimento da Resposta Completa**
   - Cliente recebe toda a resposta HTTP antes de processar
   - Aguarda o EOF (fim da conexão)
   - Acumula dados em buffer até a resposta completa

4. **Encerramento da Conexão**
   - O cliente fecha ativamente a conexão
   - Four-way handshake (FIN, ACK, FIN, ACK)

#### Observações com Cliente Web Python:
- Automatização completa da requisição HTTP
- Mais eficiente que telnet para testes repetidos
- Permite programar múltiplas requisições
- Maior controle sobre headers HTTP
- Tempo de execução é mais rápido

---

## 5. Comparação: Telnet vs Cliente Web

| Aspecto | Telnet | Cliente Web Python |
|---------|--------|-------------------|
| **Automatização** | Manual | Automática |
| **Headers HTTP** | Digitados manualmente | Gerados automaticamente |
| **Facilidade de Teste** | Moderada | Alta |
| **Visualização do Protocolo** | Clara e detalhada | Rápida e programável |
| **Número de Pacotes TCP** | Igual ou maior (entrada manual) | Otimizado (batching possível) |
| **Tempo de Resposta** | Depende de digitação | Imediato |
| **Tratamento de Erros** | Manual | Automático |

---

## 6. Estrutura de Pacotes HTTP Observada

### 6.1 Requisição HTTP GET
```
GET /index.html HTTP/1.0
Host: 192.168.56.21:6789
[User-Agent: cliente]
[Additional Headers]

```

### 6.2 Resposta HTTP 200 OK
```
HTTP/1.0 200 OK
Content-Type: text/html
Content-Length: [número de bytes]
Connection: close

[HTML content aqui]
```

---

## 7. Conclusões

1. **Funcionamento do Protocolo HTTP:**
   - HTTP é um protocolo baseado em texto simples sobre TCP
   - O cliente envia requisições estruturadas
   - O servidor responde com status e conteúdo

2. **Importância da Camada TCP:**
   - TCP garante entrega confiável e ordenada dos dados
   - O handshake de 3 vias estabelece a conexão
   - O handshake de 4 vias encerra a conexão

3. **Análise de Pacotes:**
   - Com ferramentas como Wireshark, podemos observar:
     - Sequência exata de pacotes
     - Tamanho e conteúdo de cada pacote
     - RTT (Round-Trip Time)
     - Perdas de pacotes (se houver)

4. **Diferenças Práticas:**
   - Telnet é didático para compreender o protocolo
   - Cliente web Python é mais prático para automação e testes

---

## 8. Notas Técnicas

- **Porta 6789:** Escolhida como porta não-privilegiada (>1024)
- **HTTP/1.0:** Versão simplificada do protocolo HTTP
- **Connection: close:** Indica que a conexão será fechada após a resposta
- **IP 192.168.56.21:** Servidor na rede privada Vagrant
- **IP 192.168.56.22-23:** Clientes na rede privada Vagrant

---

## 9. Como Reproduzir os Testes

1. **Iniciar o servidor:**
   ```bash
   cd /pasta/webserver
   python webserver.py 6789
   ```

2. **Teste com Telnet (a partir de client1 ou client2):**
   ```bash
   telnet 192.168.56.21 6789
   GET /index.html HTTP/1.0
   Host: 192.168.56.21:6789
   [Enter][Enter]
   ```

3. **Teste com Cliente Web (a partir de client1 ou client2):**
   ```bash
   python webclient.py 192.168.56.21 6789 /index.html
   ```

4. **Captura de pacotes com tcpdump:**
   ```bash
   sudo tcpdump -i eth1 -w captura.pcap -n tcp port 6789
   ```

---

## 10. Referências

- RFC 7230: HTTP/1.1 Message Syntax and Routing
- RFC 793: Transmission Control Protocol (TCP)
- Python Socket Documentation
- Wireshark User Guide

---

**Documento preparado para análise e apresentação no Laboratório 2 de RCI**
