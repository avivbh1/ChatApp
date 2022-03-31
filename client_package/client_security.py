def is_password_confirmed(password1, password2):
    if password1 == password2:
        return True
    return False


def is_field_valid(field):
    """
    checks if the field given is valid according to the password / username minimal check in client side
    :param field:
    :return:
    """
    if 3 < len(field) <= 15:  # no passing more than 15 characters as name/pass
        return True
    return False


def is_valid_to_send(msg):
    """
    checks if the message is to short or to long to send in the socket
    preventing scoket disconnction
    :param msg:
    :return:
    """
    if 0 < len(msg) <= 80:
        return True
    return False
