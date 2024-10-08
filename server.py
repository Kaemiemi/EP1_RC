import socket
import threading

# Armazenamento de enquetes
polls = {}
poll_id_counter = 1
lock = threading.Lock()

class Poll:
    def __init__(self, poll_id, question):
        self.poll_id = poll_id
        self.question = question
        self.votes = 0

    def vote(self):
        self.votes += 1

    def get_results(self):
        return f"Enquete '{self.question}' tem {self.votes} votos."

def handle_client(client_socket):
    global poll_id_counter
    with client_socket:
        while True:
            try:
                request = client_socket.recv(1024).decode()
                if not request:
                    break
                print(f"Recebido: {request}")

                response = process_request(request)
                client_socket.sendall(response.encode())
            except:
                break

def process_request(request):
    global poll_id_counter
    parts = request.split(' ')
    command = parts[0].upper()

    if command == "CREATE":
        question = ' '.join(parts[1:])
        return create_poll(question)
    elif command == "VOTE":
        poll_id = int(parts[1])
        return vote_poll(poll_id)
    elif command == "LIST":
        return list_polls()
    elif command == "RESULTS":
        poll_id = int(parts[1])
        return poll_results(poll_id)
    else:
        return "Comando inválido!"

def create_poll(question):
    global poll_id_counter
    with lock:
        poll = Poll(poll_id_counter, question)
        polls[poll_id_counter] = poll
        poll_id_counter += 1
    return f"Enquete criada com sucesso! ID: {poll.poll_id}"

def vote_poll(poll_id):
    with lock:
        if poll_id in polls:
            polls[poll_id].vote()
            return f"Voto computado na enquete ID: {poll_id}"
        else:
            return "Enquete não encontrada!"

def list_polls():
    if not polls:
        return "Nenhuma enquete disponível."
    response = "Enquetes disponíveis:\n"
    for poll_id, poll in polls.items():
        response += f"ID {poll_id}: {poll.question}\n"
    return response

def poll_results(poll_id):
    if poll_id in polls:
        return polls[poll_id].get_results()
    else:
        return "Enquete não encontrada!"

def start_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor de enquetes rodando em {host}:{port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexão de {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
