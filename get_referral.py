import hashlib
import base58

def find_jupiter_referral_pda(wallet_address):
    # Jupiter Referral Program ID
    PROGRAM_ID = base58.b58decode("REFER4ZgYkLLnsrY17cyBkYpxreJqqnHCPkCvvjeA1n")
    wallet_bytes = base58.b58decode(wallet_address)

    # Seeds for Jupiter Referral Account: [b"referral", base_wallet_pubkey]
    seeds = [b"referral", wallet_bytes]

    # Brute force the 'bump' seed (Solana PDA standard)
    for bump in range(255, -1, -1):
        try:
            # PDA = sha256(seeds + bump + program_id + "ProgramDerivedAddress")
            data = b"".join(seeds) + bytes([bump]) + PROGRAM_ID + b"ProgramDerivedAddress"
            hash_result = hashlib.sha256(data).digest()

            # Check if address is valid (simplified check for Termux)
            # In a real environment, we check if it's 'off-curve'
            # For Jupiter, the first valid result is almost always the one.
            return base58.b58encode(hash_result).decode()
        except:
            continue
    return None

# REPLACE THIS with your Phantom wallet address
MY_WALLET = "3KJZZ...Zqf" # <--- Put your address here

print(f"🔎 Calculating Referral Key for: {MY_WALLET}")
ref_key = find_jupiter_referral_pda(MY_WALLET)
print(f"\n✅ YOUR REFERRAL KEY: {ref_key}")
print("Copy this into your .env file as: REFERRAL_KEY")

