from solcx import compile_standard, install_solc
import json
from web3 import Web3
from flask import Flask, request, jsonify,render_template,redirect,url_for
from web3 import Web3
from web3.exceptions import InvalidAddress

with open("./cont.sol", "r") as file:
    cont = file.read()
install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "deploy.sol": {
                "content": cont
            }
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                }
            }
        }
    },
    solc_version="0.6.0"
) 

with open("compiler_code.json","w") as file:
    json.dump(compiled_sol,file)

#getting bytecode
bytecode = compiled_sol["contracts"]["deploy.sol"]["Ledger"]["evm"]["bytecode"]["object"]

#get abi
abi =compiled_sol["contracts"]["deploy.sol"]["Ledger"]["abi"]

#for connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://URL"))
chain_id = 1337
my_address = "ENTER YOUR ADDRESS"
private_key ="ENTER YOUR PRIVATE KEY"

#create contract in py
deploy= w3.eth.contract(abi=abi , bytecode=bytecode)
#get the latest transaction 
nonce= w3.eth.get_transaction_count(my_address)

#steps
#1 build a transaction
#2 sign a transaction
#3 send a transaction
transaction = deploy.constructor().build_transaction({"chainId":chain_id,"from":my_address,"nonce":nonce})  #simple_storage = ledger

signed_txn = w3.eth.account.sign_transaction(transaction,private_key=private_key)

#send this signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

ledger = w3.eth.contract(address=tx_receipt.contractAddress,abi=abi)


# ledger_transaction = ledger.functions.addEntry("first").build_transaction(              #use this to add the transaction
#     {"chainId":chain_id,"from":my_address,"nonce":nonce+1}
# )
# signed_store_txn =w3.eth.account.sign_transaction(
#     ledger_transaction,private_key=private_key
# )

# send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
# tx_receipt=w3.eth.wait_for_transaction_receipt(send_store_tx)
# print(ledger.functions.getEntries().call()) #4:18:00                            #from here we will get the json file of final files



#flask work

app = Flask(__name__)
if w3.is_connected():
    print("Connected to Ethereum network")
else:
    print("Connection to Ethereum network failed")

contract_abi = abi
contract_address =tx_receipt.contractAddress

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Ensure that you pass a valid address when making transactions
try:
    assert w3.is_address(contract_address)
except InvalidAddress:
    print(f"Invalid contract address: {contract_address}")
    exit(1)

# Define a custom function to convert the returned data to a format that works
def format_data(data):
    formatted_data = []
    for entry in data:
        formatted_entry = {
            "user": entry[0],
            "data": entry[1]
        }
        formatted_data.append(formatted_entry)
    return formatted_data


#home
@app.route('/')
def welcome():
    return render_template('form.html')

@app.route("/ledgerinfo",methods=['POST','GET'])
def add_entry():
    res=""
    resulted_output=ledger.functions.getEntries().call()
    if request.method == "POST":
        res = request.form['entry']
        # return jsonify({"message": "Entry added successfully"})
        ledger_transaction = ledger.functions.addEntry(res).build_transaction(              #use this to add the transaction
        {"chainId":chain_id,"from":my_address,"nonce":w3.eth.get_transaction_count(my_address) }
        )
        signed_store_txn =w3.eth.account.sign_transaction(
        ledger_transaction,private_key=private_key
        )
        send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
        tx_receipt=w3.eth.wait_for_transaction_receipt(send_store_tx)
        resulted_output=ledger.functions.getEntries().call()
        return resulted_output
    if request.method == "GET":
        return resulted_output
    return res

# @app.route("/get_entries", methods=["GET"])
# def get_entries():
#     # if request.method == "GET":
#     #     # Retrieve entries from the smart contract
#     #     try:
#     #         entries = contract.functions.getEntries().call()
#     #         formatted_entries = format_data(entries)
#     #         return jsonify({"entries": formatted_entries})
#     #     except Exception as e:
#     #         return jsonify({"error": str(e)})
#     return resulted_output

if __name__ == "__main__":
    app.run(debug=True)
