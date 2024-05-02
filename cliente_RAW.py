"""
Grupo: HENRIQUE DE ANDRADE FRANCA       - 20210024961
       ISAAC SEBASTIAN LIMA DE ARAUJO   - 20210025403
       RODRIGO LANES MENESES            - 20210025243
       
Descrição: Implementação do cliente (socket RAW)
Linguagem: Python

"""

'''
UDP Field:
 0      7 8     15 16    23 24    31 
+--------+--------+--------+--------+
|      Source     |    Destination  |
|       Port      |       Port      |
+--------+--------+--------+--------+
|      Length     |     Checksum    |
+--------+--------+--------+--------+
|
|        data octets ...
+--------------- ...

UDP Pseudo Header
 0      7 8     15 16    23 24    31 
+--------+--------+--------+--------+
|           source address          |
+--------+--------+--------+--------+
|        destination address        |
+--------+--------+--------+--------+
|  zero  |protocol|   UDP length    |
+--------+--------+--------+--------+

IP Header
 0      7 8     15 16    23 24    31
+--------+--------+--------+--------+
|Ver.|IHL|DSCP|ECN|   Total length  |
+--------+--------+--------+--------+
|  Identification |Flags|   Offset  |
+--------+--------+--------+--------+
|   TTL  |Protocol| Header Checksum |
+--------+--------+--------+--------+
|         Source IP address         |
+--------+--------+--------+--------+
|       Destination IP address      |
+--------+--------+--------+--------+
'''

import socket
import struct
import pprint
import random

VERSION_OFF     = 0
IHL_OFF         = VERSION_OFF
DSCP_OFF        = IHL_OFF + 1
ECN_OFF         = DSCP_OFF
LENGTH_OFF      = DSCP_OFF + 1
ID_OFF          = LENGTH_OFF + 2
FLAGS_OFF       = ID_OFF + 2
OFF_OFF         = FLAGS_OFF
TTL_OFF         = OFF_OFF + 2
PROTOCOL_OFF    = TTL_OFF + 1
IP_CHECKSUM_OFF = PROTOCOL_OFF + 1
SRC_IP_OFF      = IP_CHECKSUM_OFF + 2
DEST_IP_OFF     = SRC_IP_OFF + 4
SRC_PORT_OFF    = DEST_IP_OFF + 4
DEST_PORT_OFF   = SRC_PORT_OFF + 2
UDP_LEN_OFF     = DEST_PORT_OFF + 2
UDP_CHECKSUM_OFF= UDP_LEN_OFF + 2
DATA_OFF        = UDP_CHECKSUM_OFF + 2

IP_PACKET_OFF   = VERSION_OFF
UDP_PACKET_OFF  = SRC_PORT_OFF

def parse(data):
    packet = {}
    packet['version']       = data[VERSION_OFF] >> 4
    packet['IHL']           = data[IHL_OFF] & 0x0F
    packet['DSCP']          = data[DSCP_OFF] >> 2
    packet['ECN']           = data[ECN_OFF] & 0x03
    packet['length']        = (data[LENGTH_OFF] << 8) + data[LENGTH_OFF + 1]
    packet['Identification']= (data[ID_OFF] << 8) + data[ID_OFF + 1]
    packet['Flags']         = data[FLAGS_OFF] >> 5
    packet['Offset']        = ((data[OFF_OFF] & 0b11111) << 8) + data[OFF_OFF + 1]
    packet['TTL']           = data[TTL_OFF]
    packet['Protocol']      = data[PROTOCOL_OFF]
    packet['Checksum']      = (data[IP_CHECKSUM_OFF] << 8) + data[IP_CHECKSUM_OFF + 1]
    packet['src_ip']        = '.'.join(map(str, [data[x] for x in range(SRC_IP_OFF, SRC_IP_OFF + 4)]))
    packet['dest_ip']       = '.'.join(map(str, [data[x] for x in range(DEST_IP_OFF, DEST_IP_OFF + 4)]))
    packet['src_port']      = (data[SRC_PORT_OFF] << 8) + data[SRC_PORT_OFF + 1]
    packet['dest_port']     = (data[DEST_PORT_OFF] << 8) + data[DEST_PORT_OFF + 1]
    packet['udp_length']    = (data[UDP_LEN_OFF] << 8) + data[UDP_LEN_OFF + 1]
    packet['UDP_checksum']  = (data[UDP_CHECKSUM_OFF] << 8) + data[UDP_CHECKSUM_OFF + 1]
    packet['data']          = ''.join(map(chr, [data[DATA_OFF + x] for x in range(0, packet['udp_length'] - 8)]))

    return packet

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

