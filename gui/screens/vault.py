import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from vault import load_vault, save_vault
from encryptor import derive_key
import re
import secrets
import string



class Vault(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#0f172a")
        self.app = app
        self.password = None
        self.vault_data = {}

        # ===== Auto Lock Settings =====
        self.auto_lock_minutes = 1
        self.auto_lock_seconds = self.auto_lock_minutes * 60
        self.remaining_seconds = self.auto_lock_seconds
        self.auto_lock_job = None
        self.countdown_job = None

        # ===== Glass Card =====
        self.card = tk.Frame(self, bg="#1e293b", padx=30, pady=30)
        self.card.pack(expand=True)

        # ===== Title =====
        tk.Label(
            self.card,
            text="🔐 Secure Vault",
            font=("Segoe UI", 22, "bold"),
            bg="#1e293b",
            fg="white"
        ).pack(pady=(0, 10))

        # ===== Timer Label =====
        self.timer_label = tk.Label(
            self.card,
            text="Auto-lock in: --:--",
            bg="#1e293b",
            fg="#94a3b8",
            font=("Segoe UI", 9)
        )
        self.timer_label.pack(pady=(0, 10))

        # ===== Detect User Activity =====
        self.bind_all("<Key>", self.reset_auto_lock_timer)
        self.bind_all("<Motion>", self.reset_auto_lock_timer)
        self.bind_all("<Button>", self.reset_auto_lock_timer)

        # ===== Search =====
        search_frame = tk.Frame(self.card, bg="#1e293b")
        search_frame.pack(fill="x", pady=(0, 15))

        tk.Label(
            search_frame,
            text="🔍 Search:",
            bg="#1e293b",
            fg="#94a3b8",
            font=("Segoe UI", 9)
        ).pack(side="left")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.update_table())

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            bg="#334155",
            fg="white",
            insertbackground="white",
            bd=0
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=(5, 0), ipady=6)

        # ===== Table =====
        tree_frame = tk.Frame(self.card, bg="#1e293b")
        tree_frame.pack(fill="both", expand=True)

        columns = ("site", "password", "strength")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading("site", text="Website / Application")
        self.tree.heading("password", text="Password (Hidden)")
        self.tree.heading("strength", text="Security Level")

        self.tree.column("site", width=220)
        self.tree.column("password", width=250)
        self.tree.column("strength", width=120)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ===== Buttons =====
        button_frame = tk.Frame(self.card, bg="#1e293b")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="➕ Add", bg="#10b981", fg="white",
                  width=12, command=self.add_entry).grid(row=0, column=0, padx=10)

        tk.Button(button_frame, text="👁 View", bg="#3b82f6", fg="white",
                  width=12, command=self.view_entry).grid(row=0, column=1, padx=10)

        tk.Button(button_frame, text="🗑 Delete", bg="#ef4444", fg="white",
                  width=12, command=self.delete_entry).grid(row=0, column=2, padx=10)

        tk.Button(self.card, text="🔒 Lock & Exit", bg="#475569", fg="white",
                  width=20, command=self.lock_vault).pack(pady=(0, 10))


    # ================= Vault Logic =================

    def refresh(self, password):
        self.password = password
        key = derive_key(password)
        data = load_vault(key)
        self.vault_data = data if data else {}
        self.update_table()

        self.start_auto_lock_timer()


    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        search_query = self.search_var.get().lower()

        for site, pwd in self.vault_data.items():
            if search_query in site.lower():
                masked_pwd = "•" * 12
                self.tree.insert("", tk.END,
                                 values=(site, masked_pwd, self.get_strength(pwd)))


    # ================= Entry Actions =================

    def add_entry(self):
        site = simpledialog.askstring("Add Entry", "Enter site/app name:")
        if not site:
            return

    # Ask user if they want to generate password
        generate = messagebox.askyesno("Generate Password", "Generate a secure password?")

        if generate:
            pwd = self.generate_password()
            messagebox.showinfo("Generated Password", f"Generated:\n{pwd}")
        else:
            pwd = simpledialog.askstring(
            "Add Entry",
            f"Enter password for {site}:",
            show='*'
        )

        if not pwd:
            return

        self.vault_data[site] = pwd
        key = derive_key(self.password)
        save_vault(self.vault_data, key)

        self.update_table()
        messagebox.showinfo("Success", f"{site} saved.")



    def view_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Click a row to view.")
            return

        site = self.tree.item(selected[0], "values")[0]
        real_pwd = self.vault_data.get(site, "Not Found")
        messagebox.showinfo("Credentials", f"Site: {site}\nPassword: {real_pwd}")


    def delete_entry(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Select an entry.")
            return

        site = self.tree.item(selected[0], "values")[0]
        if messagebox.askyesno("Confirm", f"Delete {site}?"):
            del self.vault_data[site]
            key = derive_key(self.password)
            save_vault(self.vault_data, key)
            self.update_table()


    def lock_vault(self):
        self.cancel_auto_lock_timer()
        self.vault_data = {}
        self.password = None
        self.search_var.set("")
        self.update_table()
        self.timer_label.config(text="Auto-lock in: --:--")
        self.app.show("Welcome")


    # ================= Password Strength =================

    def get_strength(self, pwd):
        score = sum([
            len(pwd) >= 8,
            bool(re.search(r"[A-Z]", pwd)),
            bool(re.search(r"[a-z]", pwd)),
            bool(re.search(r"\d", pwd)),
            bool(re.search(r"[!@#$%^&*()]", pwd))
        ])

        mapping = {
            0: "Weak",
            1: "Weak",
            2: "Weak",
            3: "Moderate",
            4: "Strong",
            5: "Very Strong"
        }
        return mapping.get(score, "Weak")


    # ================= AUTO LOCK SYSTEM =================

    def start_auto_lock_timer(self):
        self.cancel_auto_lock_timer()
        self.remaining_seconds = self.auto_lock_seconds
        self.update_countdown()


    def update_countdown(self):
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        self.timer_label.config(text=f"Auto-lock in: {minutes:02}:{seconds:02}")

        if self.remaining_seconds <= 0:
            self.auto_lock()
        else:
            self.remaining_seconds -= 1
            self.countdown_job = self.after(1000, self.update_countdown)


    def cancel_auto_lock_timer(self):
        if self.countdown_job:
            self.after_cancel(self.countdown_job)
            self.countdown_job = None


    def reset_auto_lock_timer(self, event=None):
        if self.password:  # Only reset if vault unlocked
            self.start_auto_lock_timer()


    def auto_lock(self):
        messagebox.showwarning("Auto Lock", "Vault locked due to inactivity.")
        self.lock_vault()
    # ================= PASSWORD GENERATOR =================

    def generate_password(self, length=16, use_symbols=True):
        letters = string.ascii_letters
        digits = string.digits
        symbols = "!@#$%^&*()"

        characters = letters + digits
        if use_symbols:
            characters += symbols

    # Ensure at least one of each type
        password = [
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.digits),
    ]

        if use_symbols:
            password.append(secrets.choice(symbols))

    # Fill remaining length
        password += [secrets.choice(characters) for _ in range(length - len(password))]

        secrets.SystemRandom().shuffle(password)

        return "".join(password)

