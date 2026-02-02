import os
import firebase_admin
from firebase_admin import credentials, auth
from src.backend.database import get_db_connection

# Initialize Firebase Admin SDK
cred_path = os.getenv("FIREBASE_CREDENTIALS")
if cred_path and os.path.exists(cred_path):
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
else:
    print("⚠️ Firebase Credentials not found. Using Mock Auth for Development.")
    # In production, this would raise an error.

def register_user(email, password, confirm_password):
    if not email or not password:
        return False, "Email and password are required."
    
    if password != confirm_password:
        return False, "Passwords do not match."

    # Try Firebase Registration
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return True, f"User {user.uid} created successfully due to Firebase!"
    except Exception as e:
        # Fallback for dev without firebase keys
        if "Default Credentials" in str(e) or "Certificate" in str(e) or "app" in str(e):
             # Use naive local auth logic (from previous step, but simplified)
             # NOTE: THIS IS FOR DEV ONLY
             return _mock_register(email, password)
        return False, str(e)

def authenticate_user(email, password):
    # Note: Firebase Admin SDK does NOT support verifying passwords (that's client-side SDK).
    # Since we are server-side Python, typically we verify ID Tokens sent from client.
    # However, for this Gradio app, we can't easily use the JS SDK.
    # We will use the Google Identity Toolkit REST API if Key is present,
    # OR fallback to Mock for this "Start Development" phase.
    
    return _mock_login(email, password)

# --- Mock Implementations for Dev (preserves previous functionality) ---
# In a real "fully developed" app, we'd use the Identity Platform REST API 
# to exchange password for checking, or use a custom backend flow.

import json
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
USERS_FILE = "users.json"

def _load_users():
    if not os.path.exists(USERS_FILE): return {}
    try:
        with open(USERS_FILE, "r") as f: return json.load(f)
    except: return {}

def _save_users(users):
    with open(USERS_FILE, "w") as f: json.dump(users, f)

def _mock_register(username, password):
    users = _load_users()
    if username in users: return False, "User already exists (Local)."
    hashed = pwd_context.hash(password)
    users[username] = {"password": hashed}
    _save_users(users)
    return True, "Registration successful (Local Dev)."

def _mock_login(username, password):
    users = _load_users()
    if username not in users: return False, "Invalid credentials."
    if pwd_context.verify(password, users[username]["password"]):
        return True, "Login successful."
    return False, "Invalid credentials."
