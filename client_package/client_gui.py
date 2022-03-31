from datetime import datetime
from message import Message
from set_all_windows import *
from client_security import is_password_confirmed, is_field_valid, is_valid_to_send
from client_send import client_send
from set_up_client_socket import open_socket
import chatApp_constant

client_user_and_pass = {"username": "", "password": ""}
current_client_socket = open_socket()


def disconnect_from_server():
    msg_id = chatApp_constant.client_disconnected_msg_id
    msg_data = ""
    msg = Message(msg_id, msg_data)
    client_send(current_client_socket, msg)
    back_to_home_window()


def unplace_clients_list():
    client_list_text.place_forget()
    close_client_list_button.place_forget()
    show_client_list_button.place(x=375, y=5, height=20, width=30)


def activate_clients_list():
    show_client_list_button.place_forget()
    client_list_text.place(x=275, y=10, height=120, width=100)
    close_client_list_button.config(command=unplace_clients_list)
    close_client_list_button.place(x=375, y=5, height=20, width=30)


def activate_close_client_message():
    clean_window()
    close_client_frame.place(x=0, y=100, height=300, width=450)
    server_off_message_label.place(x=-25, y=0, height=300, width=450)


def back_to_home_window():
    chat_text_box.delete(0, 'end')  # clearing chat_text_box
    text_chat.delete("1.0", tk.END)
    clean_window()
    start_home_window()


def kill_client_socket():
    global current_client_socket
    try:
        current_client_socket.close()
    except Exception as e:
        pass
    print("[WE LEFT CHAT]")


def update_clients_list(connected_clients):
    """
    this function gets the connected clients in string, names separated by comma
     and prints it in the text widget of clients list
    :param connected_clients:
    :return:
    """
    output = "online: "
    connected_clients = "\n".join(connected_clients.split(","))
    output += connected_clients

    client_list_text.config(state=tk.NORMAL)
    client_list_text.delete('1.0', tk.END)
    client_list_text.insert(tk.END, output)
    client_list_text.config(state=tk.DISABLED)


def update_text_screen(data):
    deliver_name, context = data.split(",")[0], data.split(",")[1]
    if deliver_name == client_user_and_pass["username"]:
        deliver_name = "You"

    now = datetime.now()
    current_time = now.strftime("[%H:%M:%S]")

    output = f"{deliver_name}: {context}  {current_time}"

    text_chat.config(state=tk.NORMAL)
    text_chat.insert(tk.INSERT, f"{output}\n")

    text_chat.config(state=tk.DISABLED)


def start_chat_window():
    """ chat window """
    clean_window()
    text_chat.config(state=tk.NORMAL)
    text_chat.delete("1.0", "end")
    text_chat.config(state=tk.DISABLED)
    text_chat.place(x=5, y=6, height=350, width=400)
    chat_text_box.place(x=6, y=360, height=35, width=300)
    client_name_label.config(text=client_user_and_pass["username"])
    client_name_label.place(x=-5, y=400, height=20, width=120)

    show_client_list_button.config(command=activate_clients_list)
    show_client_list_button.place(x=375, y=5, height=20, width=30)

    chat_send_button.config(command=build_chat_message)
    chat_send_button.place(x=320, y=360, height=35, width=83)
    return_button.config(state=tk.NORMAL, command=disconnect_from_server)

    credits_label.place(x=100, y=495, height=20, width=200)
    logo_label.place(x=148, y=470, height=22, width=100)
    return_button.place(x=370, y=485, height=20, width=25)


def activate_server_off():
    back_to_home_window()
    server_off_message_label.place(x=25, y=430, height=30, width=450)


def clean_window():
    """ cleaning the window in order to make place for the other pages"""
    for widget in window.winfo_children():
        if type(widget) is tk.Entry:
            widget.delete(0, "end")
        widget.place_forget()


