def encrypt_data(data):
    """
    this encryption works with cypher caesar
    the key is 3
    :param data:
    :return: encrypted data:
    """
    encrypted_data = ""
    key = 3
    for char in data:
        try:
            if 255 >= ord(char) >= 0:
                """
                """
                dec_value = ord(char) + key
                if (dec_value / 255) > 0:
                    dec_value = dec_value % 255
                encrypted_data += chr(dec_value)
            else:
                raise TypeError()
        except TypeError:
            return None  # if we get a typeError we return None
    return encrypted_data


def decrypt_data(data):
    """
    this decryption works with caesar cypher
    the key is 3
    :param data:
    :raise TypeError
    :return: decrypted_data:
    """
    key = 3
    decrypted_data = ""

    for char in data:
        try:
            if 255 >= ord(char) >= 0:
                dec_value = ord(char) - key
                if dec_value < 0:
                    dec_value = 255 - (key % ord(char))
                decrypted_data += chr(dec_value)
            else:
                raise TypeError()
        except TypeError:
            return None  # if we get a typeError we return None
    return decrypted_data
