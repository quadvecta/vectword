import tkinter as tk
from auth import register_master_password
from totp import setup_totp
from PIL import Image, ImageTk


class Register(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#0f172a")
        self.app = app
        self.qr_img = None

        # ===== Glass Card (NO fixed height) =====
        self.card = tk.Frame(
            self,
            bg="#1e293b",
            padx=50,
            pady=40
        )
        self.card.pack(expand=True)

        self.build_ui()

    # ================= UI =================
    def build_ui(self):

        # ===== Title =====
        tk.Label(
            self.card,
            text="🔐 Create Vault",
            font=("Segoe UI", 24, "bold"),
            bg="#1e293b",
            fg="white"
        ).pack(pady=(0, 5))

        tk.Label(
            self.card,
            text="Set a master password for your vault",
            font=("Segoe UI", 10),
            bg="#1e293b",
            fg="#94a3b8"
        ).pack(pady=(0, 30))

        # ===== Form =====
        form = tk.Frame(self.card, bg="#1e293b")
        form.pack()

        # Master Password
        tk.Label(
            form,
            text="Master Password",
            bg="#1e293b",
            fg="white",
            anchor="w"
        ).pack(fill="x")

        self.pw1 = tk.Entry(
            form,
            show="*",
            width=30,
            font=("Segoe UI", 10),
            bg="#334155",
            fg="white",
            insertbackground="white",
            bd=0
        )
        self.pw1.pack(pady=(5, 20), ipady=6)

        # Confirm Password
        tk.Label(
            form,
            text="Confirm Password",
            bg="#1e293b",
            fg="white",
            anchor="w"
        ).pack(fill="x")

        self.pw2 = tk.Entry(
            form,
            show="*",
            width=30,
            font=("Segoe UI", 10),
            bg="#334155",
            fg="white",
            insertbackground="white",
            bd=0
        )
        self.pw2.pack(pady=(5, 20), ipady=6)

        # ===== Error Message =====
        self.message = tk.StringVar()
        tk.Label(
            self.card,
            textvariable=self.message,
            bg="#1e293b",
            fg="#ef4444",
            font=("Segoe UI", 9)
        ).pack(pady=(0, 10))

        # ===== Generate QR Button =====
        self.button = tk.Button(
            self.card,
            text="Generate 2FA QR Code",
            width=24,
            height=2,
            bg="#3b82f6",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            cursor="hand2",
            activebackground="#2563eb",
            command=self.register
        )
        self.button.pack(pady=10)

        self.add_hover(self.button, "#3b82f6", "#2563eb")
        
        self.back_btn = tk.Button(
            self.card,
            text="⬅ Back to Home",
            bg="#475569",
            fg="white",
            width=20,
            font=("Segoe UI", 9),
            bd=0,
            cursor="hand2",
            command=lambda: self.app.show("Welcome")
            )
        self.back_btn.pack(pady=(10, 0))


        # ===== QR Section =====
        self.qr_label = tk.Label(self.card, bg="#1e293b")
        self.qr_label.pack(pady=15)

        self.info = tk.Label(
            self.card,
            text="",
            font=("Segoe UI", 9),
            bg="#1e293b",
            fg="#94a3b8"
        )
        self.info.pack()

        # ===== Go To Login Button (Hidden Initially) =====
        self.login_button = tk.Button(
            self.card,
            text="🔐 Go to Login",
            width=24,
            height=2,
            bg="#10b981",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            cursor="hand2",
            activebackground="#059669",
            command=self.go_to_login
        )

    # ================= Hover Effect =================
    def add_hover(self, button, normal_color, hover_color):
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))

    # ================= Register Logic =================
    def register(self):
        pw1 = self.pw1.get()
        pw2 = self.pw2.get()

        if not pw1 or not pw2:
            self.message.set("Password fields cannot be empty")
            return

        if pw1 != pw2:
            self.message.set("Passwords do not match")
            return

        self.message.set("")

        # Save password
        register_master_password(pw1)

        # Generate QR
        qr_path = setup_totp()

        img = Image.open(qr_path).resize((180, 180))
        self.qr_img = ImageTk.PhotoImage(img)
        self.qr_label.config(image=self.qr_img)

        self.info.config(
            text="Scan this QR code with Google Authenticator.\nThen proceed to login."
        )

        self.button.config(state="disabled")

        # Clear fields for security
        self.pw1.delete(0, tk.END)
        self.pw2.delete(0, tk.END)

        # Show login button
        self.login_button.pack(pady=15)
        self.add_hover(self.login_button, "#10b981", "#059669")

    # ================= Navigation =================
    def go_to_login(self):
        self.app.show("Login")
