from set_up_server_socket import conn_and_names
import chatApp_constant
import sqlite3
import encryption


def initialize_db():
    """
        creating the data base file so it will be 'remembered' and created
    """
    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE accounts (
        username text,
        password text
        )""")
    conn.commit()
    conn.close()


def form_username_and_password(receive):
    """
    this function gets the username and the password seperated by comma : username,password
    :param receive:
    :return: {"username":username, "password":password}
    """
    username, password = receive.split(",")[0], receive.split(",")[1]
    username_and_password_dict = {"username": username, "password": password}
    return username_and_password_dict


def is_password_valid(password):
    """
    password must contain:
     - letters only
     - at least one upper case letter
     - at least one lower case letter
    - length of 5 characters at least
     - one digit at least
    :param password:
    :return:
    """
    upper_letter = 0
    lower_letter = 0
    digit = 0
    if len(password) < 5:
        return False
    for char in password:
        if not ((65 <= ord(char) <= 90) or (97 <= ord(char) <= 122) or (48 <= ord(char) <= 57)):  # not letter or digit
            return False
        elif char.isupper():
            upper_letter += 1
        elif char.islower():
            lower_letter += 1
        elif char.isdigit():
            digit += 1
    if upper_letter >= 1 and lower_letter >= 1 and digit >= 1:
        return True
    return False


def is_username_valid(username):
    """
    username must contain:
     - letters only
     - first letter in upper case
     - one letter in lower case
     - 5 characters long at least
    :return:
    """
    lower_letter = 0
    if len(username) < 5:
        return False
    if not username[0].isupper():
        return False
    for char in username:
        if not ((65 <= ord(char) <= 90) or (97 <= ord(char) <= 122) or (48 <= ord(char) <= 57)):  # not letter or digit
            return False
        elif char.islower():
            lower_letter += 1
    if lower_letter >= 1:
        return True
    return False


def add_connected_user(client_conn, username):
    """
    gets the client connection and the username of this client and adds it the list
    :param username:
    :param client_conn:
    :return:
    """
    conn_and_names[client_conn] = username


def remove_user_from_data_base(username):
    """
    removing the username and his password from the data base
    :param username:
    :return:
    """
    with sqlite3.connect(chatApp_constant.accounts_db_path) as conn:
        cursor = conn.cursor()
        encrypted_username = encryption.encrypt_data(username)
        cursor.execute(f"DELETE * FROM accounts WHERE username = '{encrypted_username}'")
        conn.commit()


def get_password_by_user_name(username):
    """
    gets the password by the username from the data base
    in order to check if the password matches the username
    :param username:
    :return:
    """
    with sqlite3.connect(chatApp_constant.accounts_db_path) as conn:

        cursor = conn.cursor()
        encrypted_username = encryption.encrypt_data(username)
        cursor.execute(f"SELECT password FROM accounts WHERE username = '{encrypted_username}'")
        encrypted_password = cursor.fetchone()[0]
        password = encryption.decrypt_data(encrypted_password)
        return password


def is_username_taken(username_to_find):
    """
    checking if the given username is found in the data base
    :param username_to_find:
    :return:
    """
    with sqlite3.connect(chatApp_constant.accounts_db_path) as conn:

        cursor = conn.cursor()

        cursor.execute("SELECT username FROM accounts")

        usernames = cursor.fetchall()
        for temp_username in usernames:  # the temp_username is in tuple
            if username_to_find == encryption.decrypt_data(temp_username[0]):
                return True
    return False


def check_existing_account(client_conn, message):
    """
    this function gets the message data which is the username and the password
    and checks if it is matches to an existing account
    :param message:
    :param client_conn:
    :return:
    """
    message_data = message["data"]
    ret_msg_id = 0  # unrecognized error
    user_and_pass = form_username_and_password(message_data)  # we gets it in the form of a dict

    if user_and_pass["username"] == "Admin" and user_and_pass["password"] == "Admin":
        return chatApp_constant.successful_log_in_msg_id  # admin joined the chat

    elif not is_username_valid(user_and_pass["username"]):
        ret_msg_id = chatApp_constant.invalid_username_msg_id # by protocol it means the username isn't valid

    elif not is_password_valid(user_and_pass["password"]):
        ret_msg_id = chatApp_constant.invalid_password_msg_id  # by protocol it means the password isn't valid

    elif not is_username_taken(user_and_pass["username"]):
        ret_msg_id = chatApp_constant.username_not_in_data_base_msg_id  # means username is not in data base

    elif is_username_taken(user_and_pass["username"]):  # username in data base
        might_be_password = get_password_by_user_name(user_and_pass["username"])
        if (might_be_password is None) or (user_and_pass["password"] != might_be_password):
            ret_msg_id = chatApp_constant.password_not_match_username_msg_id  # password isn't matches the username
        elif user_and_pass["password"] == might_be_password:  # the username exists and the password matches the password in the data base
            ret_msg_id = chatApp_constant.successful_log_in_msg_id  # user logged in successfully
            add_connected_user(client_conn=client_conn, username=user_and_pass["username"])

    return ret_msg_id


def try_create_new_account(client_conn, message):
    """
    gets the message in the form of a dict {"id":id, "data":data, "data length":dataLen}
    and trying create a new account by making sure everything is valid
    :param client_conn:
    :param message:
    :return:
    """
    user_and_pass = form_username_and_password(message["data"])  # we gets it in the form of a dict
    if not is_username_valid(user_and_pass["username"]):
        ret_msg_id = chatApp_constant.invalid_username_msg_id  # by protocol it means the username isn't valid

    elif is_username_taken(user_and_pass["username"]):
        ret_msg_id = chatApp_constant.username_is_taken_msg_id  # by protocol it means the username is taken

    elif not is_password_valid(user_and_pass["password"]):
        ret_msg_id = chatApp_constant.invalid_password_msg_id  # by protocol it means the password isn't valid

    else:  # it means the username and the password are completely fine and we create a new account in the data base
        insert_data_to_file(user_and_pass["username"], user_and_pass["password"])
        add_connected_user(client_conn=client_conn, username=user_and_pass["username"])
        ret_msg_id = chatApp_constant.successful_sign_up_msg_id  # means everything is fine and the user was created
    return ret_msg_id


def get_number_of_accounts_in_database():
    """
        returns the number of accounts in the data base
    """
    with sqlite3.connect(chatApp_constant.accounts_db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT username FROM accounts")

        return len(cursor.fetchall())


def insert_data_to_file(username, password):
    """
    this functions gets the password and the the username as strings an insert them to the data base
    this function will activate only when a new account was created
    :param username:
    :param password:
    :return: None
    """
    STATIC_NUMBER_OF_ACCOUNTS = get_number_of_accounts_in_database()
    encrypted_username = encryption.encrypt_data(username)
    encrypted_password = encryption.encrypt_data(password)
    with sqlite3.connect(chatApp_constant.accounts_db_path) as conn:
        cursor = conn.cursor()

        cursor.execute(f"INSERT INTO accounts VALUES ('{encrypted_username}' , '{encrypted_password}')")
        conn.commit()
