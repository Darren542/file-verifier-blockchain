import os
import hashlib
import json
from web3 import Web3
from utils import load_contract_abi

# === CONFIG ===
FOLDER_TO_SCAN = "../myfiles"  # or any local test folder
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# === LOAD ABI ===
abi = load_contract_abi()

# === HASH FUNCTION ===
def hash_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

# === SCAN & COMPARE ===
def check_files(folder, contract_address, rpc_url):
    print(f"Scanning folder: {folder}\n")
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if not os.path.isfile(filepath): continue

        local_hash = hash_file(filepath)

        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url))
            contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
            latest = contract.functions.getLatestFileVersion(filename).call()

            if not latest:
                print(f"{filename}: Not found on blockchain")
                continue

            blockchain_hash = latest[1]  # .hash field
            lversion = latest[2]

            if local_hash == blockchain_hash:
                print(f"{filename}: Verified (v{lversion})")
            else:
                versions = contract.functions.getAllVersions(filename).call()
                matching_version = None
                for version in versions:
                    if version[1] == local_hash:
                        matching_version = version
                        break
                if matching_version:
                    print(f"{filename}: Version mismatch - this is v{matching_version[2]}, latest is v{lversion}")
                else:
                    print(f"{filename}: Hash not found on blockchain (latest is v{lversion})")

        except Exception as e:
            print(f"{filename}: Not found on blockchain")
