import threading
from server_message import take_apart_msg, Message
import chatApp_constant
from server_security import try_create_new_account, check_existing_account
from set_up_server_socket import *  # setup the socket
from time import sleep


def send_clients_list(client_conn):
    id_msg = chatApp_constant.clients_list_msg_id
    data_msg = ",".join([name for name in conn_and_names.values() if name != ""])  # names separated by comma
    message = Message(id_msg, data_msg)
    broadcast(msg=message)
    #client_conn.send(str(message).encode())


def send_error_message(client_conn):
    """
    sending an error message to a specific client
    :param client_conn:
    :return:
    """
    id_msg = chatApp_constant.unrecognized_error_msg_id
    data_msg = ""
    message = Message(id_msg, data_msg)
    client_conn.send(str(message).encode())


def keep_connection_alive(client_conn, client_addr):
    """
    this function gets activate for every client as a thread every time a user connecting to our server
    :param client_addr:
    :param client_conn:
    :return:
    """
    while True:
        try:
            msg = Message(id=chatApp_constant.health_check_msg_id, data="")  # means for staying alive
            client_conn.send(str(msg).encode())
            sleep(5)  # checking any 5 seconds
            print(conn_and_names.keys())  # printing the connections
        except Exception as e:
            break  # killing the thread :)
    print(f"[DISCONNECTED] {client_addr}")
    username_left = remove_user_by_connection(client_conn)
    announce_other_clients_user_disconnected(username_left)
    send_clients_list(client_conn)


def announce_other_clients_user_disconnected(username_left):
    """
    announcing all connected clients, a user disconnected
    :param username_left:
    :return:
    """
    msg_id = chatApp_constant.admin_announcement_msg_id  # announcement of server to everyone
    msg_data = f"Admin,{username_left} just left the chat"
    message = Message(id=msg_id, data=msg_data)
    broadcast(message)


def share_clients_with_client_message(data_msg):
    """
    gets the data to transfer everyone
    :param data:
    :return:
    """
    msg_id = chatApp_constant.admin_announcement_msg_id  # by protocol it means for the clients to display a message on the screen
    message = Message(id=msg_id, data=data_msg)
    broadcast(message)


def remove_user_by_connection(client_conn):
    """
    this function gets the client conn and removing him from the chat for now
    his user in the data base still exits
    :param client_conn:
    :return: username: in order to announce everyone he left the chat
    """
    username = conn_and_names[client_conn]
    conn_and_names[client_conn] = ""  # user now considered as connected but no to chat
    return username


def disconnect_client(client_conn):
    """
    disconnecting the client
    :param client_conn:
    :return: username:
    """
    client_conn.close()


def announce_other_clients_user_connected(deliver_conn, username):
    msg_id = chatApp_constant.admin_announcement_msg_id  # by protocol it means the a client joined the chat
    msg_data = f"Admin,{username} just joined the chat"
    message = Message(msg_id, msg_data)
    broadcast(msg=message, deliver_conn=deliver_conn)


def broadcast(msg, deliver_conn=None):
    """
    gets a message by the protocol and sending it to all the clients in the server
    :param msg:
    :param deliver_conn:
    :param msg:
    :return:
    """
    print(msg)
    print("in broadcast")
    if deliver_conn is None:
        # checking if the deliver connection was passed as an argument.
        # if it didn't passed as an argument we sent it to all of the clients
        for client_conn in conn_and_names.keys():
            try:
                if conn_and_names[client_conn] != "":  # "" means the client got disconnected
                    client_conn.send(str(msg).encode())  # sending str(msg)
            except Exception as e:  # if we're entering the exception, it means the client isnt found on the other side of the socket
                print(e)
                username_left = remove_user_by_connection(client_conn)
                disconnect_client(client_conn)
                announce_other_clients_user_disconnected(username_left=username_left)
                send_clients_list(client_conn)

    elif deliver_conn in conn_and_names.keys():
        # sending the msg to all the clients in the server except the one who sent it
        for client_conn in conn_and_names.keys():
            if client_conn != deliver_conn:
                try:
                    if conn_and_names[client_conn] != "":  # "" means the client isn't in the chat currently
                        client_conn.send(str(msg).encode())  # sending str(msg)
                except Exception as e:
                    print(e)
                    username_left = remove_user_by_connection(client_conn=client_conn)
                    disconnect_client(client_conn)
                    announce_other_clients_user_disconnected(username_left=username_left)
                    send_clients_list(client_conn)


