# Cliente UDP de Requisições

Este é um cliente implementado em Python utilizando sockets UDP para se comunicar com um servidor. Ele permite que os usuários façam solicitações a um servidor remoto para obter informações como data e hora atual, mensagens motivacionais para o fim do semestre e a quantidade de respostas emitidas pelo servidor até o momento.

## Pré-requisitos

Certifique-se de ter Python 3 instalado em seu sistema.

## Como Usar

1. Clone este repositório em sua máquina local:

    ```
    git clone https://github.com/Henrique-Andrade-Franca/Projeto-Redes-de-Comp.git
    ```

2. Navegue até o diretório clonado:

    ```
    cd Projeto-Redes-de-Comp
    ```

3. Execute o programa cliente:

    ```
    python cliente_UDP.py
    ```

4. O cliente solicitará ao usuário a escolha de uma das opções de requisição disponíveis:

    1. Data e hora atual.
    2. Uma mensagem motivacional para o fim do semestre.
    3. A quantidade de respostas emitidas pelo servidor até o momento.
    4. Sair.

5. Após selecionar uma opção, o cliente enviará a requisição ao servidor e exibirá a resposta recebida de forma legível para o usuário.

6. O programa continuará aguardando novas requisições até que o usuário selecione a opção "Sair".

## Formato de Mensagem

As requisições enviadas pelo cliente e as respostas recebidas pelo servidor seguem o seguinte formato de mensagem:

```
REQ/RES: <req_res>
TIPO: <tipo>
IDENTIFICADOR: <identificador>
TAMANHO DA RESPOSTA: <tamanho>
RESPOSTA: <resposta_bytes>

```

Onde:

1. `<req_res>` é um campo de 4 bits indicando se é uma requisição (REQ) ou resposta (RES).
2. `<tipo>` é um campo de 4 bits indicando o tipo de requisição ou resposta.
3. `<identificador>` é um campo de 16 bits usado para identificar a requisição ou resposta.
4. `<tamanho>` é um campo de 8 bits indicando o tamanho da resposta em bytes.
5. `<resposta_bytes>` são os bytes da resposta, onde cada byte é representado por 8 bits.

## Servidor Remoto

O cliente está configurado para se comunicar com um servidor remoto hospedado no endereço IP `15.228.191.109` na porta `50000`.

## Contribuição

Este projeto está sendo desenvolvido como parte integrante da avaliação da disciplina "Redes de Computadores I", ministrada pelo Professor Fernando Menezes Matos, na Universidade Federal da Paraíba, no curso de graduação de Engenharia da Computação. Os alunos responsáveis pelo desenvolvimento são: Henrique Andrade, Isaac Sebastian e Rodrigo Lanes.
