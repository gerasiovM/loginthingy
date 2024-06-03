import logging

from CProtocol import *


class CClientBL:

    def __init__(self, host: str, port: int):
        self._client_socket: socket.socket = None
        self._host = host
        self._port = port

    def connect(self) -> socket:
        try:
            self._client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self._client_socket.connect((self._host,self._port))
            self._client_socket.setblocking(False)
            write_to_log(f"[CLIENT_BL] {self._client_socket.getsockname()} connected")
            return self._client_socket
        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on connect: {}".format(e))
            return None

    def disconnect(self) -> bool:
        try:
            write_to_log(f"[CLIENT_BL] {self._client_socket.getsockname()} closing")
            self.send_data(CProtocol.DISCONNECT_MSG)
            self._client_socket.close()
            self._client_socket = None
            return True
        except Exception as e:
            # write_to_log("[CLIENT_BL] Exception on disconnect: {}".format(e))
            logging.exception(e)
            return False

    def send_data(self, msg: str) -> bool:
        command, args = (msg.split(">") + [""])[:2]
        used_protocol = check_cmd(command, self._client_socket, [])
        try:
            msg = used_protocol.create_request(command, args)
            message = msg.encode(used_protocol.FORMAT)
            self._client_socket.send(message)
            write_to_log(f"[CLIENT_BL] send {self._client_socket.getsockname()} {msg} ")
            return True
        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on send_data: {}".format(e))
            return False

    def receive_data(self) -> str:
        if not self._client_socket:
            return
        try:
            (bres, msg) = read_buffer(self._client_socket)
            if bres:
                # message = msg.decode(FORMAT)
                write_to_log(f"[CLIENT_BL] received {self._client_socket.getsockname()} {msg} ")
                return msg
        except Exception as e:
            write_to_log("[CLIENT_BL] Exception on receive: {}".format(e))
            return ""