def handle_client(client_conn, client_addr):
    """
    takes the message which the client sent and send it to all the other clients
    :param client_addr:
    :param client_conn
    :return:
    """
    while True:
        try:
            receive = client_conn.recv(1024).decode()  # decoding msg after receiving
            """
            now we handle the client by the receive we got as: id|data|data_len
            id
            :param receive:
            :return:
            """
            given_message = take_apart_msg(receive)  # breaking it apart to a form of a dict

            if given_message["id"] == chatApp_constant.new_client_msg_id:  # it means there is a new client who want to join the chat
                response_msg_id = try_create_new_account(client_conn=client_conn, message=given_message)  # this function returns the id message accordingly
                #  try_create_new_account() make sure to do what ever it needs to be done behind the scenes
                if response_msg_id == chatApp_constant.successful_sign_up_msg_id:  # it means the user signed up successfully
                    # now we send all the other clients an announcement the user signed up successfully
                    given_msg_data = given_message["data"]  # 'username,password'
                    deliver_username = given_msg_data.split(",")[0]  # the username of the deliver
                    announce_other_clients_user_connected(deliver_conn=client_conn, username=deliver_username)

                    print(f"[CONNECTED SUCCESSFULLY] {client_addr}")

                    data_msg = f"Admin,welcome to the chat {deliver_username}"

                else:
                    data_msg = ""

                response_message = Message(id=response_msg_id, data=data_msg)  # building the msg to send back to the client
                client_conn.send(str(response_message).encode())  # sending the message correctly
                if response_msg_id == chatApp_constant.successful_sign_up_msg_id:
                    """ sending the list of the clients that are connected currently"""
                    send_clients_list(client_conn=client_conn)

            elif given_message["id"] == chatApp_constant.existing_client_msg_id:  # it means there is a client with an existing account who wants to join the chat
                response_msg_id = check_existing_account(client_conn=client_conn, message=given_message)  # this function returns the id message accordingly
                #  if the account exits, check_existing_account appends the username to the conn_and_names
                if response_msg_id == chatApp_constant.successful_log_in_msg_id:  # means the user logged in successfully
                    # now we announce all the other clients that the user joined the chat
                    given_msg_data = given_message["data"]
                    deliver_username = given_msg_data.split(",")[0]  # the username of the deliver
                    announce_other_clients_user_connected(client_conn, deliver_username)
                    print(f"[CONNECTED SUCCESSFULLY] {client_addr}")
                    response_msg_data = f"Admin,welcome back to the chat {deliver_username}"

                else:
                    print(f"[DIDN'T MANAGE TO CONNECT] {client_addr}")
                    response_msg_data = ""  # if response_msg_id != 201 the data doesnt matter

                message = Message(response_msg_id, response_msg_data)  # building the msg to send back to the client
                client_conn.send(str(message).encode())  # sending the message correctly
                if response_msg_id == chatApp_constant.successful_log_in_msg_id:
                    """ sending the list of the clients that are connected currently"""
                    send_clients_list(client_conn=client_conn)

            elif given_message["id"] == chatApp_constant.client_disconnected_msg_id:
                username_left = remove_user_by_connection(client_conn=client_conn)
                announce_other_clients_user_disconnected(username_left=username_left)
                send_clients_list(client_conn=client_conn)
                # we're not really disconnecting the socket of this client because he just disconnected from a
                # specific user, but didn't closed his client

            elif given_message["id"] == chatApp_constant.client_group_message_msg_id:  # it means a connected user sent a message to send to all the others
                share_clients_with_client_message(given_message["data"])  # the data we got presented like: "username,msg_data"

            elif given_message["id"] == 0:  # unrecognized error
                print(f"[UNRECOGNIZED ID MESSAGE] from {client_addr}")
                send_error_message(client_conn)

        except Exception as e:
            print(e)
            disconnect_client(client_conn)
            print(f"[DISCONNECTED] {client_addr}")
            break


def server_receive():
    """
    this function handle any client that just connected to the chat
    :return:
    """
    while True:
        try:
            client_conn, client_addr = my_socket.accept()  # waiting for a connection from a client
            conn_and_names[client_conn] = ""  # currently this connection has no username because it just got connected
            threading.Thread(target=keep_connection_alive, args=(client_conn, client_addr,), daemon=True).start()
            thread = threading.Thread(target=handle_client, args=(client_conn, client_addr), daemon=True)
            thread.start()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    server_receive()
