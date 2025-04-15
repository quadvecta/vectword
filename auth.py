import os
import hashlib
import json

AUTH_FILE = "data/auth.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_master_password(password):
    if not os.path.exists("data"):
        os.makedirs("data")
    with open(AUTH_FILE, "w") as f:
        json.dump({"master_hash": hash_password(password)}, f)

def verify_master_password(password):
    if not os.path.exists(AUTH_FILE):
        return False
    with open(AUTH_FILE, "r") as f:
        data = json.load(f)
    return hash_password(password) == data["master_hash"]
