import json
import os
from encryptor import encrypt_data, decrypt_data

VAULT_FILE = "data/vault.enc"

def save_vault(vault_dict, key):
    encrypted = encrypt_data(json.dumps(vault_dict), key)
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)

def load_vault(key):
    if not os.path.exists(VAULT_FILE):
        return {}
    with open(VAULT_FILE, "rb") as f:
        encrypted = f.read()
    try:
        decrypted = decrypt_data(encrypted, key)
        return json.loads(decrypted)
    except:
        return None
