# Blockchain File Verifier

This project is a blockchain-based system for **file integrity** and **version control**. It uses a smart contract to store file hashes and version history on a **local Ethereum blockchain** (via Hardhat), and provides **Python scripts** to:

- ✅ Scan local files for verification
- 📤 Upload new file versions
- 🔍 Check file integrity
- 🔄 Transfer Ownership of files
- 🔐 Support multiple users

## 📦 Project Structure
```plaintext
file-verifier-blockchain/
├── contracts/ # Solidity smart contracts
│ └── FileRegistry.sol
├── test/ # Contract tests
│ └── FileRegistry.js
├── scripts/
│ └── deploy.js # Contract deployment script
├── scanner/ # Python client tools
│ ├── main.py # Console interface
│ ├── scanner.py # File scan logic
│ ├── upload_file.py # Upload logic
│ ├── FileRegistry_abi.json
| ├── user_config.json # generated by upload_file.py
│ ├── accounts.txt # paste hrdhat accounts here
│ ├── requirements.txt # Python dependencies
| ├── .env # environment variables
│ └── gen_users.py # generate user_config.json
├── artifacts/ # Auto-generated by Hardhat
├── hardhat.config.js
├── package.json
├── README.md
```

---

## 🚀 Prerequisites

- [Node.js v20](https://nodejs.org/) (recommended)
- [Python 3.10+](https://www.python.org/)
- [Hardhat](https://hardhat.org/) for local Ethereum development
- `pip`, `venv`, etc.

---

## ⚙️ 1. How The Hardhat Project  Initialy Created

```bash
npm init -y
npm install --save-dev hardhat
npx hardhat  # choose "Create a JavaScript project"
npm install --save-dev @nomicfoundation/hardhat-toolbox
```

---

## 🧪 2. Test the Contract

Write tests in test/FileRegistry.js, then run:
```bash
npx hardhat test
```

---

## 🧱 3. Deploy Locally

Start the local blockchain:
```bash
npx hardhat compile
npx hardhat node
```

In another terminal, deploy the contract:
```bash
npx hardhat run scripts/deploy.js --network localhost
```

Copy the deployed contract address from the output into the scanner/.env file.

---

## 🐍 4. Set Up Python Scripts

Navigate to the scanner/ folder:

```bash
cd scanner
python -m venv venv
venv\Scripts\activate  # On Windows
# or source venv/bin/activate on macOS/Linux

pip install -r requirements.txt
```

---

## 🔐 5. Configure Users & Contract Info

### A. Paste Hardhat Accounts
Copy and paste the entire output from **npx hardhat node** into: **scanner/accounts.txt**.

### B. Set Environment Variables
Create a **.env** file in the **scanner/** directory with the following content:

```ini
CONTRACT_ADDRESS=0xYourDeployedContractAddress
RPC_URL=http://127.0.0.1:8545
```

---

## ⚙️ 6. First-Time User Setup

When you run the app, if user_config.json doesn’t exist:

- It will auto-generate it from accounts.txt
- Assign default users like alice, bob, charlie with password password123

---

## 🧪 7. Run the Python Console App

```bash
cd scanner
python main.py
```
Choose:
- `1` Scan a directory
- `2` Upload a file
- `3` Transfer ownership
- `4` Exit