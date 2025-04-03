import sys
import os
import hashlib
import json
from web3 import Web3
from web3.exceptions import ContractLogicError, Web3Exception
from utils import load_contract_abi

# === CONFIG ===
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# === Load ABI ===
abi = load_contract_abi()

# === Hash a file ===
def hash_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

# === Upload hash to blockchain ===
def upload_file(filepath, address, private_key, contract_address, rpc_url):
    filehash = hash_file(filepath)
    filename = os.path.basename(filepath)

    print(f"Uploading {filename} with hash {filehash}...")

    try:
        # Connect to blockchain
        with open("FileRegistry_abi.json") as f:
            abi = json.load(f)

        w3 = Web3(Web3.HTTPProvider(rpc_url))
        contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)

        nonce = w3.eth.get_transaction_count(address)
        func = contract.functions.addFileVersion(filename, filehash)

        gas_estimate = func.estimate_gas({"from": address})
        txn = func.build_transaction({
            "from": address,
            "nonce": nonce,
            "gas": gas_estimate + 10000,
            "gasPrice": w3.to_wei("1", "gwei")
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        print(f"File uploaded successfully. Tx Hash: {tx_hash.hex()}")

    except ContractLogicError as e:
        # Display smart contract revert reason
        message = str(e)
        if "reverted with reason string" in message:
            reason = message.split("reverted with reason string '")[1].split("'")[0]
            print(f"Reverted: {reason}")
        else:
            print(f"Contract reverted: {message}")
    except Web3Exception as e:
        print(f"Web3 error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
