import customtkinter as ctk
import threading
from cryptography.aes_manager import generate_aes_key, encrypt_message,decrypt_message
from cryptography.rsa_manager import encrypt_aes_key,load_private_key,decrypt_aes_key
import base64

class ChatWindow:
    def __init__(self, parent, username,client):
        # Window
        self.username = username
        self.private_key = load_private_key(username)
        self.client = client
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Secure Chat")
        self.window.geometry("900x600")
        self.window.minsize(900, 600)
        print("Chat window created")

        # Appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Window Grid
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # Main Frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Configuration of rows/columns in main frame 
        self.main_frame.grid_rowconfigure(3, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=0)

        # ---------- Widgets ----------
        # Title Label
        self.title_label = ctk.CTkLabel(self.main_frame,text='Secure Chat',font=("Arial",30,"bold"))
        self.title_label.grid(row=0,column=0,padx=100,pady=20)
        #Receiver entry
        self.receiver_entry = ctk.CTkEntry(self.main_frame,placeholder_text="Receiver username")
        self.receiver_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        #Load chat button
        self.load_chat_btn = ctk.CTkButton(self.main_frame,text='Open Chat',command = self.open_chat)
        self.load_chat_btn.grid(row =1,column = 1,padx=10,pady=10)
        # Chat Textbox
        self.chat_box = ctk.CTkTextbox(self.main_frame,width=600,height=400,corner_radius=10,wrap="word")
        self.chat_box.grid(row=3,column=0,columnspan=2,padx=10,pady=20,sticky="nsew")
        # Message Entry
        self.message_entry = ctk.CTkEntry(self.main_frame, placeholder_text='Type a message')
        self.message_entry.grid(row=4,column=0,padx=10,pady=20,sticky="ew")

        # Send Button
        self.send_btn = ctk.CTkButton(self.main_frame,text='Send',command=self.send_message)
        self.send_btn.grid(row=4,column=1)


        # Logout Button
        self.logout_btn = ctk.CTkButton(self.main_frame,text ="Logout",command=self.logout)
        self.logout_btn.grid(row=0, column=1)

        # threading
        thread = threading.Thread(target=self.receive_messages,daemon=True)
        thread.start()

        self.current_receiver = None
        self.public_key_event = threading.Event()
        self.public_key_lock = threading.Lock()
        self.public_key = None

    def send_message(self):
        receiver = self.receiver_entry.get().strip()
        message = self.message_entry.get().strip()

        if not message or not receiver:
            return

        threading.Thread(
            target=self._send_message_worker,
            args=(receiver, message),
            daemon=True,
        ).start()

        self.message_entry.delete(0, "end")

    def _send_message_worker(self, receiver, message):
        sender_public_key = self.request_public_key(self.username)
        if sender_public_key is None:
            return
        receiver_public_key = self.request_public_key(receiver)
        if receiver_public_key is None:
            return

        aes_key = generate_aes_key()
        nonce, tag, ciphertext = encrypt_message(message, aes_key)

        sender_encrypted_key = encrypt_aes_key(aes_key, sender_public_key)
        receiver_encrypted_key = encrypt_aes_key(aes_key, receiver_public_key)

        sender_encrypted_key = base64.b64encode(sender_encrypted_key).decode()
        receiver_encrypted_key = base64.b64encode(receiver_encrypted_key).decode()
        nonce = base64.b64encode(nonce).decode()
        tag = base64.b64encode(tag).decode()
        ciphertext = base64.b64encode(ciphertext).decode()

        packet = (
            f"MESSAGE|{receiver}|{sender_encrypted_key}|"
            f"{receiver_encrypted_key}|{nonce}|{tag}|{ciphertext}"
        )
        self.client.send(packet)

        self.window.after(0, self.display_message, f"You: {message}")
    
    def receive_messages(self):
        print("Receive thread started")

        while True:
            try:
                message = self.client.receive()
                print("Received from server:", message)

                if message is None:
                    break

                parts = message.split("|", 1)

                if parts[0] == "PUBLIC_KEY":
                    self.public_key = base64.b64decode(parts[1]).decode()
                    self.public_key_event.set()
                    continue

                parts = message.split("|", 5)
                packet_type = parts[0]
                if packet_type == "MESSAGE":

                    sender = parts[1]

                    encrypted_key = base64.b64decode(parts[2])
                    aes_key = decrypt_aes_key(encrypted_key,self.private_key)

                    nonce = base64.b64decode(parts[3])

                    tag = base64.b64decode(parts[4])

                    ciphertext = base64.b64decode(parts[5])
                    plaintext = decrypt_message(nonce,tag,ciphertext,aes_key)
                    display = f"{sender}: {plaintext}"

                    self.window.after(
                        0,
                        self.display_message,
                        display
                    )

                elif packet_type == "HISTORY":

                    sender = parts[1]

                    encrypted_key = base64.b64decode(parts[2])
                    nonce = base64.b64decode(parts[3])
                    tag = base64.b64decode(parts[4])
                    ciphertext = base64.b64decode(parts[5])

                    aes_key = decrypt_aes_key(
                        encrypted_key,
                        self.private_key
                    )

                    plaintext = decrypt_message(
                        nonce,
                        tag,
                        ciphertext,
                        aes_key
                    )

                    if sender == self.username:
                        display = f"You: {plaintext}"
                    else:
                        display = f"{sender}: {plaintext}"

                    self.window.after(0, self.display_message, display)

                else:
                    self.window.after(0, self.display_message, message)

            except Exception as e:
                print("Receive thread stopped:", e)
                break
    def display_message(self,message):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end",f"{message}\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")

    def open_chat(self):
        self.chat_box.configure(state="normal")
        self.chat_box.delete("1.0", "end")
        self.current_receiver = self.receiver_entry.get().strip()
        if not self.current_receiver:
            return

        self.client.send(f"LOAD_MESSAGES|{self.current_receiver}")
        
    def request_public_key(self, receiver):

        
        with self.public_key_lock:
            self.public_key = None
            self.public_key_event.clear()
            self.client.send(f"GET_PUBLIC_KEY|{receiver}")
            self.public_key_event.wait()
            return self.public_key
        

    def logout(self):
        print("Logout called")
        self.window.destroy()
    