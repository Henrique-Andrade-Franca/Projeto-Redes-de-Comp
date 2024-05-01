import socket
import struct
import random

# Função para adicionar cabeçalho IP
def add_ip_header(message):
    ip_header = struct.pack('!BBHHHBBH4s4s', 69, 0, 20 + len(message), 0, 0, 64, 17, 0, socket.inet_aton('0.0.0.0'), socket.inet_aton('15.228.191.109'))
    return ip_header + message

# Função para adicionar cabeçalho UDP
def add_udp_header(message):
    udp_header = struct.pack('!HHHH', 1234, 50000, len(message) + 8, 0)
    return udp_header + message

# Função para enviar requisição ao servidor
def enviar_requisicao(request_type, identifier):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

    server_address = ('15.228.191.109', 50000)
    request_message = struct.pack('!BBH', 0, request_type, identifier)
    request_message = add_udp_header(request_message)
    request_message = add_ip_header(request_message)
    
    client_socket.sendto(request_message, server_address)
    response, _ = client_socket.recvfrom(1024)
    
    return response

# Função para formatar e exibir a resposta
def display_response(response):
    ip_header = response[:20]
    udp_header = response[20:28]
    response_data = response[28:]

    tipo_resposta, identifier, response_length = struct.unpack('!BHH', response_data[:5])
    resposta_correta = response_data[5:]

    print("response_data = ", response_data)
    print("resposta_correta = ", resposta_correta)
    print("resposta_lenght = ", response_length)
    print("response = ", response)

    if len(resposta_correta) != response_length:
        print("Erro: Tamanho da resposta incorreto")
        return

    if tipo_resposta == 0:
        print("Data e hora atual:", resposta_correta.decode())
    elif tipo_resposta == 1:
        print("Mensagem motivacional:", resposta_correta.decode())
    elif tipo_resposta == 2:
        print("Quantidade de respostas emitidas pelo servidor:", int.from_bytes(resposta_correta, byteorder='big'))

# Função principal
def main():
    while True:
        print("\nEscolha uma opção:")
        print("1. Data e hora atual")
        print("2. Mensagem motivacional para o fim do semestre")
        print("3. Quantidade de respostas emitidas pelo servidor")
        print("4. Sair")
        
        choice = int(input("Opção: "))
        
        if choice == 4:
            print("Saindo...")
            break
        
        identifier = random.randint(1, 65535)
        
        if choice in (1, 2, 3):
            response = enviar_requisicao(choice - 1, identifier)
            display_response(response)
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
