from handle_client import handle_received_message
from chatApp_constant import server_is_off_msg_id
from message import Message


def client_receive(curr_client_socket):
    """
    receive the message in the form of the protocol: id|data|dataLen
    data -    the data to be transported with the message
    dataLen - the length of the data
    :return:
    """
    while True:
        try:
            if (curr_client_socket.fileno() != -1) or curr_client_socket is not None:
                receive = curr_client_socket.recv(1024).decode()
                print(receive + " in client receive")
                handle_received_message(receive)
            else:
                pass
        except Exception as e:  # means the server on the other side of the socket is not found, so we close the socket
            print(e)
            msg_id = server_is_off_msg_id
            msg_data = ""
            msg = Message(msg_id, msg_data)
            handle_received_message(str(msg))
            break
