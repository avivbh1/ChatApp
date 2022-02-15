"""error ud msg"""
unrecognized_error_msg_id = 0

"""new client want to join the server """
new_client_msg_id = 1
new_client_msg_context = "welcome to the server"


""" existing cline want to join the chat"""
existing_client_msg_id = 2
existing_client_msg_context = "welocme back to the server"


" announce to client he entered invalid username "
invalid_username_msg_id = 3

""" announce to client he entered invalid password """
invalid_password_msg_id = 4


""" announce to client that his username is already taken """
username_is_taken_msg_id = 5


""" announce to client his username is not in data base """
username_not_in_data_base_msg_id = 6


""" password doesnt match the username """
password_not_match_username_msg_id = 7


""" successful sign up message """
successful_sign_up_msg_id = 200


""" telling the user that he logged in successfully """
successful_log_in_msg_id = 201


""" client sent a message to all other client """
client_group_message_msg_id = 300


""" group announcement from server """
admin_announcement_msg_id = 301


""" servers are off """
server_is_off_msg_id = 500


""" client disconnected """
client_disconnected_msg_id = 600

""" sending messages in order to keep connection alive and know when connection is off"""
health_check_msg_id = 400


data_base_path = r"C:\Users\avivb\PycharmProjects\my_whatsapp\server_package\database.txt"