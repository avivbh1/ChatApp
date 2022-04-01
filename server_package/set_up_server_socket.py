import socket

PORT = 8820
IP = '0.0.0.0'  # this ip works as all ip's
conn_and_names = {}

my_socket = socket.socket()  # setting up the socket
my_socket.bind((IP, PORT))  # binding ip and port
my_socket.listen()  # start waiting for connections
