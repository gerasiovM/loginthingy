from abc import ABC, abstractmethod
import socket
import logging

CMD_26 = ("TIME", "NAME", "RAND", "EXIT")
CMD_27 = ("DIR", "DELETE", "COPY", "EXECUTE", "TAKE_SCREENSHOT")
CMD_REG = ("REG", "SIGNIN")
CMD_DB = ''

# prepare Log file
LOG_FILE = 'LOG.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CProtocol(ABC):
    SERVER_HOST: str = "0.0.0.0"
    CLIENT_HOST: str = "127.0.0.1"
    PORT: int = 12345
    BUFFER_SIZE: int = 1024
    HEADER_LEN: int = 4
    FORMAT: str = 'utf-8'
    DISCONNECT_MSG: str = "EXIT"

    def init(self):
        super().__init__()

    @abstractmethod
    def create_request(self, cmd: str, args: str):
        pass

    @abstractmethod
    def create_response(self, cmd: str, args: str):
        pass


def read_buffer(sock: socket.socket) -> (bool, str):
    try:
        str_header = sock.recv(CProtocol.HEADER_LEN).decode(CProtocol.FORMAT)
        length = int(str_header)
        print(length)
        if length > 0:
            buf = sock.recv(length).decode(CProtocol.FORMAT)
        else:
            return False, "Error"
        return True, buf
    except Exception as e:
        return False, "Error"


def check_cmd(data: str, client_socket: socket.socket, callbacks) -> CProtocol:
    from CProtocol26 import CProtocol26
    from CProtocol27 import CProtocol27
    from CProtocolReg import CProtocolReg
    loc_data = data.upper()
    if loc_data in CMD_26:
        return CProtocol26()
    elif loc_data in CMD_27:
        return CProtocol27(client_socket)
    elif loc_data in CMD_REG:
        return CProtocolReg(callbacks)
    else:
        return None


def write_to_log(msg: str):
    print(msg)
    logging.info(msg)
