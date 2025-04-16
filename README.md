# Vectword

**Vectword** is a secure, local password manager built with Python.  
It features AES-256 encryption, TOTP-based two-factor authentication (2FA), and a simple command-line interface for managing credentials securely.

---

## Features

- 🔐 Master password authentication
- 🛡️ AES-256 encryption for credential storage
- 📱 Two-Factor Authentication using TOTP (compatible with Google Authenticator)
- 🗂️ Add, view, and delete saved credentials
- 📁 Local encrypted vault (no cloud storage)

---

## Getting Started

### Prerequisites

- Python 3.7+
- `pip` for dependency installation

### Installation

1. Clone the repository:

```bash
git clone https://github.com/quadvecta/vectword.git
cd vectword
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

---

## Usage

### Register

- Set a master password (stored as a hash)
- A QR code will be generated for 2FA setup (scan with Google Authenticator)

### Login

- Enter master password
- Enter 6-digit 2FA code from your authenticator app
- Access your encrypted vault

### Vault Commands

| Command | Description                  |
|---------|------------------------------|
| `add`   | Add a new credential entry   |
| `view`  | View all saved credentials   |
| `delete`| Delete an existing entry     |
| `exit`  | Exit and lock the vault      |

---

## Project Structure

```
vectword/
├── main.py          # App entry point
├── auth.py          # Master password logic
├── encryptor.py     # AES encryption/decryption
├── vault.py         # Vault operations
├── totp.py          # TOTP-based 2FA
├── requirements.txt
├── assets/          # QR code image
└── data/            # Encrypted vault (excluded from version control)
```

---

## Dependencies

- [cryptography](https://pypi.org/project/cryptography/)
- [pyotp](https://pypi.org/project/pyotp/)
- [qrcode](https://pypi.org/project/qrcode/)

Install all with:

```bash
pip install -r requirements.txt
```

---

## License

This project is licensed under the MIT License.  
You are free to use, modify, and distribute it for personal or educational purposes.

---

## Disclaimer

Vectword stores all data locally and does not include cloud syncing or remote backup features. Users are responsible for securely maintaining their vault file and 2FA setup.



---
