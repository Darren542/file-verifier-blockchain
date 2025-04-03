import os
import hashlib
import json
from web3 import Web3

# === CONFIG ===
FOLDER_TO_SCAN = "../myfiles"  # or any local test folder
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# === LOAD ABI ===
with open("FileRegistry_abi.json") as f:
    abi = json.load(f)

# === CONNECT TO BLOCKCHAIN ===
# w3 = Web3(Web3.HTTPProvider(RPC_URL))
# contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)

# === HASH FUNCTION ===
def hash_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

# === SCAN & COMPARE ===
def check_files(folder, contract_address, rpc_url):
    print(f"📁 Scanning folder: {folder}\n")
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if not os.path.isfile(filepath): continue

        local_hash = hash_file(filepath)

        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url))
            contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
            latest = contract.functions.getLatestFileVersion(filename).call()
            blockchain_hash = latest[1]  # .hash field
            version = latest[2]

            if local_hash == blockchain_hash:
                print(f"{filename}: Verified (v{version})")
            else:
                print(f"{filename}: Outdated (v{version} on blockchain)")

        except Exception as e:
            print(f"{filename}: Not found on blockchain")
