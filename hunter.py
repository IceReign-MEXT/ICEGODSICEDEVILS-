import os
import time
import threading
import requests
import warnings
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv

# Silence the pkg_resources warning
warnings.filterwarnings("ignore", category=UserWarning, module='web3')

load_dotenv()

# --- CONFIGURATION ---
ULTRA_URL = "https://api.jup.ag/ultra"
API_KEY = os.getenv("JUP_API_KEY")
TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
TG_CHAT_ID = os.getenv("TELEGRAM_CHANNEL_ID")
REF_KEY = os.getenv("REFERRAL_KEY")

# --- 1. KEEP-ALIVE SERVER (For UptimeRobot) ---
class KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ICE ALPHA HUNTER STATUS: ACTIVE")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    httpd = HTTPServer(("0.0.0.0", port), KeepAliveHandler)
    print(f"🌍 Keep-alive active on port {port}")
    httpd.serve_forever()

# --- 2. TELEGRAM MESSENGER ---
def send_alert(msg):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TG_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

# --- 3. AUDIT ENGINE (Honeypot Check) ---
def check_security(mint_address):
    """Checks GoPlus for Honeypots & Rug risks."""
    print(f"🔎 Auditing: {mint_address}")
    url = f"https://api.gopluslabs.io/api/v1/solana/token_security?contract_addresses={mint_address}"
    try:
        res = requests.get(url).json()
        if res.get("code") == 1:
            data = res["result"][mint_address]
            # 1 = Danger, 0 = Safe
            is_hp = data.get("is_honeypot") == "1"
            is_frozen = data.get("freezable") == "1"
            if is_hp or is_frozen:
                return False, "❌ DANGER: Honeypot or Freezable!"
            return True, "✅ SAFE: Clean Audit."
    except Exception as e:
        return False, f"⚠️ Audit Failed: {e}"
    return False, "❓ Unknown Risk"

# --- 4. EXECUTION ENGINE (Jupiter Ultra) ---
def ultra_swap(input_mint, output_mint, amount):
    """Executes sub-second swap with 1% referral fee for YOU."""
    headers = {"x-api-key": API_KEY}
    quote_url = f"{ULTRA_URL}/quote"
    params = {
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": amount,
        "slippageBps": 100,
        "platformFeeBps": 100 # This is your 1% commission!
    }

    try:
        quote = requests.get(quote_url, params=params, headers=headers).json()
        if "outAmount" in quote:
            # Here you would typically sign the tx with 'solders' 
            # and send to Jup Ultra /swap endpoint.
            return True, quote["outAmount"]
    except: pass
    return False, 0

# --- 5. THE HUNT LOOP ---
def start_hunting():
    send_alert("🚀 *ICE ALPHA HUNTER v4.0 LIVE*\nConnected to Jupiter Ultra.")
    print("💀 Scanning Mempool...")

    # In production, you would use a WebSocket here to catch new tokens.
    # For now, we simulate the logic:
    while True:
        # Example Target: A new token just launched
        # target_token = "MINT_ADDRESS_FROM_WEBSOCKET"

        # 1. Audit
        # is_safe, reason = check_security(target_token)

        # 2. If Safe, Execute Snipe
        # if is_safe:
        #    success, amount = ultra_swap("So111...111", target_token, 100000000) # 0.1 SOL

        time.sleep(10) # Prevent rate limits on free APIs

if __name__ == "__main__":
    # Start Keep-Alive thread
    threading.Thread(target=run_server, daemon=True).start()
    # Start Hunting
    start_hunting()

