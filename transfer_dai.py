#!/usr/bin/python3

from eth_account import Account
from web3 import Web3, HTTPProvider
from web3.gas_strategies.time_based import medium_gas_price_strategy
import dai
import config

w3 = Web3(HTTPProvider(config['DEFAULT']['EthereumNode'],request_kwargs={'timeout':60}))
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

dai_contract_address = Web3.toChecksumAddress("0xad6d458402f60fd3bd25163575031acdce07538d")

contract_instance = w3.eth.contract(address=dai_contract_address, abi=dai.contract_abi)

print(contract_instance.functions.name().call())

private_key = w3.sha3(text = config['DEFAULT']['PrivateKeySecret'])
acct = w3.eth.account.privateKeyToAccount(private_key)
print ('account_address: ', acct.address)

print('amount: ', contract_instance.functions.balanceOf(acct.address).call() / 10**18)



transaction = contract_instance.functions.transfer(config['DEFAULT']['MetaMaskAddress'], 10*10**18).buildTransaction()
transaction.update({ 'nonce' : w3.eth.get_transaction_count(acct.address) })
signed_tx = w3.eth.account.sign_transaction(transaction, private_key)

print('signed: ', signed_tx)
print('transaction: ', transaction)

txn_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print ('receipt: ', txn_receipt)

exit()
