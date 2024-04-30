import socket

# Obtém o nome do host
hostname = socket.gethostname()

# Obtém o endereço IP associado ao nome do host
ip_address = socket.gethostbyname(hostname)

print("Nome do host:", hostname)
print("Endereço IP:", ip_address)
