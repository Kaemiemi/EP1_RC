import socket

def start_client(host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print("Conectado ao servidor de adivinhação.")
    print("Comandos disponíveis: PROTO-START, PROTO-GUESS <número>, PROTO-SCORE, PROTO-END")

    try:
        while True:
            command = input("> ")
            if not command:
                continue

            client_socket.sendall(command.encode())
            response = client_socket.recv(1024).decode()
            print(f"Servidor: {response}")
    except KeyboardInterrupt:
        print("\nFechando conexão.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
