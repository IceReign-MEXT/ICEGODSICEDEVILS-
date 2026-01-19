import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# --- STEP 1: THE KEEP-ALIVE SERVER ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ICE ALPHA HUNTER IS ACTIVE")

def run_dummy_server():
    # Render provides a 'PORT' variable automatically
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    print(f"🌍 Keep-alive server online on port {port}")
    server.serve_forever()

# --- STEP 2: THE BOT LOGIC ---
def hunt():
    print("💀 ICE ALPHA HUNTER: Scanning Mempool...")
    # Add your logic here
    while True:
        pass

if __name__ == "__main__":
    # Start the web server in a background thread
    threading.Thread(target=run_dummy_server, daemon=True).start()

    # Run the bot
    hunt()

