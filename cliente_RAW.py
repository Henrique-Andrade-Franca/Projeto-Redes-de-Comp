import socket
import random
import struct

def enviar_requisicao(socket_raw, tipo, identificador):
    # Cabeçalho UDP: Origem (16 bits), Destino (16 bits), Comprimento (16 bits), Checksum (16 bits)
    udp_header = struct.pack('!HHHH', CLIENT_PORT, SERVER_PORT, 28, 0)  # Comprimento fixo de 8 bytes
    # Formato da mensagem de requisição: req/res (4 bits), tipo (4 bits), identificador (16 bits)
    mensagem = bytes([tipo, identificador >> 28, identificador & 0xFF])
    # Enviar requisição com cabeçalho UDP
    socket_raw.sendto(udp_header + mensagem, (SERVER_IP, SERVER_PORT))

def receber_resposta(socket_raw):
    # Receber resposta do servidor (considerando que o cabeçalho UDP também será recebido)
    dados, _ = socket_raw.recvfrom(1024)
    return dados[28:]  # Ignorar os primeiros 8 bytes do cabeçalho UDP e IP

def exibir_resposta(resposta):
    # Extrair os primeiros 4 bits do 1º byte da resposta, que representam o tipo da resposta (0, 1 ou 2)
    tipo_resposta = resposta[28] & 0b00001111  # Considerando os 28 bytes do cabeçalho UDP e IP
    tamanho_resposta = resposta[28 + 3]  # Considerando o tamanho do cabeçalho UDP e IP

    # Verificar se o tamanho da resposta corresponde ao valor especificado no cabeçalho
    if len(resposta) != tamanho_resposta + 28:  # Adicionando o tamanho do cabeçalho UDP
        print("\nResposta do servidor: ", resposta)
        print("Tipo da resposta: ", tipo_resposta)
        print("Tamanho da resposta: ", tamanho_resposta)
        print("\nErro: Tamanho da resposta incorreto")
        return

    # Exibir a resposta de acordo com o tipo
    if tipo_resposta == 0:
        print("Data e hora atual:", str(resposta[8 + 4:8 + 4 + tamanho_resposta], 'latin-1'))
    elif tipo_resposta == 1:
        print("Mensagem motivacional:", str(resposta[8 + 4:8 + 4 + tamanho_resposta], 'latin-1'))
    elif tipo_resposta == 2:
        print("Quantidade de respostas emitidas pelo servidor:", int.from_bytes(resposta[8 + 4:8 + 4 + tamanho_resposta], byteorder='big'))

# Endereço IP e porta do servidor
SERVER_IP = '15.228.191.109'
SERVER_PORT = 50000
# Porta do cliente para enviar requisições
CLIENT_PORT = 50001  # Valor arbitrário

# Criar socket RAW
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

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
        enviar_requisicao(cliente_socket, escolha - 1, identificador)
        resposta = receber_resposta(cliente_socket)
        exibir_resposta(resposta)
    else:
        print("Opção inválida. Tente novamente.")

# Fechar o socket
cliente_socket.close()
