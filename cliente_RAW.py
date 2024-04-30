import socket
import struct
import random

SERVER_IP = '15.228.191.109'
SERVER_PORT = 50000

def enviar_requisicao(socket_cliente, packet):
    # Formato da mensagem de requisição: req/res (4 bits), tipo (4 bits), identificador (16 bits)
    """
      outra alternativa para empacotar os valores de tipo e identificador em uma sequência de bytes
      formato '!BBH' indica que estamos empacotando dois unsigned bytes (B) seguidos por um unsigned
      short integer de 16 bits (H)
      =================================================================================================
      adicionar: import struct
      substituir: mensagem = struct.pack('!BBH', tipo, 0, identificador)  # O segundo byte é reservado
      para possíveis futuras extensões
    """
    socket_cliente.sendto(packet, (SERVER_IP, SERVER_PORT))
    dados, _ = socket_cliente.recvfrom(1024)  # Recebendo resposta do servidor
    return dados

def exibir_resposta(resposta):
    # extrai os primeiros 4 bits do 1º byte da resposta, que representam o tipo da resposta (0, 1 ou 2)
    tipo_resposta = resposta[0] & 0b00001111
    tamanho_resposta = resposta[3]

    # Verificar se o tamanho da resposta corresponde ao valor especificado no cabeçalho
    if len(resposta) != tamanho_resposta + 4:
        print("Erro: Tamanho da resposta incorreto")
        return
    
    """
      [4:4+tamanho_resposta]: retorna parte dos bytes da resposta, começa do quinto byte (índice 4)
      até o índice correspondente
      ao quarto byte mais o tamanho da propria resposta, p/ n incluir o cabeçalho da mensagem
    """
    # Exibir a resposta de acordo com o tipo
    if tipo_resposta == 0:
        print("Data e hora atual:", str(resposta[4:4+tamanho_resposta], 'latin-1'))
    elif tipo_resposta == 1:
        print("Mensagem motivacional:", str(resposta[4:4+tamanho_resposta], 'latin-1'))
    elif tipo_resposta == 2:
        """
          byteorder='big': especifica a ordem dos bytes ao interpretar um número inteiro a
          partir de uma sequência de bytes; 'big': significa que os bytes mais significativos
          (mais à esquerda na sequência de bytes) representam os bits mais significativos do nº inteiro
        """
        print("Quantidade de respostas emitidas pelo servidor:", int.from_bytes(resposta[4:4+tamanho_resposta], byteorder='big'))

# Função para calcular o checksum IP
def calc_checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        w = (data[i] << 8) + (data[i+1])
        checksum += w
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = ~checksum & 0xffff
    return checksum

# Cabeçalho IP
def create_ip_header(source_ip, dest_ip):
    version_ihl = 69  # Versão 4 do IP, IHL = 5 (20 bytes)
    dscp_ecn = 0
    total_length = 20 + 8  # Tamanho do cabeçalho IP + tamanho do cabeçalho UDP
    identification = 0
    flags_offset = 0
    ttl = 64
    protocol = socket.IPPROTO_UDP
    checksum = 0
    source_addr = socket.inet_aton(source_ip)
    dest_addr = socket.inet_aton(dest_ip)

    ip_header = struct.pack('!BBHHHBBH4s4s', version_ihl, dscp_ecn, total_length,
                            identification, flags_offset, ttl, protocol, checksum,
                            source_addr, dest_addr)
    checksum = calc_checksum(ip_header)
    ip_header = struct.pack('!BBHHHBBH4s4s', version_ihl, dscp_ecn, total_length,
                            identification, flags_offset, ttl, protocol, checksum,
                            source_addr, dest_addr)

    return ip_header

# Cabeçalho UDP
def create_udp_header(source_port, dest_port, data_length):
    udp_length = 8 + data_length  # Tamanho do cabeçalho UDP + tamanho dos dados
    checksum = 0
    udp_header = struct.pack('!HHHH', source_port, dest_port, udp_length, checksum)
    return udp_header


# Endereços de origem e destino
source_ip = socket.gethostbyname(socket.gethostname())
dest_ip = '15.228.191.109'

# Portas de origem e destino
source_port = 12345
dest_port = 5000



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
        mensagem = bytes([escolha - 1, identificador >> 8, identificador & 0xFF])

        ip_header = create_ip_header(source_ip, dest_ip)
        udp_header = create_udp_header(source_port, dest_port, len(mensagem))
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        packet = ip_header + udp_header + mensagem

        resposta = enviar_requisicao(raw_socket, packet)
        exibir_resposta(resposta)
    else:
        print("Opção inválida. Tente novamente.")
