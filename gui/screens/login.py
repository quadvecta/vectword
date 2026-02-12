import tkinter as tk
from tkinter import messagebox
from auth import verify_master_password
from totp import verify_totp


class Login(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0f172a")
        self.controller = controller

        # ===== Shadow Layer =====
        shadow = tk.Frame(self, bg="#0b1120")
        shadow.place(relx=0.5, rely=0.5, anchor="center", width=540, height=420)

        # ===== Glass Card =====
        self.card = tk.Frame(
            self,
            bg="#1e293b"
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=520, height=400)

        self.build_ui()

    def build_ui(self):

        # ===== Title =====
        tk.Label(
            self.card,
            text="🔐 Unlock Vault",
            font=("Segoe UI", 24, "bold"),
            bg="#1e293b",
            fg="white"
        ).pack(pady=(40, 5))

        tk.Label(
            self.card,
            text="Enter your master password and 2FA code",
            font=("Segoe UI", 10),
            bg="#1e293b",
            fg="#94a3b8"
        ).pack(pady=(0, 30))

        # ===== Form Container =====
        form = tk.Frame(self.card, bg="#1e293b")
        form.pack()

        # ===== Master Password =====
        tk.Label(
            form,
            text="Master Password",
            bg="#1e293b",
            fg="white",
            anchor="w"
        ).pack(fill="x")

        self.password_entry = tk.Entry(
            form,
            show="*",
            width=30,
            font=("Segoe UI", 10),
            bg="#334155",
            fg="white",
            insertbackground="white",
            bd=0
        )
        self.password_entry.pack(pady=(5, 20), ipady=6)

        # ===== 2FA =====
        tk.Label(
            form,
            text="2FA Code",
            bg="#1e293b",
            fg="white",
            anchor="w"
        ).pack(fill="x")

        self.totp_entry = tk.Entry(
            form,
            width=30,
            font=("Segoe UI", 10),
            bg="#334155",
            fg="white",
            insertbackground="white",
            bd=0
        )
        self.totp_entry.pack(pady=(5, 30), ipady=6)

        # ===== Unlock Button =====
        self.login_btn = tk.Button(
            self.card,
            text="Unlock Vault",
            width=22,
            height=2,
            bg="#3b82f6",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            cursor="hand2",
            activebackground="#2563eb",
            command=self.login
        )
        self.login_btn.pack(pady=(0, 10))

        # ===== Back Button =====
        self.back_btn = tk.Button(
            self.card,
            text="⬅ Back to Home",
            width=22,
            height=2,
            bg="#475569",
            fg="white",
            font=("Segoe UI", 10),
            bd=0,
            cursor="hand2",
            activebackground="#334155",
            command=self.go_home
        )
        self.back_btn.pack()

        # Hover Effects
        self.add_hover(self.login_btn, "#3b82f6", "#2563eb")
        self.add_hover(self.back_btn, "#475569", "#334155")

    # ================= HOVER EFFECT =================
    def add_hover(self, button, normal_color, hover_color):
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))

    # ================= LOGIN LOGIC =================
    def login(self):
        password = self.password_entry.get()
        code = self.totp_entry.get()

        if not verify_master_password(password):
            messagebox.showerror("Error", "Invalid master password")
            return

        if not verify_totp(code):
            messagebox.showerror("Error", "Invalid 2FA code")
            return

        messagebox.showinfo("Success", "Vault unlocked!")

        # Clear fields
        self.password_entry.delete(0, tk.END)
        self.totp_entry.delete(0, tk.END)

        self.controller.show("Vault", password=password)

    # ================= NAVIGATION =================
    def go_home(self):
        self.password_entry.delete(0, tk.END)
        self.totp_entry.delete(0, tk.END)
        self.controller.show("Welcome")
