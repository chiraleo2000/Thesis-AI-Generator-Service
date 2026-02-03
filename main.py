
import os
import sys

# Force the root directory into sys.path to allow module imports
sys.path.append(os.getcwd())

from dotenv import load_dotenv
from src.frontend.ui import create_ui

# Load environment variables
load_dotenv()

# Configuration
SERVER_PORT = int(os.getenv("PORT", os.getenv("GRADIO_SERVER_PORT", 7880)))
SERVER_NAME = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")

if __name__ == "__main__":
    print(f"🚀 Starting Thesis AI Generator...")
    print(f"📍 Mode: {'Cloud Run' if 'PORT' in os.environ else 'Local/Docker'}")
    print(f"🔌 Port: {SERVER_PORT}")

    app = create_ui()
    
    # Launch with simplified parameters to avoid Gradio version conflicts
    try:
        app.launch(
            server_name=SERVER_NAME,
            server_port=SERVER_PORT,
            show_error=True
        )
    except Exception as e:
        print(f"❌ Gradio Launch Failed: {e}")
