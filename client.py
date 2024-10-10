import socket

def start_client(host='localhost', port=12345):
    socket_do_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_do_cliente.connect((host, port))

    print("Conectado ao servidor de adivinhação.")
    print("Comandos disponíveis: PROTO-START, PROTO-GUESS <número>, PROTO-SCORE, PROTO-END")

    try:
        while True:
            comando = input("> ")
            if not comando:
                continue

            socket_do_cliente.sendall(comando.encode())
            resposta = socket_do_cliente.recv(1024).decode()
            print(f"Servidor: {resposta}")
    except KeyboardInterrupt:
        print("\nFechando conexão.")
    finally:
        socket_do_cliente.close()

if __name__ == "__main__":
    start_client()
