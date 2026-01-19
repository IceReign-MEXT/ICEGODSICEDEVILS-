import os, time, requests, threading, json
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler

load_dotenv()

# --- GLOBALS ---
API_KEY = os.getenv("JUP_API_KEY")
MY_PUBKEY = os.getenv("MY_PUBLIC_KEY")
HEADERS = {"x-api-key": API_KEY, "Content-Type": "application/json"}

# --- JUPITER FUNCTIONS ---

def get_quote(input_mint, output_mint, amount_lamports):
    """Fetches a quote with a 1% platform fee included."""
    url = "https://api.jup.ag/swap/v1/quote"
    params = {
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": amount_lamports,
        "slippageBps": 100,      # 1% slippage
        "platformFeeBps": 100    # YOUR 1% PROFIT
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        return r.json()
    except Exception as e:
        print(f"❌ Quote Error: {e}")
        return None

def execute_swap(quote_res):
    """Builds the swap transaction."""
    url = "https://api.jup.ag/swap/v1/swap"
    payload = {
        "quoteResponse": quote_res,
        "userPublicKey": MY_PUBKEY,
        "feeAccount": MY_PUBKEY, # Direct fee to your wallet
        "wrapAndUnwrapSol": True,
        "dynamicComputeUnitLimit": True,
        "prioritizationFeeLamports": "auto"
    }
    try:
        r = requests.post(url, json=payload, headers=HEADERS, timeout=10)
        return r.json().get("swapTransaction")
    except Exception as e:
        print(f"❌ Swap Error: {e}")
        return None

# --- MAIN ENGINE ---

def hunt():
    print("🚀 ICE HUNTER STARTING...")

    # --- IMMEDIATE CONNECTION TEST ---
    print("📡 Testing API Key & Connection...")
    test = get_quote("So11111111111111111111111111111111111111112", 
                     "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", 10000000)

    if test and "outAmount" in test:
        print("✅ CONNECTION VERIFIED: Jupiter Dashboard will now show activity.")
    else:
        print("⚠️ WARNING: API Key test failed. Check JUP_API_KEY in Render.")

    # --- THE TRADING LOOP ---
    while True:
        # This is where the bot waits for new token alerts from your Telegram/Scanner
        # Once an alert hits, it calls get_quote() and execute_swap()
        time.sleep(15)

# --- RENDER HEALTH CHECKER (KEEP-ALIVE) ---
def run_pinger():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), type('H', (BaseHTTPRequestHandler,), 
        {'do_GET': lambda s: s.send_response(200) or s.end_headers() or s.wfile.write(b"ALIVE")}))
    print(f"🌐 Health Check Server live on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=run_pinger, daemon=True).start()
    hunt()

