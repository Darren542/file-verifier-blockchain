import os
import json
from scanner import check_files
from upload_file import upload_file
from gen_users import gen_users
from dotenv import load_dotenv
load_dotenv()

CONFIG_PATH = "user_config.json"
RPC_URL = os.getenv("RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# === Load user config ===
def load_users():
    if not os.path.exists(CONFIG_PATH):
        print("user_config.json not found. Generating from accounts.txt...")
        gen_users()  # Automatically generate from accounts.txt
    with open(CONFIG_PATH) as f:
        return json.load(f)

def select_user(users):
    print("Available Users:")
    for name in users:
        print(f" - {name}")
    username = input("\nEnter your username: ").strip().lower()
    if username not in users:
        print("User not found.")
        return None
    password = input("Enter your password: ").strip()
    user_password = users[username].get("password")
    if password != user_password:
        print("Incorrect password.")
        return None
    return users[username]

def show_menu():
    print("\n=== MENU ===")
    print("1. Scan a directory")
    print("2. Upload a file")
    print("3. Exit")

def main():
    users = load_users()
    if not users:
        print("No users found in user_config.json")
        return

    user = select_user(users)
    if not user:
        return

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            folder = input("Enter folder path to scan: ").strip()
            if os.path.exists(folder):
                check_files(folder, CONTRACT_ADDRESS, RPC_URL)
            else:
                print("Folder not found.")

        elif choice == "2":
            file = input("Enter file path to upload: ").strip()
            if os.path.exists(file):
                upload_file(file, user["address"], user["private_key"], CONTRACT_ADDRESS, RPC_URL)
            else:
                print("File not found.")

        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
