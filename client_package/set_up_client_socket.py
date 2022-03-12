import socket
PORT = 8820
IP = '127.0.0.1'


def open_socket():
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP, PORT))
        return client_socket
    except Exception as e:
        print("[SERVER IS OFF]")
        return None
