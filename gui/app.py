import tkinter as tk
from gui.screens.welcome import Welcome
from gui.screens.login import Login
from gui.screens.register import Register
from gui.screens.vault import Vault

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Vaultword")
        self.geometry("900x600")
        self.minsize(900, 600)
        self.resizable(True, True)
        self.configure(bg="#f7f7f7")
        
        # Center the window on the screen
        self.eval('tk::PlaceWindow . center')

        # The main container where all screens "live"
        self.container = tk.Frame(self, bg="#f7f7f7")
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        # ✅ REGISTER ALL SCREENS
        for Screen in (Welcome, Login, Register, Vault):
            self.register(Screen)

        # ✅ START WITH WELCOME
        self.show("Welcome")

    def register(self, Screen):
        """Initializes the screen and adds it to the frames dictionary"""
        frame = Screen(self.container, self)
        self.frames[Screen.__name__] = frame
        # Use place so screens stack on top of each other
        frame.place(relwidth=1, relheight=1)

    def show(self, name, password=None):
        """
        Switches the visible screen. 
        If 'password' is provided, it triggers the Vault data load.
        """
        if name not in self.frames:
            print(f"Error: Screen '{name}' not found.")
            return

        frame = self.frames[name]
        
        # PERSISTENCE FIX: 
        # When moving to Vault, send the password to the Vault class 
        # so it can run load_vault() and update_table()
        if name == "Vault" and password:
            if hasattr(frame, 'refresh'):
                frame.refresh(password)
            
        frame.tkraise()