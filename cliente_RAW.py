import socket
import random

# Função para anexar cabeçalho UDP à mensagem
def adicionar_cabecalho_udp(mensagem, identificador, tamanho_resposta):
    cabecalho = bytearray(8)
    # req/res (4 bits), tipo (4 bits)
    cabecalho[0] = 0b00000000  # Requisição
    cabecalho[1] = 0b00000000  # Tipo: a ser definido
    # Identificador (16 bits)
    cabecalho[2] = (identificador >> 8) & 0xFF
    cabecalho[3] = identificador & 0xFF
    # Tamanho da resposta (8 bits)
    cabecalho[4] = tamanho_resposta
    # Copiar o cabeçalho para a mensagem
    mensagem_com_cabecalho = cabecalho + mensagem
    return mensagem_com_cabecalho

# Endereço IP e porta do servidor
SERVER_IP = '15.228.191.109'
SERVER_PORT = 50000

# Criar socket RAW com protocolo IPPROTO_UDP
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
        
        # Definir o tipo da requisição de acordo com a escolha do usuário
        tipo_requisicao = escolha - 1
        
        # Preparar a mensagem da requisição
        mensagem_requisicao = bytes([tipo_requisicao])
        
        # Adicionar cabeçalho UDP à mensagem
        mensagem_com_cabecalho = adicionar_cabecalho_udp(mensagem_requisicao, identificador, 0)
        
        # Enviar a requisição para o servidor
        cliente_socket.sendto(mensagem_com_cabecalho, (SERVER_IP, SERVER_PORT))
        
        # Receber a resposta do servidor
        resposta, endereco_servidor = cliente_socket.recvfrom(1024)
        
        # Exibir a resposta do servidor
        tipo_resposta = resposta[0] & 0b00001111
        tamanho_resposta = resposta[4]
        print("Resposta do servidor:")
        print("Tipo:", tipo_resposta)
        print("Identificador:", (resposta[2] << 8) + resposta[3])
        print("Tamanho da resposta:", tamanho_resposta)
        print("Resposta propriamente dita:", resposta[8:].decode('utf-8', errors='ignore'))
    else:
        print("Opção inválida. Tente novamente.")

# Fechar o socket
cliente_socket.close()
