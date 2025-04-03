import json

def load_contract_abi():
    with open("../artifacts/contracts/FileRegistry.sol/FileRegistry.json") as f:
        return json.load(f)["abi"]