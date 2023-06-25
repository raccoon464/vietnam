
import json
from django.utils.translation import LANGUAGE_SESSION_KEY
from var_dump import var_dump
# from bscscan import BscScan
from web3 import Web3, EthereumTesterProvider
from eth_account import Account
import secrets

import requests


YOUR_API_KEY = "35359DCTPJPPB8IZY74FH9BKX34539NRVG"
CONTRACT = "0x0F67A226c385500c68fFa8bb7Fbe0DB15fE65E24"
ABI = json.loads('[{"inputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"symbol","type":"string"},{"internalType":"address","name":"_minter","type":"address"},{"internalType":"address","name":"_settingContract","type":"address"},{"internalType":"address","name":"_recipientCommission","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"previousAdminRole","type":"bytes32"},{"indexed":true,"internalType":"bytes32","name":"newAdminRole","type":"bytes32"}],"name":"RoleAdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleGranted","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"role","type":"bytes32"},{"indexed":true,"internalType":"address","name":"account","type":"address"},{"indexed":true,"internalType":"address","name":"sender","type":"address"}],"name":"RoleRevoked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":true,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"string","name":"externalRecipient","type":"string"},{"indexed":false,"internalType":"string","name":"blockchain","type":"string"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"SwapToken","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"DEFAULT_ADMIN_ROLE","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"blockchainExisting","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"","type":"string"}],"name":"commissionPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"}],"name":"getRoleAdmin","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"grantRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"hasRole","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"renounceRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"role","type":"bytes32"},{"internalType":"address","name":"account","type":"address"}],"name":"revokeRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"toBlockchain","type":"string"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"setCommissionPrice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"toBlockchain","type":"string"},{"internalType":"bool","name":"status","type":"bool"}],"name":"setSwapBlockchain","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"externalRecipient","type":"string"},{"internalType":"string","name":"toBlockchain","type":"string"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"swap","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]')
URL = 'https://eth.llamarpc.com'

def test():
    # INFURA HTTP API
    infura_url = URL  # your uri
    w3 = Web3(Web3.HTTPProvider(infura_url))
    return w3.isConnected()

def create_account():
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    return [private_key, acct.address]



def transfer_bnb(pk, me, to, amount):

    w3 = Web3(Web3.HTTPProvider(URL))

    amount = w3.toWei(amount, 'ether')
    nonce = w3.eth.getTransactionCount(me)


    tx = {
        'nonce': nonce,
        'to': to,
        'value': amount,
        'gas': 21000,
        'gasPrice': w3.toWei(gas_price(), 'gwei'),

    }

    sign_txn = w3.eth.account.signTransaction(tx, private_key=pk)
    tx_hash = w3.eth.sendRawTransaction(sign_txn.rawTransaction)
    return Web3.toHex(tx_hash)

def transfer_mill(pk, me, to, amount, gas = 0):
    w3 = Web3(Web3.HTTPProvider(URL))
    contract = w3.eth.contract(address=CONTRACT, abi=ABI)

    amount = w3.toWei(amount, 'ether')
    nonce = w3.eth.getTransactionCount(me)

    token_tx = contract.functions.transfer(to, amount).buildTransaction({
        'chainId': 56,
        'gas': 50000 + gas,
        'gasPrice': w3.toWei(gas_price(), 'gwei'),
        'nonce': nonce
    })
    sign_txn = w3.eth.account.signTransaction(token_tx, private_key=pk)

    w3.eth.sendRawTransaction(sign_txn.rawTransaction)
    return Web3.toHex(Web3.toBytes(sign_txn.hash).rjust(32, b'\0'))



def get_balance_plex(addres):
    w3 = Web3(Web3.HTTPProvider(URL))
    contract = w3.eth.contract(address=CONTRACT, abi=ABI, )
    balanceOf = contract.functions.balanceOf(addres).call()
    return w3.fromWei(balanceOf, 'mwei')
# https://github.com/ethereum/web3.py/blob/master/docs/examples.rst


def get_balance_eth(addres):
    w3 = Web3(Web3.HTTPProvider(URL))
    balanceOf = w3.eth.get_balance(addres)
    return w3.fromWei(balanceOf, 'ether')

def gas_price():
    w3 = Web3(Web3.HTTPProvider(URL))
    return w3.eth.gas_price