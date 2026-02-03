import os
from dotenv import load_dotenv
from src.frontend.ui import create_ui

# Load environment variables
load_dotenv()

# Configuration
# Cloud Run injects 'PORT', defaulting to 8080. Fallback to GRADIO_SERVER_PORT or 7880 for local.
SERVER_PORT = int(os.getenv("PORT", os.getenv("GRADIO_SERVER_PORT", 7880)))
SERVER_NAME = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")

if __name__ == "__main__":
    # Get auth from env if set, else None
    auth_user = os.getenv("ADMIN_USERNAME")
    auth_pass = os.getenv("ADMIN_PASSWORD")
    auth = (auth_user, auth_pass) if auth_user and auth_pass else None

    print(f"Starting Thesis AI Generator on {SERVER_NAME}:{SERVER_PORT}")
    print("Stack: Google Cloud, Gemini 2.0, Gradio")
    
    app = create_ui()
    app.launch(
        server_name=SERVER_NAME,
        server_port=SERVER_PORT,
        auth=auth
    )
