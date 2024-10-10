import socket
import threading
import random

# Estado do jogo
jogadores = {} #armazena as informacoes dos jogadores (pontuacao, estado de conexao)
numero_para_adivinhar = 0 #eh o numero que devem adivinhar
jogo_comecou = False #se o jogo ja comecou
lock = threading.Lock() #para garantir que multiplas threads possam acessar variaveis globais

#Funcao para lidar com as interacoes do cliente, cada cliente sera tratado em uma thread separada
def recebe_cliente(socket_do_cliente, addr):
    global numero_para_adivinhar, jogo_comecou

    with socket_do_cliente:
        nome_do_jogador = f"Jogador_{addr[1]}" #define um nome ao cliente/jogador
        jogadores[nome_do_jogador] = {"score": 0, "connected": True} #dá uma pontuacao e um status ao jogador
        socket_do_cliente.sendall("Bem-vindo ao Jogo de Adivinhação!\n".encode())

        while True:
            try:
                #recebe solicitacao do cliente
                requisicao = socket_do_cliente.recv(1024).decode().strip() #requisicao = recebe um pacote de ate 1024 bytes, decodifica transformando em uma string e strip() remove espaços
                if not requisicao:
                    break #se receber uma mensagem vazia, encerra conexao
                print(f"Recebido de {nome_do_jogador}: {requisicao}")

                #processa o comando do cliente e devolve uma reposta
                resposta = processa_requisicao(requisicao, nome_do_jogador)
                socket_do_cliente.sendall(resposta.encode())
            except:
                break #caso aconteça algum erro, saímos do loop

#processa o comando
def processa_requisicao(requisicao, nome_do_jogador):
    global numero_para_adivinhar, jogo_comecou

    #essa parte separa a requisicao recebida (ex: usuario digita "GUESS 42", pedido = ["GUESS", "42"])
    pedido = requisicao.split(' ') 
    comando = pedido[0].upper() #pega a primeira parte do comando: comando = "GUESS"

    if comando == "START":
        return inicia_jogo() #inicia um jogo
    elif comando == "GUESS": #se o cliente fez uma adivinhacao
        if len(pedido) > 1:
            guess = int(pedido[1]) # guess = "42"
            return adivinha_numero(nome_do_jogador, guess)
        return "Erro: Forneça um número para adivinhar!" #caso usuario digite "GUESS " (sem um chute)
    elif comando == "SCORE":
        return pontuacao(nome_do_jogador)
    elif comando == "END":
        return finalizar_jogo()
    else:
        return "Comando inválido!"

def inicia_jogo():
    global numero_para_adivinhar, jogo_comecou
    with lock:
        if jogo_comecou:
            return "Jogo já iniciado!"
        numero_para_adivinhar = random.randint(1, 100) #gera um numero aleatorio para adivinhar
        jogo_comecou = True
       # print(f"Novo número gerado: {numero_para_adivinhar}") mano pq q isso aqui ta no codigo preciso rodar pra ver
        return "START: Jogo iniciado! Adivinhe um número entre 1 e 100."

def adivinha_numero(nome_do_jogador, guess):
    global numero_para_adivinhar
    if not jogo_comecou:
        return "Erro: O jogo ainda não começou! Use START."

    if guess < numero_para_adivinhar:
        return "resposta: Seu palpite é muito baixo."
    elif guess > numero_para_adivinhar:
        return "resposta: Seu palpite é muito alto."
    else: #ideia: acho que a gente poderia variar a pontuacao, se acertar de primeira dá 10 pontos, e vai diminuindo conforme as tentativas
        jogadores[nome_do_jogador]["score"] += 1 #queria mudar a variavel score pra pontuacao :(
        return f"resposta: Correto! {nome_do_jogador} ganhou 1 ponto."

def pontuacao(nome_do_jogador):
    score = jogadores[nome_do_jogador]["score"]
    return f"SCORE: Sua pontuação é {score}."

def finalizar_jogo():
    global jogo_comecou
    with lock:
        if not jogo_comecou:
            return "Erro: O jogo ainda não começou!"
        jogo_comecou = False

    scores = "\n".join([f"{player}: {data['score']} pontos" for player, data in jogadores.items()])
    return f"END: Jogo encerrado!\nPontuações finais:\n{scores}"

def start_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor de Adivinhação rodando em {host}:{port}...")

    while True:
        socket_do_cliente, addr = server_socket.accept()
        print(f"Conexão de {addr}")
        client_handler = threading.Thread(target=recebe_cliente, args=(socket_do_cliente, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()
