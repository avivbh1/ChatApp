def client_send(client_socket, message):
    """
    getting the message and sending it to the server
    :param client_socket:
    :param message:
    :return: None:
    """
    try:
        print(message)
        client_socket.send(str(message).encode())  # sending the msg in the correct form of the protocol
    except Exception as e:
        print(e)
        print("[SERVER DISCONNECTED] client send*")
        client_socket.close()
