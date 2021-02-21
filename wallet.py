# Import libraries and classes
import subprocess
import json
import constants
from dotenv import load_dotenv
import os
import bit
from web3 import Web3
from eth_account import Account

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

load_dotenv()
mnemonic = os.getenv('MNEMONIC')

def derive_wallets(num, coin_str=[]):
number_for_derive = str(num) # number of child keys to generate
wallet = []
for i in range(len(coin_str)):

    coin_choice = getattr(constants, coin_str[i]) #coins from constants.py
    command = f'./derive -g --mnemonic="{mnemonic}" --coin="{coin_choice}" --numderive="{number_for_derive}" --cols=path,address,privkey,pubkey --format=json'

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()

    keys = json.loads(output)
    with_name = {coin_choice : keys}
    dump = json.dumps(with_name, indent = 4)
    wallet.append(with_name)
return wallet

coins = derive_wallets(2,['ETH', 'BTCTEST'])

eth_key = (coins[0]['eth'][0]['privkey'])
btc_test_key = (coins[1]['btc-test'][0]['privkey'])

def priv_key_to_account(coin, priv_key):
if coin == 'eth':
    return Account.privateKeyToAccount(priv_key)
if coin == 'btc-test':
    account_bit = bit.PrivateKeyTestnet(priv_key)
    return account_bit

eth_account = priv_key_to_account('eth', eth_key)
btc_account = priv_key_to_account('btc-test', btc_test_key)

def create_txn(coin, account, recipient, amount):
if coin == 'eth':
    gasEstimate = w3.eth.estimateGas(
    {"from": account.address, "to": recipient, "value": amount}
    )
    return {
        "from": account.address,
        "to": recipient,
        "value": amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(account.address),
    }
if coin == 'btc-test':
    return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

def send_tx(coin, account, recipient, amount):
if coin == 'eth':
    tx_eth = create_tx(coin, account, recipient, amount)
    tx_sign_eth = account.sign_transaction(tx_eth)
    result = w3.eth.sendRawTransaction(sign_tx_eth.rawTransaction)
    print(result.hex())
    return result.hex()
else:
    tx_btctest= create_tx(coin,account,recipient,amount)
    sign_trxns_btctest = account.sign_transaction(trxns_btctest)
    from bit.network import NetworkAPI
    NetworkAPI.broadcast_tx_testnet(sign_trxns_btctest)       
    return tx_hex

print(coins[1]['btc-test'][1])
