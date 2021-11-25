#!/usr/bin/python3

from eth_account import Account
from web3 import Web3, HTTPProvider
from web3.gas_strategies.time_based import medium_gas_price_strategy
import config

w3 = Web3(HTTPProvider(config['DEFAULT']['EthereumNode'],request_kwargs={'timeout':60}))

# block = w3.eth.get_block(12345)
# print(block)
# exit()

private_key = w3.sha3(text = config['DEFAULT']['PrivateKeySecret'])
print('private key:', private_key)

acct = w3.eth.account.privateKeyToAccount(private_key)
# print(acct)
print('address:', acct.address)
print ('balance:', Web3.fromWei(w3.eth.get_balance(acct.address), 'ether'))

tx = dict(
    nonce=w3.eth.get_transaction_count(acct.address),
    maxFeePerGas=3000000000,
    maxPriorityFeePerGas=2000000000,
    gas=100000,
    to=config['DEFAULT']['MetamaskAddress'],
    value=Web3.toWei(0.01, 'ether'),
    data=b'',
    type=2,
    chainId=3,
  )

signed_txn = w3.eth.account.sign_transaction(tx , private_key)
tx_id = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print('signed_txn', signed_txn)
print('tx_id: ', tx_id)

exit()
