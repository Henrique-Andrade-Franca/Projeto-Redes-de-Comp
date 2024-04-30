import socket
import random
import struct

def montar_cabecalho_udp(porta_origem, porta_destino, tamanho_total):
    # Montar o cabeçalho UDP
    # Cabeçalho UDP: porta origem (16 bits), porta destino (16 bits), tamanho (16 bits), checksum (16 bits)
    cabecalho = struct.pack('!HHHH', porta_origem, porta_destino, tamanho_total, 0)
    return cabecalho

def montar_cabecalho_ip(ip_origem, ip_destino, protocolo, tamanho_total):
    # Convertendo endereços IP para representação de bytes
    ip_origem_bytes = socket.inet_aton(ip_origem)
    ip_destino_bytes = socket.inet_aton(ip_destino)
    
    # Montar o cabeçalho IP
    # Cabeçalho IP: versão, IHL, tipo de serviço, tamanho total, identificador, flags, offset, TTL, protocolo, checksum,
    # IP origem (32 bits), IP destino (32 bits)
    cabecalho = struct.pack('!BBHHHBBH4s4s', 69, 0, 0, tamanho_total, 0, 64, protocolo, 0, ip_origem_bytes, ip_destino_bytes)
    return cabecalho

def enviar_requisicao(socket_raw, tipo, identificador):
    # Endereço IP e porta do servidor
    SERVER_IP = '15.228.191.109'
    SERVER_PORT = 50000
    
    # Montar o payload da mensagem
    payload = struct.pack('!BBBBH', 0, tipo, identificador >> 8, identificador & 0xFF, 0)
    
    # Montar o cabeçalho UDP
    cabecalho_udp = montar_cabecalho_udp(12345, SERVER_PORT, len(payload))
    
    # Montar o cabeçalho IP
    cabecalho_ip = montar_cabecalho_ip('192.168.0.1', SERVER_IP, socket.IPPROTO_UDP, len(cabecalho_udp) + len(payload))
    
    # Enviar pacote UDP/IP
    socket_raw.sendto(cabecalho_ip + cabecalho_udp + payload, (SERVER_IP, SERVER_PORT))
    
    # Receber resposta do servidor
    dados, _ = socket_raw.recvfrom(1024)
    return dados

def exibir_resposta(resposta):
    # Interpretar a resposta
    tipo_resposta = resposta[1] & 0b00001111
    tamanho_resposta = resposta[3]
    
    if tipo_resposta == 0:
        print("Data e hora atual:", resposta[4:].decode('utf-8', errors='ignore'))
    elif tipo_resposta == 1:
        print("Mensagem motivacional:", resposta[4:].decode('utf-8', errors='ignore'))
    elif tipo_resposta == 2:
        print("Quantidade de respostas emitidas pelo servidor:", struct.unpack('!I', resposta[4:8])[0])
    else:
        print("Tipo de resposta inválido")

# Criar socket RAW
cliente_socket_raw = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

# Loop principal do cliente
while True:
    print("\nEscolha uma opção:")
    print("1. Data e hora atual")
    print("2. Mensagem motivacional para o fim do semestre")
    print("3. Quantidade de respostas emitidas pelo servidor")
    print("4. Sair")
    escolha = int(input("Opção: "))
    
    if escolha == 4:
        break
    
    if escolha in [1, 2, 3]:
        # Gerar identificador aleatório entre 1 e 65535
        identificador = random.randint(1, 65535)  
        resposta = enviar_requisicao(cliente_socket_raw, escolha - 1, identificador)
        exibir_resposta(resposta)
    else:
        print("Opção inválida. Tente novamente.")

# Fechar o socket
cliente_socket_raw.close()
