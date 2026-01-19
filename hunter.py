import os
import requests
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Config
ETH_RPC = os.getenv("ETH_RPC_URL")
TG_TOKEN = os.getenv("TELEGRAM_TOKEN")
TG_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
w3 = Web3(Web3.HTTPProvider(ETH_RPC))

def send_telegram_alert(message):
    """Sends a notification to your Telegram channel."""
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"❌ Telegram Error: {e}")

def hunt():
    print("💀 ICE ALPHA HUNTER: Online and Scanning...")
    # Example notification when the bot starts
    send_telegram_alert("🚀 *ICE ALPHA HUNTER v4.0 Status:* Online and Scanning for Zero-Block Liquidity.")

    while True:
        # Your scanning logic here...
        # When a token is found:
        # send_telegram_alert("🎯 *TOKEN DETECTED!* \nAddress: `0x...` \nLiquidity: Locked ✅")
        pass

if __name__ == "__main__":
    hunt()

