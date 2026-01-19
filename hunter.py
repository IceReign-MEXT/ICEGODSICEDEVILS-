import os, time, requests, threading
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler

load_dotenv()

# --- CONFIG ---
API_KEY = os.getenv("JUP_API_KEY")
HEADERS = {"x-api-key": API_KEY, "Content-Type": "application/json"}
MY_ADDR = os.getenv("MY_WALLET_ADDRESS")

# --- 1. GET PRICE (V2) ---
def get_price(mint):
    url = f"https://api.jup.ag/price/v2?ids={mint}"
    try:
        res = requests.get(url, headers=HEADERS).json()
        return float(res['data'][mint]['price'])
    except: return 0

# --- 2. THE MONEY MAKER (Direct Fee Quote) ---
def get_quote(input_mint, output_mint, amount):
    # platformFeeBps=100 takes 1% fee automatically
    url = f"https://api.jup.ag/swap/v1/quote?inputMint={input_mint}&outputMint={output_mint}&amount={amount}&slippageBps=100&platformFeeBps=100"
    try:
        return requests.get(url, headers=HEADERS).json()
    except: return None

# --- 3. EXECUTE SWAP (Direct Fee Account) ---
def execute_swap(quote_response):
    url = "https://api.jup.ag/swap/v1/swap"
    payload = {
        "quoteResponse": quote_response,
        "userPublicKey": MY_ADDR,
        # Direct Fee: Send 1% to your wallet's Token Account
        "feeAccount": MY_ADDR,
        "wrapAndUnwrapSol": True,
        "dynamicComputeUnitLimit": True,
        "prioritizationFeeLamports": "auto"
    }
    try:
        res = requests.post(url, json=payload, headers=HEADERS).json()
        return res.get("swapTransaction")
    except: return None

# --- MAIN LOOP ---
def hunt():
    print(f"🎯 Hunting on api.jup.ag | Target: $10 | Fee: 1% Direct")
    while True:
        # Scanning logic here...
        time.sleep(20)

# Keep-alive for Render
def run_pinger():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(("0.0.0.0", port), type('H', (BaseHTTPRequestHandler,), {'do_GET': lambda s: s.send_response(200) or s.end_headers() or s.wfile.write(b"ALIVE")})).serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_pinger, daemon=True).start()
    hunt()

