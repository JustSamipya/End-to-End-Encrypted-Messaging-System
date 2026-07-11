import socket

class ClientSocket:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.buffer = ""

    def connect(self):
        self.client_socket = socket.socket()
        self.client_socket.connect((self.host, self.port))

    def send(self, message: str):
        if not message:
            return

        self.client_socket.sendall((message + "\n").encode())

    def receive(self):
        while "\n" not in self.buffer:
            data = self.client_socket.recv(8192)

            if not data:
                return None

            self.buffer += data.decode()

        packet, self.buffer = self.buffer.split("\n", 1)

        return packet

    def close(self):
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None