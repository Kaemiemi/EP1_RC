import socket
import threading
import random

# Estado do jogo
jogadores = {} #armazena as informacoes dos jogadores (pontuacao, estado de conexao)
number_to_guess = 0 #eh o numero que devem adivinhar
game_started = False #se o jogo ja comecou
lock = threading.Lock() #para garantir que multiplas threads possam acessar variaveis globais

#Funcao para lidar com as interacoes do cliente, cada cliente sera tratado em uma thread separada
def handle_client(client_socket, addr):
    global number_to_guess, game_started

    with client_socket:
        player_name = f"Player_{addr[1]}" #define um nome ao cliente/jogador
        jogadores[player_name] = {"score": 0, "connected": True} #dá uma pontuacao e um status ao jogador
        client_socket.sendall("Bem-vindo ao Jogo de Adivinhação!\n".encode())

        while True:
            try:
                #recebe solicitacao do cliente
                request = client_socket.recv(1024).decode().strip() #request = recebe um pacote de ate 1024 bytes, decodifica tranformando em uma string e strip() remove espaços
                if not request:
                    break #se receber uma mensagem vazia, encerra conexao
                print(f"Recebido de {player_name}: {request}")

                #
                response = process_request(request, player_name)
                client_socket.sendall(response.encode())
            except:
                break

def process_request(request, player_name):
    global number_to_guess, game_started

    parts = request.split(' ')
    command = parts[0].upper()

    if command == "PROTO-START":
        return start_game()
    elif command == "PROTO-GUESS":
        if len(parts) > 1:
            guess = int(parts[1])
            return guess_number(player_name, guess)
        return "Erro: Forneça um número para adivinhar!"
    elif command == "PROTO-SCORE":
        return get_score(player_name)
    elif command == "PROTO-END":
        return end_game()
    else:
        return "Comando inválido!"

def start_game():
    global number_to_guess, game_started
    with lock:
        if game_started:
            return "Jogo já iniciado!"
        number_to_guess = random.randint(1, 100)
        game_started = True
        print(f"Novo número gerado: {number_to_guess}")
        return "PROTO-START: Jogo iniciado! Adivinhe um número entre 1 e 100."

def guess_number(player_name, guess):
    global number_to_guess
    if not game_started:
        return "Erro: O jogo ainda não começou! Use PROTO-START."

    if guess < number_to_guess:
        return "PROTO-RESPONSE: Seu palpite é muito baixo."
    elif guess > number_to_guess:
        return "PROTO-RESPONSE: Seu palpite é muito alto."
    else:
        jogadores[player_name]["score"] += 1
        return f"PROTO-RESPONSE: Correto! {player_name} ganhou 1 ponto."

def get_score(player_name):
    score = jogadores[player_name]["score"]
    return f"PROTO-SCORE: Sua pontuação é {score}."

def end_game():
    global game_started
    with lock:
        if not game_started:
            return "Erro: O jogo ainda não começou!"
        game_started = False

    scores = "\n".join([f"{player}: {data['score']} pontos" for player, data in jogadores.items()])
    return f"PROTO-END: Jogo encerrado!\nPontuações finais:\n{scores}"

def start_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor de Adivinhação rodando em {host}:{port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexão de {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()
