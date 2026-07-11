import socket
import threading
import base64
from server.auth import Auth
from server.database import Database

server_socket = socket.socket()
host = "127.0.0.1"
port = 5000
server_socket.bind((host,port))
server_socket.listen(5)


database = Database()
database.create_tables()
auth = Auth(database)
connected_clients_lock = threading.Lock()
connected_clients = {}

def handle_message(sender, packet):
    parts = packet.split("|",6)
    print(parts)
    if len(parts) != 7:
        return

    receiver = parts[1]
    sender_encrypted_key = parts[2]
    receiver_encrypted_key = parts[3]
    nonce = parts[4]
    tag = parts[5]
    ciphertext = parts[6]

    database.save_message(sender, receiver, sender_encrypted_key,receiver_encrypted_key,nonce,tag,ciphertext)

    with connected_clients_lock:
        receiver_socket = connected_clients.get(receiver)

    if receiver_socket:
        forward_packet = (
    f"MESSAGE|"
    f"{sender}|"
    f"{receiver_encrypted_key}|"
    f"{nonce}|"
    f"{tag}|"
    f"{ciphertext}")
        receiver_socket.send((forward_packet+ "\n").encode())

def handle_load_messages(username, client_socket, parts):

    if len(parts) != 2:
        return

    receiver = parts[1]

    messages = database.load_messages(username, receiver)

    for( sender,receiver,sender_encrypted_key,receiver_encrypted_key,nonce,tag,ciphertext,timestamp) in messages:
        if sender == username:
            encrypted_key = sender_encrypted_key
        else:
            encrypted_key = receiver_encrypted_key
        packet = (
        f"HISTORY|"
        f"{sender}|"
        f"{encrypted_key}|"
        f"{nonce}|"
        f"{tag}|"
        f"{ciphertext}"
    )
    
        client_socket.send((packet + "\n").encode())
    
def handle_get_public_key(client_socket, parts):

    if len(parts) != 2:
        return

    username = parts[1]

    public_key = database.get_public_key(username)

    if public_key is None:
        client_socket.send(b"PUBLIC_KEY_NOT_FOUND\n")
        return

    public_key_b64 = base64.b64encode(public_key.encode()).decode()
    packet = f"PUBLIC_KEY|{public_key_b64}"
    client_socket.send((packet + "\n").encode())
def handle_register(client_socket, packet):
    parts = packet.split("|", 3)
    if len(parts) != 4:
        client_socket.send(b"Register_Failed\n")
        return

    _, username, password, public_key_b64 = parts
    public_key = base64.b64decode(public_key_b64).decode()
    success = auth.register_with_public_key(username, password, public_key)

    client_socket.send(b"Register_Success\n" if success else b"Register_Failed\n")

def process_packet(username, client_socket, packet):
    parts = packet.split("|", 2)

    if not parts:
        print("No parts")
        return

    packet_type = parts[0]
    
    if packet_type == "MESSAGE":
        handle_message(username, packet)

    elif packet_type == "LOAD_MESSAGES":
        handle_load_messages(username, client_socket, parts)

    elif packet_type == "GET_PUBLIC_KEY":
        handle_get_public_key(client_socket, parts)

    else:
        print("Unknown packet:", packet)

def receive_packet(client_socket, buffer):
    while "\n" not in buffer:
        data = client_socket.recv(8192)

        if not data:
            return None, buffer

        buffer += data.decode()

    packet, buffer = buffer.split("\n", 1)

    return packet, buffer

def handle_client(client_socket):
    
    # ----- Login -----
    buffer = ""
    first_packet, buffer = receive_packet(client_socket, buffer)
    if first_packet is None:
        client_socket.close()
        return

    if first_packet.startswith("REGISTER|"):
        handle_register(client_socket, first_packet)
        client_socket.close()
        return

    parts = first_packet.split("|")
    if len(parts) != 3 or parts[0] != "LOGIN":
        client_socket.close()
        return
    _, username, password = parts

    success = auth.login(username, password)
    print("Username:", username)
    print("Password:", repr(password))
    print("Auth result:", success)

    if not success:
        client_socket.send(b"Login_Failed\n")
        client_socket.close()
        return

    if username in connected_clients:
        client_socket.send(b"Login_Failed\n")
        client_socket.close()
        return

    connected_clients[username] = client_socket
    client_socket.send(b"Login_Success\n")

    print(f"{username} logged in")

    # ----- Packet loop -----
    try:
        while True:

            packet, buffer = receive_packet(client_socket, buffer)

            if packet is None:
                break

            process_packet(username, client_socket, packet)

    finally:
        connected_clients.pop(username, None)
        client_socket.close()
        print(f"{username} disconnected")
                        
while True:
    client_socket ,address  = server_socket.accept()
    print(f"{address} Connected")
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
    

