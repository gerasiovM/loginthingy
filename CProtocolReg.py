from CProtocol import *
from json import loads, JSONDecodeError


class CProtocolReg(CProtocol):
    def __init__(self, callbacks):
        self._callbacks = callbacks
        super().__init__()

    def create_request(self, cmd: str, args: str) -> str:
        """Create a valid protocol message, will be sent by client, with length field"""
        request = f"{len(cmd + '>' + args):0{self.HEADER_LEN}}{cmd + '>' + args}"
        print(request)
        return request

    def create_response(self, cmd: str, args: str) -> str:
        """Create a valid protocol message, will be sent by server, with length field"""
        response = "Error"
        if cmd == "REG":
            try:
                print(args)
                res = loads(args)
                if (not isinstance(res, dict) or "login" not in res.keys() or "password" not in
                        res.keys()):
                    response = "A valid json object wasn't provided"
                else:
                    self._callbacks[0]((res["login"], res["password"],))
                    response = "Request received"
            except JSONDecodeError as e:
                response = "A json object wasn't provided"
        return f"{len(response):0{self.HEADER_LEN}}{response}"