
class Message:
    """
    our protocol to tansport data will be like this:

                Id|Data|DataLen
    """
    def __init__(self, id, data):
        self._id = id
        self._data = data
        self._data_len = len(data)
        self.output = f"{self.id}|{self.data}|{self.data_len}"

    @property
    def id(self):
        return self._id

    @property
    def data(self):
        return self._data

    @property
    def data_len(self):
        return self._data_len

    def __str__(self):
        return f"{self.id}|{self.data}|{self.data_len}"


def take_apart_msg(msg_to_take_apart):
    """
    this function can take apart the message in the form of the protocol, spliited by their fields,
    also it can handle message objects and split them correctly by the fields.
    this function gets the message and returns a dict with the attributes of the message which are:
        (id,data,data_len)
    :param msg_to_take_apart:
    :return: message_dict
    """
    splitted_msg = str(msg_to_take_apart).split("|")
    message_dict = {"id": int(splitted_msg[0]), "data": splitted_msg[1], "data length": int(splitted_msg[2])}
    return message_dict
