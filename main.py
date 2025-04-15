from auth import register_master_password, verify_master_password
from encryptor import derive_key
from vault import save_vault, load_vault
from totp import setup_totp, verify_totp
import os

def main():
    print("🛡️ Welcome to Vectword – Secure Password Vault")
    mode = input("Do you want to [login] or [register]? ").strip().lower()

    if mode == "register":
        password = input("🔑 Set your master password: ")
        register_master_password(password)
        setup_totp()
        print("✅ Master password & 2FA setup complete!")
        print("📱 Scan the generated QR code (assets/totp_qr.png) with Google Authenticator.")
        return

    elif mode == "login":
        password = input("🔑 Enter master password: ")
        if not verify_master_password(password):
            print("❌ Invalid password.")
            return

        if not os.path.exists("data/totp.secret"):
            print("⚠️ 2FA not set up. Please re-register.")
            return

        code = input("🔐 Enter your 6-digit 2FA code: ")
        if not verify_totp(code):
            print("❌ Invalid 2FA code.")
            return

        key = derive_key(password)
        vault = load_vault(key)
        if vault is None:
            print("❌ Vault could not be decrypted.")
            return

        while True:
            print("\nOptions: [add] [view] [delete] [exit]")
            cmd = input("Command: ").strip().lower()

            if cmd == "add":
                site = input("🌐 Site: ")
                user = input("👤 Username: ")
                pw = input("🔐 Password: ")
                vault[site] = {"username": user, "password": pw}
                save_vault(vault, key)
                print("✅ Saved.")

            elif cmd == "view":
                if not vault:
                    print("📂 Vault is empty.")
                for site, creds in vault.items():
                    print(f"{site}: {creds['username']} / {creds['password']}")

            elif cmd == "delete":
                site = input("🗑️ Site to delete: ")
                if site in vault:
                    del vault[site]
                    save_vault(vault, key)
                    print("🗑️ Deleted.")
                else:
                    print("❌ Not found.")

            elif cmd == "exit":
                print("🔒 Vault locked. Goodbye!")
                break

            else:
                print("❓ Unknown command.")

    else:
        print("❌ Unknown option.")

if __name__ == "__main__":
    main()
