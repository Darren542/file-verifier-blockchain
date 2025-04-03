import sys
import os
import hashlib
import json
from web3 import Web3

# === CONFIG ===
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# === Load ABI ===
with open("FileRegistry_abi.json") as f:
    abi = json.load(f)

# === Connect to blockchain ===
# w3 = Web3(Web3.HTTPProvider(RPC_URL))
# contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)

# === Hash a file ===
def hash_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

# === Upload hash to blockchain ===
def upload_file(filepath, address, private_key, contract_address, rpc_url):
    filename = os.path.basename(filepath)
    filehash = hash_file(filepath)

    print(f"Uploading {filename} with hash {filehash}...")

    w3 = Web3(Web3.HTTPProvider(rpc_url))
    contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)

    nonce = w3.eth.get_transaction_count(address)

    txn = contract.functions.addFileVersion(filename, filehash).build_transaction({
        "from": address,
        "nonce": nonce,
        "gas": 200000,
        "gasPrice": w3.to_wei("1", "gwei")
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

    print(f"Sent transaction: {tx_hash.hex()}")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction mined in block {receipt.blockNumber}")

# === CLI Entry Point ===
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python upload_file.py path/to/file")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print("File not found.")
        sys.exit(1)

    upload_file(filepath)
