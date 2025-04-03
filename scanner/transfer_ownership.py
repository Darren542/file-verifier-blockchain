import json
from web3 import Web3
from utils import load_contract_abi

def transfer_ownership(filename, sender_address, sender_key, new_owner_address, contract_address, rpc_url):
    try:
        # Load ABI
        abi = load_contract_abi()

        # Connect to Web3
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)

        nonce = w3.eth.get_transaction_count(sender_address)
        txn = contract.functions.transferOwnership(filename, new_owner_address).build_transaction({
            "from": sender_address,
            "nonce": nonce,
            "gas": 2000000,
            "gasPrice": w3.to_wei("1", "gwei")
        })

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=sender_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        print(f"Ownership transferred. Tx Hash: {tx_hash.hex()}")

    except Exception as e:
        print(f"Failed to transfer ownership: {e}")
