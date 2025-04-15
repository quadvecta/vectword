import pyotp
import os
import qrcode

TOTP_SECRET_FILE = "data/totp.secret"

def setup_totp():
    secret = pyotp.random_base32()
    if not os.path.exists("data"):
        os.makedirs("data")
    with open(TOTP_SECRET_FILE, "w") as f:
        f.write(secret)

    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name="VectwordUser", issuer_name="Vectword")
    qr = qrcode.make(totp_uri)
    qr.save("assets/totp_qr.png")
    print("📷 Scan 'assets/totp_qr.png' with Google Authenticator.")

def verify_totp(code):
    if not os.path.exists(TOTP_SECRET_FILE):
        return False
    with open(TOTP_SECRET_FILE, "r") as f:
        secret = f.read()
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
