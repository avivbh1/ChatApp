import tkinter as tk

"""
            this file used for all the windows in the application
"""

""" window set up """
window = tk.Tk()
window.geometry("410x520")
window.configure(bg='light blue')
return_button = tk.Button(window, text='>', bg='black', fg='white')
logo_label = tk.Label(text='ChatApp', font=("Times_New_Roman", 15), bg='light blue')
credits_label = tk.Label(window, bg='light blue', text="BY AVIV BEN HAMO", font=("Arial", 10))


""" chat window """
text_chat = tk.Text(window, bg='light green', font=("Arial", 12), state=tk.DISABLED)
chat_text_box = tk.Entry(window, bg="white", font=('Arial', 12))
chat_send_button = tk.Button(window, text="SEND", bg='white')


""" log in window """
username_label = tk.Label(window, text="Username:", bg="light blue", font=("Arial", 12))
password_label = tk.Label(window, text="Password:", bg="light blue", font=("Arial", 12))
username_text_box = tk.Entry(window, bg='white', font=("Arial", 14))
password_text_box = tk.Entry(window, bg='white', font=("Arial", 14), show="*")
try_log_in_button = tk.Button(window, bg='white', text='log in', font=("Arial", 14))

invalid_password_message = "make sure your password is valid"

invalid_password_label = tk.Label(window, text=invalid_password_message, fg='red', bg='light blue', font=("Arial", 10))


""" sign up window """
new_username_text_box = tk.Entry(window, bg='white', font=("Arial", 14))
new_password_text_box = tk.Entry(window, bg='white', font=("Arial", 14), show="*")
confirm_new_password_text_box = tk.Entry(window, bg= 'white', font=("Arial", 14), show="*")
try_sign_up_button = tk.Button(window, bg='white', text='sign up', font=("Arial", 12))

confirm_new_password_label = tk.Label(window, text="Confirm password:", bg="light blue", font=("Arial", 12))

un_confirmed_pass = "make sure your confirm password matches the password"
wrong_confirmed_password_label = tk.Label(window, text=un_confirmed_pass, fg='red', bg='light blue', font=("Arial", 10))

invalid_username_message = "make sure your username is valid"
invalid_username_label = tk.Label(window, text=invalid_username_message, fg='red', bg='light blue',font=("Arial",10))

invalid_context_message = "make sure your context is between 1 - 80 characters"
invalid_context_message_label = tk.Label(window, text=invalid_context_message, fg='red', bg='light blue', font=("Arial", 10))

username_is_taken_message = "username is already taken"
username_is_taken_label = tk.Label(window, text=username_is_taken_message, fg='red', bg='light blue',font=("Arial",10))

username_is_not_in_data_base_message = "username isn't exists, make sure you're writing it correctly"
username_is_not_in_data_base_label = tk.Label(window, text=username_is_not_in_data_base_message, fg='red', bg='light blue', font=("Arial", 10))

pass_not_match_username_label = tk.Label(window, text="password isn't matches the username", fg='red', bg='light blue', font=("Arial", 10))

username_not_in_data_base_label = tk.Label(window, text="username isn't exists", fg='red', bg='light blue', font=("Arial", 10))


client_name_label = tk.Label(window, fg='black', bg='light blue', font=("Arial", 13))

correct_username = """
    username must contain:
     - ascii values only
     - first letter as upper case letter
     - at least one lower case letter
    - length of 5 - 15 characters
    """

correct_username_instructions_message_label = tk.Label(window, text=correct_username, fg='red', bg='light blue', font=("Arial", 10))

correct_password = """
    password must contain:
     - ascii values only
     - at least one letter as upper case letter
     - at least one lower case letter
    - length of 5 - 15 characters 
     - one digit at least
    """

correct_password_instructions_message_label = tk.Label(window, text=correct_username, fg='red', bg='light blue', font=("Arial", 10))


client_list_text = tk.Text(window, bg='light blue', font=("Arial", 8), state=tk.DISABLED)
show_client_list_button = tk.Button(window, bg='white', text='users')
close_client_list_button = tk.Button(window, bg="white", text='close')


""" welcome window """
log_in_button = tk.Button(window, text='log in', bg='white', font=("Arial", 14))
sign_up_button = tk.Button(window, text='sign up', bg='white', font=("Arial", 14))
welcome_text = "welcome to ChatApp\nlogin to your account or sign up for free\nand start chatting"
welcome_label = tk.Label(window, text=welcome_text, font=("Arial", 15), bg='light blue')

close_client_frame = tk.Frame(window, bg='light blue')
close_client_msg = "SERVERS ARE OFF\nmake sure to be back soon"
server_off_message_label = tk.Label(close_client_frame, text=close_client_msg, fg='red', bg='light blue', font=("Arial", 15))


def clean_window_from_error_messages():
    """
    making sure to clean the window from error messages
    """
    wrong_confirmed_password_label.place_forget()
    invalid_password_label.place_forget()
    invalid_username_label.place_forget()
    username_is_taken_label.place_forget()
    username_is_not_in_data_base_label.place_forget()
    correct_username_instructions_message_label.place_forget()
    correct_password_instructions_message_label.place_forget()
    pass_not_match_username_label.place_forget()
    username_is_not_in_data_base_label.place_forget()
    server_off_message_label.place_forget()
    close_client_frame.place_forget()
    invalid_context_message_label.place_forget()


def activate_username_is_not_in_data_base_message():
    clean_window_from_error_messages()
    username_is_not_in_data_base_label.place(x=-25, y=430, height=30, width=450)


def activate_username_not_in_data_base_message():
    clean_window_from_error_messages()
    username_is_not_in_data_base_label.place(x=-25, y=430, height=30, width=450)


def activate_pass_not_match_username_message():
    clean_window_from_error_messages()
    pass_not_match_username_label.place(x=-25, y=430, height=30, width=450)


def activate_username_is_taken_message():
    clean_window_from_error_messages()
    username_is_taken_label.place(x=-25, y=430, height=30, width=450)


def activate_invalid_username_message():
    clean_window_from_error_messages()
    invalid_username_label.place(x=-25, y=430, height=30, width=450)
    correct_username_instructions_message_label.place(x=-40, y=10, height=130, width=450)


def activate_invalid_context_message():
    clean_window_from_error_messages()
    invalid_context_message_label.place(x=-40, y=430, height=15, width=450)


def activate_wrong_confirmed_password_message():
    clean_window_from_error_messages()
    wrong_confirmed_password_label.place(x=-25, y=430, height=30, width=450)


def activate_invalid_password_message():
    clean_window_from_error_messages()
    invalid_password_label.place(x=-25, y=430, height=30, width=450)
    correct_password_instructions_message_label.place(x=-40, y=10, height=130, width=450)

