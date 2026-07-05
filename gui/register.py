import customtkinter as ctk

class Registration:
    def __init__(self,parent,auth):
        
        # Window
        self.auth = auth
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Register")
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
        self.title_label = ctk.CTkLabel(self.main_frame,text="Create Account",font=("Arial",28,"bold"))
        self.title_label.grid(row =0,column =0 ,pady=(20,20))

        #Username Entry
        self.username_entry = ctk.CTkEntry(self.main_frame,width=300,placeholder_text="Username")
        self.username_entry.grid(row =1, column =0,pady=20)
        
        # Password Entry
        self.password_entry = ctk.CTkEntry(self.main_frame,width=300,placeholder_text="Password",show = "*")
        self.password_entry.grid(row =2 ,column=0,pady=20)

        # Repassword Entry 
        self.repassword_entry = ctk.CTkEntry(self.main_frame,width=300,placeholder_text="Confirm Password",show="*")
        self.repassword_entry.grid(row=3 ,column =0)
        
        #Registration Status
        self.status_label =  ctk.CTkLabel(self.main_frame,text="")
        self.status_label.grid(row=4,column=0)

        #Register Button
        self.registration_btn = ctk.CTkButton(self.main_frame   ,text="Register",command=self.register)
        self.registration_btn.grid(row=5,column =0,pady= 20)
    def register(self):
        
        username = self.username_entry.get()
        password = self.password_entry.get()
        repassword = self.repassword_entry.get()
        if not username or not password or not repassword:
            self.status_label.configure(text="All fields are required")
            self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")
            self.repassword_entry.delete(0, "end")
            return
        if password != repassword:
            self.status_label.configure(text="Passwords do not match")
            self.password_entry.delete(0, "end")
            self.repassword_entry.delete(0, "end")
            return
        success = self.auth.register(username,password)
        if success:
            
            self.window.destroy()
            return
        else:
            self.status_label.configure(text="Username already exists")
            self.password_entry.delete(0, "end")
            self.repassword_entry.delete(0, "end")
            self.username_entry.delete(0, "end")
            return
        


            