import customtkinter as ctk
from gui.register import Registration
from gui.chat import ChatWindow

  


class LoginWindow:
    def __init__(self,auth,client):
        # Window
        self.auth = auth
        self.client = client
        self.window = ctk.CTk()
        self.window.title("Secure Chat")
        self.window.geometry("900x400")
        self.window.minsize(900, 400)

        #Appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0,weight=1)

        #Main Frame
        self.main_frame =  ctk.CTkFrame(self.window)
        self.main_frame.grid(row=0, column=0,padx= 20,pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)

        #Title Label
        self.title_label = ctk.CTkLabel(self.main_frame,text="Secure Chat",font=("Arial",28,"bold"))
        self.title_label.grid(row =0,column =0 ,pady=(20,20))

        #Username Entry
        self.username_entry = ctk.CTkEntry(self.main_frame,width=300,placeholder_text="Username")
        self.username_entry.grid(row =1, column =0,pady=20)
        
        # Password Entry
        self.password_entry = ctk.CTkEntry(self.main_frame,width=300,placeholder_text="Password",show = "*")
        self.password_entry.grid(row =2 ,column=0,pady=20)

        #Login Button
        self.login_button = ctk.CTkButton(self.main_frame,width=50,command=self.login,text="Login")
        self.login_button.grid(row=3,column = 1,pady=20,padx = 20)

        #Register Button
        
        self.register_button = ctk.CTkButton(self.main_frame,width=50,command=self.register,text="Register")
        self.register_button.grid(row=4,column = 1,pady=20, padx = 20)

        #Status Label
        self.status_label = ctk.CTkLabel(self.main_frame, text="", text_color="red")
        self.status_label.grid(row=5, column=0, columnspan=2, pady=10)
        

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        # Check for empty fields
        if not username or not password:
            self.status_label.configure(text="All fields are required")
            return

        try:
            # Connect to the server
            print("1. Connecting...")
            self.client.connect()

            # Send login request
            print("2. Sending login packet...") 
            self.client.send(f"LOGIN|{username}|{password}")

            # Wait for server response
            print("3. Waiting for response...")
            response = self.client.receive()
            print("4. Response:", repr(response))
            if response == "Login_Success":
                self.window.withdraw()

                chat = ChatWindow(self.window, username, self.client)

                self.window.wait_window(chat.window)
                self.client.close()

                self.username_entry.delete(0, "end")
                self.password_entry.delete(0, "end")
                self.window.deiconify()

            else:
                self.status_label.configure(text="Invalid username or password")
                self.password_entry.delete(0, "end")
                self.client.close()

        except Exception as e:
            self.status_label.configure(text=f"Connection Error: {e}")
                

    def register(self):
        self.window.withdraw()
        registration =Registration(self.window, self.auth, self.client)
        # Wait until the registration window is closed
        self.window.wait_window(registration.window)

        self.window.deiconify()
    def run(self):
        self.window.mainloop()


