import ipaddress
from datetime import datetime
import socket
import random
import logging

SERVER_HOST: str = "0.0.0.0"
CLIENT_HOST: str = "10.81.208.178"
PORT: int = 8080
BUFFER_SIZE: int = 1024
HEADER_LEN: int = 2
FORMAT: str = 'utf-8'
DISCONNECT_MSG: str = "EXIT"

# prepare Log file
LOG_FILE = 'LOG.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def check_cmd(data) -> bool:
    """Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)"""
    data = data.upper()
    return data in ("TIME", "NAME", "RAND", DISCONNECT_MSG)


def create_request_msg(data) -> str:
    """Create a valid protocol message, will be sent by client, with length field"""
    request = ''
    if check_cmd(data):
        request += f"{len(data):02d}{data.upper()}"
    else:
        request = f"{len('Non-supported cmd')}Non-supported cmd"
    return request


def create_response_msg(data) -> str:
    """Create a valid protocol message, will be sent by server, with length field"""
    response = "Non-supported cmd"
    if data == "TIME":
        response = str(datetime.now())
    elif data == "NAME":
        response = socket.gethostname()
    elif data == "RAND":
        response = f"{random.randint(1,1000)}"
    elif data == DISCONNECT_MSG:
        response = "Exit request accepted"

    response = f"{len(response):02d}{response}"
    return response


def receive_msg(my_socket: socket) -> (bool, str):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    str_header = my_socket.recv(HEADER_LEN).decode(FORMAT)
    length = int(str_header)
    if length > 0:
        buf = my_socket.recv(length).decode(FORMAT)
    else:
        return False, "Error"

    return True, buf


def write_to_log(msg):
    logging.info(msg)
    print(msg)
