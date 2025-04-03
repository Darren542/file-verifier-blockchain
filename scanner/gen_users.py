import json
import re

input_path = "accounts.txt"
output_path = "user_config.json"
default_password = "password123"

def gen_users():
    with open(input_path, "r") as f:
        lines = f.readlines()

    users = {}
    usernames = ["alice", "bob", "charlie", "david", "eve", "frank", "grace", "heidi", "ivan", "judy",
                "karen", "leo", "mallory", "nancy", "oliver", "peggy", "quinn", "rick", "sybil", "trent"]

    i = 0
    while i < len(lines):
        if lines[i].startswith("Account"):
            address_match = re.search(r"Account #[0-9]+: (0x[a-fA-F0-9]{40})", lines[i])
            privkey_match = re.search(r"Private Key: (0x[a-fA-F0-9]{64})", lines[i + 1])
            if address_match and privkey_match:
                username = usernames.pop(0)
                address = address_match.group(1)
                private_key = privkey_match.group(1)
                users[username] = {
                    "address": address,
                    "private_key": private_key,
                    "password": default_password
                }
            i += 2
        else:
            i += 1

    with open(output_path, "w") as f:
        json.dump(users, f, indent=2)

    print(f"✅ Created {output_path} with {len(users)} users.")

if __name__ == "__main__":
    gen_users()

