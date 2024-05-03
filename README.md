# Aplicação Cliente/Servidor UDP e RAW

Este repositório contém a implementação de dois clientes (um utilizando socket UDP e outro utilizando socket RAW) para uma aplicação do tipo cliente/servidor que encaminha requisições para o servidor executando no endereço IP 15.228.191.109 e porta 50000. 

## Requisitos

Para executar os clientes, é necessário ter o Python instalado na máquina.

## Funcionalidades

Os clientes oferecem as seguintes funcionalidades:

1. **Data e Hora Atual**: Solicita ao servidor a data e hora atual.
2. **Mensagem Motivacional para o Fim do Semestre**: Solicita ao servidor uma mensagem motivacional para o fim do semestre.
3. **Quantidade de Respostas Emitidas pelo Servidor**: Solicita ao servidor a quantidade de respostas emitidas até o momento.
4. **Sair**: Encerra a execução do cliente.

## Formato das Mensagens

As mensagens de requisição/resposta seguem o seguinte formato:

- **req/res**: Indicação para mensagem do tipo requisição (bits 0000) ou resposta (bits 0001).
- **tipo**: Indicação do tipo de requisição ou resposta. Bits 0000 para solicitação de data, bits 0001 para solicitação de frase motivacional para o fim do semestre e bits 0010 para quantidade de respostas emitidas pelo servidor. O servidor ainda pode emitir uma resposta com o tipo 0011 para indicar que recebeu uma requisição inválida.
- **identificador**: Número não negativo de 2 bytes determinado pelo cliente. O identificador 0 é reservado para o servidor informar o recebimento de uma requisição inválida.
- **tamanho da resposta**: Campo utilizado apenas em respostas geradas pelo servidor. Indica o tamanho da resposta propriamente ditas, em número de bytes (1 a 255). O tamanho 0 é reservado para quando o servidor envia uma resposta indicando o recebimento de uma requisição inválida.
- **bytes da resposta propriamente dita**: Uma sequência de bytes contendo a resposta solicitada pelo usuário. Caso o servidor esteja informando o recebimento de uma requisição inválida, nenhum byte é encaminhado neste campo.

## Implementação

O repositório contém duas implementações de clientes:

1. **cliente_UDP.py**: Implementação do cliente utilizando socket UDP.
2. **cliente_RAW.py**: Implementação do cliente utilizando socket RAW.

## Execução

Para executar qualquer um dos clientes, basta rodar o arquivo correspondente no terminal. Certifique-se de estar na mesma rede do servidor e de que o servidor esteja em execução.

```bash
python cliente_UDP.py
```

ou

```bash
python cliente_RAW.py
```

## Contribuição

Este projeto está sendo desenvolvido como parte integrante da avaliação da disciplina "Redes de Computadores I", ministrada pelo Professor Fernando Menezes Matos, na Universidade Federal da Paraíba, no curso de graduação de Engenharia da Computação. Os alunos responsáveis pelo desenvolvimento são: Henrique Andrade, Isaac Sebastian e Rodrigo Lanes.
