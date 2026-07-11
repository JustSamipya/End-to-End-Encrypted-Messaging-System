from server.database import Database
from server.auth import Auth
from gui.login import LoginWindow
from network.client_socket import ClientSocket

HOST = "127.0.0.1"
PORT = 5000

database = Database()
database.create_tables()

auth = Auth(database)
client = ClientSocket(HOST, PORT)


app = LoginWindow(auth,client=client)
app.run()