import json
from web3 import Web3
import random
import time
from tqdm import tqdm
from loguru import logger
from fake_useragent import UserAgent
import requests

def sleep_indicator(sec):
    for i in tqdm(range(sec), desc='Пауза', bar_format="{desc}: {n_fmt}c /{total_fmt}c {bar}", colour='green'):
        time.sleep(1)

def wallet():
    with open('wallets.txt', 'r') as f:
        wallets = f.read().splitlines()
        return wallets
def proxyy():
    with open('proxyy.txt', 'r') as f:
        proxyy = f.read().splitlines()
        return proxyy

def intToDecimal(qty, decimal):
    return int(qty * int("".join(["1"] + ["0"] * decimal)))



########################### ИЗМЕНЯЕМЫЕ ПАРАМЕТРЫ ##############################################################################

sleep_min = 150  # Спим между кошельками
sleep_max = 300
time_to_conf = 360 #ожидание подтверждения транзакций
Gwei = 20 # если газ выше уходим в ожидание
rpc_eth = "https://rpc.ankr.com/eth"    # Нода Эфира
shuffle = True      # False / True Перемешивать кошельки или нет
referrer = '0xCFC0F4C414E600d12925934d0EaCBcd707475852' #мой реферальный код (считай донат)

############################################################################################################################


def signature(account_addr):
    proxyys = proxyy()
    if proxyys != []:

        proxy = random.choice(proxyys)

        proxies = {
            "http": f'http://{proxy}',
            "https": f'https://{proxy}'
        }
    else:
        proxies = None

    while True:
        try:
            url = f'https://mint.fun/api/mintfun/fundrop/mint?address={account_addr}&referrer={referrer}'
            headers ={'User-Agent':UserAgent().random, 'Referer':f'https://mint.fun/fundrop?ref={referrer}'}
            resp = requests.get(url, headers=headers, proxies=proxies)
            if resp.status_code == 200:
                a = json.loads(resp.text)
                sign = a['signature']
                return sign
        except Exception as err:
            print(err)

def gas_price_chk():
    while True:
        web3 = Web3(Web3.HTTPProvider(rpc_eth))
        current_gas_price = web3.eth.gas_price
        current_gas_price_gwei = web3.from_wei(current_gas_price, 'gwei')
        if round(current_gas_price_gwei, 1) <= Gwei:
            break
        else:
            logger.info(f'GWEI {round(current_gas_price_gwei, 1)}  Ждем Gwei ниже {Gwei}. Сплю 30 секунд')
            sleep_indicator(30)

def mint(private_key, num):
    web3 = Web3(Web3.HTTPProvider(rpc_eth))
    abi ='[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"AlreadyMinted","type":"error"},{"inputs":[],"name":"InvalidAddress","type":"error"},{"inputs":[],"name":"InvalidSignature","type":"error"},{"inputs":[],"name":"InvalidTokenId","type":"error"},{"inputs":[],"name":"MintClosed","type":"error"},{"inputs":[],"name":"NonTransferrable","type":"error"},{"inputs":[],"name":"OnlyOwnerOrMetadataUpdater","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"_fromTokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"_toTokenId","type":"uint256"}],"name":"BatchMetadataUpdate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"MetadataUpdate","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"referrer","type":"address"}],"name":"MinterReferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"uint256[]","name":"ids","type":"uint256[]"}],"name":"adminBurn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"metadataRenderer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"metadataUpdater","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"referrer","type":"address"},{"internalType":"bytes","name":"signature","type":"bytes"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"mintOpen","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"refreshMetadata","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"rewardsDistributor","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"bool","name":"","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"_metadataRenderer","type":"address"}],"name":"setMetadataRenderer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_metadataUpdater","type":"address"}],"name":"setMetadataUpdater","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_mintOpen","type":"bool"}],"name":"setMintOpen","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_rewardsDistributor","type":"address"}],"name":"setRewardsDistributor","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_signer","type":"address"}],"name":"setSigner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"signer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    mint_pass = web3.to_checksum_address('0x0000000000664ceffed39244a8312bD895470803')    # contract mint fun pass
    minter = web3.eth.contract(address=mint_pass, abi=abi)

    account_addr = web3.eth.account.from_key(private_key).address
    logger.info(f'{num}  -  {account_addr}')
    base_fee = web3.eth.fee_history(web3.eth.get_block_number(), 'latest')['baseFeePerGas'][-1]
    priority_max = web3.to_wei(0.35, 'gwei')
    _signature = signature(account_addr)
    tx = minter.functions.mint(referrer, _signature
                ).build_transaction({
                'from': account_addr,
                'nonce': web3.eth.get_transaction_count(account_addr),
                'maxFeePerGas': base_fee + priority_max,
                'maxPriorityFeePerGas': priority_max
                })
    gasLimit = round(web3.eth.estimate_gas(tx))
    tx.update({'gas': gasLimit})

    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    logger.info(f'- Минт !fundrop pass на {account_addr}')
    logger.info('Жду подтверждение...')
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=time_to_conf)

    if tx_receipt['status'] == 1:
        logger.info(f'Сминтил mint.fun !fundrop pass')
        logger.info(f'Tx hash: https://etherscan.io/tx/{tx_hash.hex()}')
        return 1
    elif tx_receipt['status'] == 0:
        logger.warning(f'Не удалось сминтить mint.fun !fundrop pass')
        logger.warning(f'Tx hash: https://etherscan.io/tx/{tx_hash.hex()}')
        return 0


def minter():
    wallets = wallet()

    if shuffle:
        random.shuffle(wallets)

    num = 0
    for private_key in wallets:
        try:
            gas_price_chk()
            num= num+1
            mint(private_key, num)  # Минт pass
            time_wait_wal = random.randint(sleep_min, sleep_max)
            sleep_indicator(time_wait_wal)  # задержка между кошельками
        except Exception as err:
            logger.error(f'{err}')

if __name__ == '__main__':
    try:
        minter()
    except Exception as err:
        print(err)