import socket
import random
import struct

# Função para anexar o cabeçalho UDP à mensagem
def anexar_cabecalho_udp(mensagem):
    source_port = 12345  # Porta de origem do cliente (pode ser qualquer valor)
    dest_port = 50000  # Porta de destino do servidor
    length = len(mensagem) + 8  # Comprimento total do segmento UDP (tamanho da mensagem + tamanho do cabeçalho UDP)
    checksum = 0  # O cálculo do checksum pode ser ignorado
    
    # Empacotar os campos do cabeçalho UDP
    cabecalho_udp = struct.pack('!HHHH', source_port, dest_port, length, checksum)
    
    # Retornar a mensagem com o cabeçalho UDP anexado
    return cabecalho_udp + mensagem

# Função para anexar o cabeçalho IP à mensagem
def anexar_cabecalho_ip(mensagem):
    version_ihl = 0x45  # Versão do protocolo IP (4) e comprimento do cabeçalho IP (5 palavras de 32 bits)
    dscp_ecn = 0  # Ignorados
    total_length = len(mensagem) + 20  # Comprimento total do datagrama IP (tamanho da mensagem + tamanho do cabeçalho IP)
    identification = random.randint(0, 65535)  # Identificação do datagrama (número aleatório)
    flags_fragment_offset = 0  # Ignorados
    ttl = 64  # Tempo de vida do datagrama IP
    protocol = socket.IPPROTO_UDP  # Protocolo UDP
    checksum = 0  # O cálculo do checksum pode ser ignorado
    source_address = socket.inet_aton('0.0.0.0')  # Endereço de origem do cliente (qualquer valor)
    dest_address = socket.inet_aton('15.228.191.109')  # Endereço de destino do servidor

    # Empacotar os campos do cabeçalho IP
    cabecalho_ip = struct.pack('!BBHHHBBH4s4s', version_ihl, dscp_ecn, total_length, identification, flags_fragment_offset, ttl, protocol, checksum, source_address, dest_address)

    # Retornar o datagrama IP com o cabeçalho IP anexado
    return cabecalho_ip + mensagem

def enviar_requisicao(socket_cliente, tipo, identificador):
    # Formato da mensagem de requisição: req/res (4 bits), tipo (4 bits), identificador (16 bits)
    mensagem = bytes([tipo, identificador >> 8, identificador & 0xFF])

    # Anexar cabeçalhos UDP e IP à mensagem
    mensagem_com_cabecalhos = anexar_cabecalho_udp(mensagem)
    mensagem_com_cabecalhos = anexar_cabecalho_ip(mensagem_com_cabecalhos)

    # Enviar a mensagem ao servidor
    socket_cliente.sendto(mensagem_com_cabecalhos, ('15.228.191.109', 0))  # 0 indica que o SO deve escolher uma porta de origem automaticamente

    # Receber resposta do servidor
    dados, _ = socket_cliente.recvfrom(1024)
    return dados

def exibir_resposta(resposta):
    # extrair os primeiros 4 bits do 1º byte da resposta, que representam o tipo da resposta (0, 1 ou 2)
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

# Criar socket RAW UDP
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
        resposta = enviar_requisicao(cliente_socket, escolha - 1, identificador)
        exibir_resposta(resposta)
    else:
        print("Opção inválida. Tente novamente.")

# Fechar o socket
cliente_socket.close()
