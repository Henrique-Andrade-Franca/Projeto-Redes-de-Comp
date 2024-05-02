"""
Nome: Henrique Andrade
E-mail: henrique.andrade@academico.ufpb.br
Data de Criação: 26/04/2024
Última Atualização: 26/04/2024 - 16:10:55
Linguagem: Python

Descrição: Implementação do cliente (socket UDP)

"""

import socket
import random

def enviar_requisicao(socket_cliente, tipo, identificador):
    # Formato da mensagem de requisição: req/res (4 bits), tipo (4 bits), identificador (16 bits)
    mensagem = bytes([tipo, identificador >> 8, identificador & 0xFF])
    """
      outra alternativa para empacotar os valores de tipo e identificador em uma sequência de bytes
      formato '!BBH' indica que estamos empacotando dois unsigned bytes (B) seguidos por um unsigned
      short integer de 16 bits (H)
      =================================================================================================
      adicionar: import struct
      substituir: mensagem = struct.pack('!BBH', tipo, 0, identificador)  # O segundo byte é reservado
      para possíveis futuras extensões
    """
    socket_cliente.sendto(mensagem, (SERVER_IP, SERVER_PORT))
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

# Endereço IP e porta do servidor
SERVER_IP = '15.228.191.109'
SERVER_PORT = 50000

# Criar socket UDP
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
        resposta = enviar_requisicao(cliente_socket, escolha - 1, identificador)
        exibir_resposta(resposta)
    else:
        print("Opção inválida. Tente novamente.")

# Fechar o socket
cliente_socket.close()
