import customtkinter as ctk
  


class LoginWindow:
    def __init__(self,auth):
        # Window
        self.auth = auth
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
        

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success = self.auth.login(username, password)
        print(success)
    def register(self):
        print("Clicked")
    def run(self):
        self.window.mainloop()


