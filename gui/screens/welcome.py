import tkinter as tk


class Welcome(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ===== Background =====
        self.configure(bg="#0f172a")

        # ===== Glass Card =====
        self.card = tk.Frame(
            self,
            bg="#1e293b",
            highlightthickness=0
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=520, height=380)

        # Shadow effect (fake layered frame)
        shadow = tk.Frame(self, bg="#0b1120")
        shadow.place(relx=0.5, rely=0.5, anchor="center", width=530, height=390)
        self.card.lift()

        # ===== Logo / Title =====
        self.title = tk.Label(
            self.card,
            text="🔐 BlackShield",
            font=("Segoe UI", 30, "bold"),
            bg="#1e293b",
            fg="white"
        )
        self.title.pack(pady=(50, 10))

        self.subtitle = tk.Label(
            self.card,
            text="Secure • Private • Encrypted Password Manager",
            font=("Segoe UI", 11),
            bg="#1e293b",
            fg="#94a3b8"
        )
        self.subtitle.pack(pady=(0, 40))

        # ===== Buttons =====
        self.login_btn = tk.Button(
            self.card,
            text="Login",
            width=20,
            height=2,
            bg="#3b82f6",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            cursor="hand2",
            activebackground="#2563eb",
            command=lambda: controller.show("Login")
        )
        self.login_btn.pack(pady=10)

        self.register_btn = tk.Button(
            self.card,
            text="Create Account",
            width=20,
            height=2,
            bg="#10b981",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            cursor="hand2",
            activebackground="#059669",
            command=lambda: controller.show("Register")
        )
        self.register_btn.pack()

        # ===== Hover Effects =====
        self.add_hover(self.login_btn, "#3b82f6", "#2563eb")
        self.add_hover(self.register_btn, "#10b981", "#059669")

        # ===== Fade In Animation =====
        self.fade_in()

    # ================= HOVER EFFECT =================
    def add_hover(self, button, normal_color, hover_color):
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))

    # ================= FADE IN EFFECT =================
    def fade_in(self):
        self.alpha = 0
        self.root = self.winfo_toplevel()  # get main window safely
        self.root.attributes("-alpha", 0)
        self.increment_fade()

    def increment_fade(self):
        if self.alpha < 1:
            self.alpha += 0.05
        self.root.attributes("-alpha", self.alpha)
        self.after(20, self.increment_fade)
