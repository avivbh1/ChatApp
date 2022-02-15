from message import take_apart_msg
import chatApp_constant
from client_gui import start_chat_window, update_text_screen, activate_close_client_message
from set_all_windows import activate_invalid_password_message,\
    activate_invalid_username_message, activate_username_is_taken_message, \
    activate_username_not_in_data_base_message, activate_pass_not_match_username_message


def handle_received_message(receive):
    """
        this function gets the receive from
        the server and handle the message according
        to the protocol
    """
    message = take_apart_msg(receive)
    message_id = message["id"]

    if message_id == chatApp_constant.health_check_msg_id:
        pass  # we ignore id=400 because its just a check of the server to see that we still in connection

    elif message_id == chatApp_constant.server_is_off_msg_id:
        activate_close_client_message()

    elif message_id == chatApp_constant.invalid_username_msg_id:  # invalid username
        activate_invalid_username_message()

    elif message_id == chatApp_constant.invalid_password_msg_id:  # invalid password
        activate_invalid_password_message()

    elif message_id == chatApp_constant.username_is_taken_msg_id:  # username is taken
        activate_username_is_taken_message()

    elif message_id == chatApp_constant.username_not_in_data_base_msg_id:
        activate_username_not_in_data_base_message()

    elif message_id == chatApp_constant.password_not_match_username_msg_id:
        activate_pass_not_match_username_message()

    elif message_id == chatApp_constant.successful_sign_up_msg_id:  # user managed to sign up successfully
        start_chat_window()
        update_text_screen(message["data"])

    elif message_id == chatApp_constant.successful_log_in_msg_id:  # user managed to login up successfully
        start_chat_window()
        update_text_screen(message["data"])  # announcing of admin about entering the chat

    elif message_id == chatApp_constant.admin_announcement_msg_id:  # group announcement
        # the msg_data we got is built in the form of "name,announcement..."
        update_text_screen(message["data"])

    else:
        print("[UNRECOGNIZED ID MESSAGE]")