def start_home_window():
    def start_log_in_window():
        """ log in window """
        clean_window()
        username_label.place(x=18, y=182, height=13, width=100)
        username_text_box.place(x=25, y=200, height=40, width=350)

        password_label.place(x=18, y=244, height=13, width=100)
        password_text_box.place(x=25, y=260, height=40, width=350)

        try_log_in_button.config(command=build_request_to_login)
        try_log_in_button.place(x=150, y=320, height=40, width=100)

        return_button.config(command=start_home_window, state=tk.NORMAL)

        credits_label.place(x=100, y=495, height=20, width=200)
        logo_label.place(x=148, y=470, height=22, width=100)
        return_button.place(x=370, y=485, height=20, width=25)

    def start_sign_up_window():
        """ sign up window """
        clean_window()
        username_label.place(x=18, y=182, height=13, width=100)
        new_username_text_box.place(x=25, y=200, height=40, width=350)

        password_label.place(x=18, y=244, height=13, width=100)
        new_password_text_box.place(x=25, y=260, height=40, width=350)

        confirm_new_password_label.place(x=18, y=305, height=13, width=150)
        confirm_new_password_text_box.place(x=25, y=325, height=40, width=350)

        try_sign_up_button.config(command=build_request_to_sign_up)
        try_sign_up_button.place(x=150, y=380, height=40, width=100)

        return_button.config(state=tk.NORMAL, command=back_to_home_window)

        credits_label.place(x=100, y=495, height=20, width=200)
        logo_label.place(x=148, y=470, height=22, width=100)
        return_button.place(x=370, y=485, height=20, width=25)

    """ home window """
    clean_window()
    welcome_label.place(x=-55, y=100, height=100, width=500)

    log_in_button.config(command=start_log_in_window)
    log_in_button.place(x=50, y=250, height=40, width=120)

    sign_up_button.config(command=start_sign_up_window)
    sign_up_button.place(x=225, y=250, height=40, width=120)

    return_button.config(state=tk.DISABLED)

    credits_label.place(x=100, y=495, height=20, width=200)
    logo_label.place(x=148, y=470, height=22, width=100)
    return_button.place(x=370, y=485, height=20, width=25)


def build_request_to_login():
    """
    gets the:
    username field
    password field
    and checks if it is valid (minimal check) to send it to the server and continue the check there
    :return:
    """
    ID = chatApp_constant.existing_client_msg_id  # id=2 means for the server that the message is a request to login
    client_user_and_pass["username"] = username_text_box.get()
    client_user_and_pass["password"] = password_text_box.get()
    if not is_field_valid(client_user_and_pass["username"]):  # no passing more than 15 characters as name/pass
        activate_invalid_username_message()
    elif not is_field_valid(client_user_and_pass["password"]):
        activate_invalid_password_message()
    elif len(client_user_and_pass["password"]) <= 0:
        activate_invalid_password_message()
    else:
        data_of_message = f"""{client_user_and_pass["username"]},{client_user_and_pass["password"]}"""  # the server gets the username and the password separated by comma
        current_msg = Message(ID, data_of_message)  #
        print("[LOGIN REQUEST WAS SENT]")  #
        print(current_client_socket)
        client_send(current_client_socket, current_msg)


def build_chat_message():
    """
    gets the:
    message field
    and checks if it is valid (minimal check) to send it to the server and continue the check there
    :return:
    """
    global current_client_socket
    ID = chatApp_constant.client_group_message_msg_id  # send msg to all the other clients on the server
    context = chat_text_box.get()  # data of msg
    if not is_valid_to_send(context):
        activate_invalid_context_message()
    else:
        clean_window_from_error_messages()  # if we managed to send a message we need to clear error messages
        chat_text_box.delete(0, 'end')  # cleaning the entry
        deliver_name = client_user_and_pass["username"]
        data_of_message = f"{deliver_name},{context}"
        current_msg = Message(ID, data_of_message)
        print("[CHAT MESSAGE WAS SENT]")
        client_send(current_client_socket, current_msg)


def build_request_to_sign_up():
    """
    gets the:
    username field
    password field
    confirm password field
    and checks if it is valid (minimal check) to send it to the server and continue the check there
    :return:
    """
    ID = chatApp_constant.new_client_msg_id  # id = 1 means for the server that the message is a request to sign up
    client_user_and_pass["username"] = new_username_text_box.get()
    client_user_and_pass["password"] = new_password_text_box.get()
    confirm_password = confirm_new_password_text_box.get()
    if not is_field_valid(client_user_and_pass["username"]):  # no passing more than 15 characters as name/pass
        activate_invalid_username_message()
    elif not is_field_valid(client_user_and_pass["password"]):
        activate_invalid_password_message()
    elif not is_password_confirmed(client_user_and_pass["password"], confirm_password):
        activate_wrong_confirmed_password_message()  # password isn't confirmed
    else:
        data_of_message = f"""{client_user_and_pass["username"]},{client_user_and_pass["password"]}"""  # the server gets the username and the password separated by comma
        current_msg = Message(ID, data_of_message)
        print("[SIGN UP REQUEST WAS SENT]")
        client_send(current_client_socket, current_msg)  # sending the msg by the protocol
