from datetime import datetime
import random
import socket
from CProtocol import *


class CProtocol26(CProtocol):
    def __init__(self):
        super().__init__()

    def create_request(self, cmd: str, args: str) -> str:
        """Create a valid protocol message, will be sent by client, with length field"""
        request = f"{len(cmd + '>' + args):0{self.HEADER_LEN}}{cmd}"
        return request

    def create_response(self, cmd: str, args: str) -> str:
        """Create a valid protocol message, will be sent by server, with length field"""
        response = "05Error"
        data = cmd.upper()
        if data == "TIME":
            response = str(datetime.now())
        elif data == "NAME":
            response = socket.gethostname()
        elif data == "RAND":
            response = f"{random.randint(1, 1000)}"
        elif data == "EXIT":
            response = "Bye"
        return f"{len(response):0{self.HEADER_LEN}}{response}"

    def get_msg(self, my_socket: socket.socket):
        """Extract message from protocol, without the length field
           If length field does not include a number, returns False, "Error" """

        str_header = my_socket.recv(2).decode()
        write_to_log(f"[Protocol] str_header - {str_header}")
        length = int(str_header)
        write_to_log(f"[Protocol] length - {length}")
        if length > 0:
            buf = my_socket.recv(length).decode()
        else:
            return False, ''
        return True, buf

    @staticmethod
    def check_cmd(data) -> bool:
        """Check if the command is defined in the protocol (e.g. RAND, NAME, TIME, EXIT)"""
        if data.upper() in ("RAND", "NAME", "TIME", "EXIT"):
            return True
        else:
            return False