def mensagem(tipo, identificador):
    return bytes([tipo, identificador >> 8, identificador & 0xFF])

def udp_send(data, dest_addr, src_addr=('192.168.1.41', 35869)):
    #Generate pseudo header
    src_ip, dest_ip = ip2int(src_addr[0]), ip2int(dest_addr[0])
    src_ip = struct.pack('!4B', *src_ip)
    dest_ip = struct.pack('!4B', *dest_ip)

    zero = 0

    protocol = socket.IPPROTO_UDP 

    #Check the type of data
    try:
        data = data.encode()
    except AttributeError:
        pass

    src_port = src_addr[1]
    dest_port = dest_addr[1]

    data_len = len(data)
    
    udp_length = 8 + data_len

    checksum = 0
    pseudo_header = struct.pack('!BBH', zero, protocol, udp_length)
    pseudo_header = src_ip + dest_ip + pseudo_header
    udp_header = struct.pack('!4H', src_port, dest_port, udp_length, checksum)
    checksum = checksum_func(pseudo_header + udp_header + data)
    udp_header = struct.pack('!4H', src_port, dest_port, udp_length, checksum)
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP) as s:
        s.sendto(udp_header + data, dest_addr)
        response, server_address = s.recvfrom(1024)
        exibir_resposta(response[28:])


def checksum_func(data):
    checksum = 0
    data_len = len(data)
    if (data_len % 2):
        data_len += 1
        data += struct.pack('!B', 0)
    
    for i in range(0, data_len, 2):
        w = (data[i] << 8) + (data[i + 1])
        checksum += w

    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = ~checksum & 0xFFFF
    return checksum

def ip2int(ip_addr):
    if ip_addr == 'localhost':
        ip_addr = '127.0.0.1'
    return [int(x) for x in ip_addr.split('.')]

def udp_recv(addr, size):
    zero = 0
    protocol = 17
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP) as s:
        s.bind(addr)
        while True:
            data, src_addr = s.recvfrom(size)
            packet = parse(data)
            ip_addr = struct.pack('!8B', *[data[x] for x in range(SRC_IP_OFF, SRC_IP_OFF + 8)])
            udp_psuedo = struct.pack('!BB5H', zero, protocol, packet['udp_length'], packet['src_port'], packet['dest_port'], packet['udp_length'], 0)
            
            verify = verify_checksum(ip_addr + udp_psuedo + packet['data'].encode(), packet['UDP_checksum'])
            if verify == 0xFFFF:
                print(packet['data'])
            else:
                print('Checksum Error!Packet is discarded')

def verify_checksum(data, checksum):
    data_len = len(data)
    if (data_len % 2) == 1:
        data_len += 1
        data += struct.pack('!B', 0)
    
    for i in range(0, data_len, 2):
        w = (data[i] << 8) + (data[i + 1])
        checksum += w
        checksum = (checksum >> 16) + (checksum & 0xFFFF)

    return checksum

if __name__ == '__main__':
    while True:
        print("\nEscolha uma opção:")
        print("1. Data e hora atual")
        print("2. Mensagem motivacional para o fim do semestre")
        print("3. Quantidade de respostas emitidas pelo servidor")
        print("4. Sair")
        escolha = int(input("Opção: "))
    
        if escolha == 4:
            break
    
    # Gerar identificador aleatório entre 1 e 65535
        identificador = random.randint(1, 65535)  
        payload = mensagem(escolha - 1, identificador)

        udp_send(payload,('15.228.191.109', 50000)) 
