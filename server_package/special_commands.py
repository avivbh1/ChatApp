from hashlib import md5
"""
    WE ARE USING MD5 HASHING IN ORDER TO CHECK IF THE STR IS A SPECAIL COMMAND
"""


def is_quit(str):
    """
    were checking if the str we got represents a "quit()" after md5 hash
    :param str:
    :return:
    """
    QUIT = "quit()"
    quit_command = (md5(QUIT.encode())).hexdigest()
    if str == quit_command:
        return True
    return False


def hash_str(str):
    """
    gets a str and returns hashed str
    :param str:
    :return hashed_str:
    """
    return (md5(str.encode())).hexdigest()
