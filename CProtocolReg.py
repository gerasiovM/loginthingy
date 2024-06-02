from CProtocol import *


class CProtocolReg(CProtocol):
    def __init__(self, callbacks):
        self._callbacks = callbacks
        super().__init__()

    def create_request(self, cmd: str, args: str) -> str:
        """Create a valid protocol message, will be sent by client, with length field"""
        request = f"{len(cmd + '>' + args):0{self.HEADER_LEN}}{cmd}"
        return request

    def create_response(self, cmd: str, args: str) -> str:
        """Create a valid protocol message, will be sent by server, with length field"""
        response = "05Error"

        return f"{len(response):0{self.HEADER_LEN}}{response}"