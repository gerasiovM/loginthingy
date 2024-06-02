from CProtocol import *
import os
import socket
import glob
import shutil
import subprocess
# Light-weight screenshot manager
import mss
import time

# Creates a file_system folder with temp.txt inside for checking DELETE functionality
if not os.path.exists("file_system"):
    os.mkdir("file_system")
    with open("file_system/temp.txt", "w"):
        pass


class CProtocol27(CProtocol):
    ALLOWED_DIRECTORIES = {
        "DELETE": os.path.abspath("file_system"),
        "DIR": os.path.abspath(".."),
        "COPY": os.path.abspath(".")
    }

    def __init__(self, client_socket: socket.socket):
        super().__init__()
        self._client_socket = client_socket

    # Checks if the child_path is a subdirectory of parent_path
    def is_subdirectory(self, parent_path, child_path):
        """Check if child_path is a subdirectory of parent_path"""
        parent_path = os.path.abspath(parent_path)
        child_path = os.path.abspath(child_path)
        return os.path.commonpath([parent_path, child_path]) == parent_path

    # Checks if command should be allowed in a given path
    def is_operation_allowed(self, command, path):
        allowed_directory = self.ALLOWED_DIRECTORIES.get(command)
        if command == "DELETE":
            return self.is_subdirectory(allowed_directory, path) and allowed_directory != os.path.abspath(path)
        return self.is_subdirectory(allowed_directory, path)

    def create_request(self, cmd: str, args: str) -> str:
        """Create a valid protocol message, will be sent by client, with length field"""
        request = f"{len(cmd + '>' + args):0{self.HEADER_LEN}}{cmd + '>' + args}"
        return request

    def create_response(self, command: str, args: str) -> str:
        """Create a valid protocol message, will be sent by server, with length field"""
        args_num = 0
        if args:
            args_num = 1
        args = args.split("<")
        if len(args) > 1:
            args_num = len(args)
        response = "Non-supported cmd " + command
        command = command.upper()
        # Lambda function to obfuscate an absolute path.
        # Example: "/home/max/cyber/2.7" -> "cyber/2.7"
        obfuscate_path = lambda abs_path: os.path.relpath(abs_path, os.path.abspath(os.path.join("..", "..")))
        # Lambda function to create a not allowed response,
        # where x is the command and y is the path
        response_not_allowed = lambda command_name, abs_path: \
            f"Command \"{command_name}\" not allowed on \"{obfuscate_path(abs_path)}y\""
        # Lambda function to create an incorrect arguments num response,
        # where x is the command, y is the required number of arguments and z is the given number
        response_incorrect_arguments_num = lambda command_name, required_arg_num, given_arg_num: \
            f"Command \"{command_name}\" requires \"{required_arg_num}\" arguments, \"{given_arg_num}\" were given"
        # Lambda function to create an incorrect argument format response,
        # where x is the argument name and y is the argument requirement
        response_incorrect_argument_format = lambda argument_name, requirement: \
            f"Argument \"{argument_name}\" must be a(n) {requirement}"
        if command == "DIR":
            # Check if there are arguments
            if args_num == 1:
                argument = args[0]
                path = os.path.abspath(argument)
                # Check if path exists and if it's a directory
                if os.path.exists(path) and os.path.isdir(path):
                    # Check if the command is allowed on this path
                    if self.is_operation_allowed(command, path):
                        response = str([obfuscate_path(x) for x in glob.glob(path + os.path.sep + "*")])
                    else:
                        response = response_not_allowed(command, path)
                else:
                    response = f"Path {obfuscate_path(path)} doesn't exist or isn't a directory"
            else:
                response = response_incorrect_arguments_num(command, 1, args_num)
        elif command == "DELETE":
            if args_num == 1:
                argument = args[0]
                path = os.path.abspath(argument)
                if os.path.exists(path):
                    if self.is_operation_allowed(command, path):
                        try:
                            os.remove(argument)
                            response = f"{obfuscate_path(path)} was deleted"
                        except OSError as e:
                            response = "Error occurred while attempting deletion"
                    else:
                        response = response_not_allowed(command, path)
                else:
                    response = f"Path {obfuscate_path(path)} doesn't exist"
            else:
                response = response_incorrect_arguments_num(command, 1, args_num)
        elif command == "COPY":
            if args_num == 2:
                copy_from_path, copy_to_path = [os.path.abspath(x) for x in args]
                if not os.path.exists(copy_from_path):
                    response = response_incorrect_argument_format("copy_from_path", "valid path")
                elif not os.path.exists(copy_to_path):
                    response = response_incorrect_argument_format("copy_to_path", "valid path")
                else:
                    if not self.is_operation_allowed(command, copy_from_path):
                        response = response_not_allowed(command, copy_from_path)
                    elif not self.is_operation_allowed(command, copy_to_path):
                        response = response_not_allowed(command, copy_to_path)
                    else:
                        if not os.path.isdir(copy_to_path):
                            response = response_incorrect_argument_format("copy_to_path", "directory")
                        else:
                            try:
                                if os.path.isdir(copy_from_path):
                                    shutil.copytree(copy_from_path, copy_to_path, copy_function=shutil.copy2,
                                                    dirs_exist_ok=True)
                                else:
                                    shutil.copy2(copy_from_path, copy_to_path)
                                response = f"Successfully copied from {obfuscate_path(copy_from_path)} to {obfuscate_path(copy_to_path)}"
                            except Exception as e:
                                response = "Exception while trying to perform a copy"
                                logging.error(e)
            else:
                response = response_incorrect_arguments_num(command, 1, args_num)
        # Execute works perfectly fine on linux. I have no idea if this works on windows
        elif command == "EXECUTE":
            if args_num == 1:
                execute_command = args[0]
                # Checking if the command we are trying to execute exists
                if shutil.which(execute_command):
                    try:
                        result = subprocess.run(execute_command, stdout=subprocess.PIPE, text=True)
                        response = str(result.stdout)
                        if not response:
                            respone = "Command executed successfuly"
                    except Exception as e:
                        response = "Exception while trying to execute a command"
                        logging.error(e)
                else:
                    response = response_incorrect_argument_format("command_name", "valid command")
            elif args_num > 1:
                response = "Command EXECUTE with arguments is not implemented"
            else:
                response = response_incorrect_arguments_num(command, 1, args_num)
        elif command == "TAKE_SCREENSHOT":
            def is_gui_available():
                if os.name == 'posix':
                    # Check if the DISPLAY environment variable is set (Unix-like systems)
                    display_var = os.environ.get('DISPLAY')
                    return display_var is not None
                elif os.name == 'nt':
                    # Check if the windir environment variable is set (Windows)
                    windir_var = os.environ.get('windir')
                    return windir_var is not None
                else:
                    # For other platforms, assume no GUI
                    return False
            try:
                if is_gui_available():
                    with mss.mss() as sct:
                        sct.shot(output=r'screen.jpg')
                        response = "Screenshot successful"
                else:
                    response = "System can't perform screenshot"
            except Exception as e:
                response = "Error while trying to screenshot"
                logging.error(e)
        elif command == "SEND_PHOTO":
            if args_num == 1:
                send_from = os.path.abspath(args[0])
                if os.path.exists(send_from):
                    if os.path.isfile(send_from):
                        response = self.send_big_image(self._client_socket, send_from)
                    else:
                        response = response_incorrect_argument_format("send_from", "file")
                else:
                    response = response_incorrect_argument_format("send_from", "valid path")
            else:
                response = response_incorrect_arguments_num(command, 1, args_num)
        elif command == self.DISCONNECT_MSG:
            response = "Bye"
        return f"{len(response.encode(self.FORMAT)):0{self.HEADER_LEN}}{response}"

    @staticmethod
    def send_big_image(my_socket: socket.socket, file_name: str, chunk_size=1024):
        txt = ''
        try:
            with open(file_name, "rb") as file:
                image_data = file.read()
                image_size = len(image_data)
                my_socket.send(image_size.to_bytes(4, byteorder='big'))
                logging.info(f"[Protocol] Sent image size - {image_size}")
                file.seek(0)
                while True:
                    image_data = file.read(chunk_size)
                    if not image_data:
                        break
                    my_socket.send(image_data)
                logging.info(f"[Protocol] Sent image data - done")
                txt = f'Sent photo {file_name} - done'
                time.sleep(0.1)
        except FileNotFoundError as e:
            logging.error(e)
            txt = f'Sent photo {file_name} - Photo file doesn\'t exist'
        return txt

    @staticmethod
    def receive_big_image(my_socket: socket.socket, file_name: str, chunk_size=1024):
        image_size = int.from_bytes(my_socket.recv(4), byteorder='big')
        logging.info(f"[Protocol] Received image size - {image_size}")
        received_data = b""
        while len(received_data) < image_size:
            data = my_socket.recv(chunk_size)
            if not data:
                break
            received_data += data
        logging.info(f"[Protocol] Received image data - Done")
        with open(file_name, "wb") as file:
            file.write(received_data)
        logging.info(f"[Protocol] Wrote data to file - done")

    def receive_msg(self, my_socket: socket.socket) -> (bool, str):
        """Extract message from protocol, without the length field
           If length field does not include a number, returns False, "Error" """

        str_header = my_socket.recv(self.HEADER_LEN).decode(self.FORMAT)
        logging.info(f"[Protocol] str_header - {str_header}")
        if not str_header.isnumeric():
            return False, "Error"
        length = int(str_header)
        logging.info(f"[Protocol] length - {length}")
        if length > 0:
            buf = my_socket.recv(length).decode(self.FORMAT)
        else:
            return False, 'Error'
        return True, buf