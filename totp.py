import os
import pyotp
import qrcode

SECRET_FILE = "data/totp.secret"   # ✅ THIS WAS MISSING

def setup_totp():
    os.makedirs("data", exist_ok=True)
    os.makedirs("assets", exist_ok=True)

    secret = pyotp.random_base32()

    with open(SECRET_FILE, "w") as f:
        f.write(secret)

    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(
        name="BlackShield",
        issuer_name="BlackShield Password Manager"
    )

    qr = qrcode.make(uri)
    qr_path = "assets/totp_qr.png"
    qr.save(qr_path)

    return qr_path

def verify_totp(code):
    if not os.path.exists(SECRET_FILE):
        return False
    with open(SECRET_FILE, "r") as f:
        secret = f.read()
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
