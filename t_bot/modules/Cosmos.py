from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet, Wallet
from cosmpy.crypto.keypairs import PrivateKey
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins
from cosmpy.aerial.tx import Transaction
from cosmpy.aerial.client.utils import prepare_and_broadcast_basic_transaction
from cosmpy.protos.cosmos.distribution.v1beta1.tx_pb2 import MsgWithdrawValidatorCommission

from t_bot.modules import MP_explorer, Coingeco, Helper

CHAIN_ID = "mineplex-mainnet-1"
URL_GRPC = "grpc+http://164.68.98.163:9090"
FEE_MINIMUM = 10000000000000
FEE_DENOM = "mpx"
FEE_DENOM_XFI = "xfi"
STAKING_DENOM = "mpx"
PREFIX = "mx"

def config(chain_id=CHAIN_ID, url=URL_GRPC, fee_minimum=FEE_MINIMUM, fee_denom=FEE_DENOM):
    cfg = NetworkConfig(
        chain_id=chain_id,
        url=url,
        fee_minimum_gas_price=fee_minimum,
        fee_denomination=fee_denom,
        staking_denomination=STAKING_DENOM,
    )
    return LedgerClient(cfg)

def get_wallet(mnemonic):
    # return wallet
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    bip44_def_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.COSMOS).DeriveDefaultPath()
    return LocalWallet(PrivateKey(bip44_def_ctx.PrivateKey().Raw().ToBytes()), prefix=PREFIX)

def get_balance(address, denom=STAKING_DENOM, ledger=config()):
    return ledger.query_bank_balance(address, denom=denom)

def get_all_balance(address, ledger=config()):
    return ledger.query_bank_all_balances(address)

def staking_of_address(address, ledger=config()):
    return ledger.query_staking_summary(address)

def send_tokens(wallet, destination_address, amount, denom=STAKING_DENOM, ledger=config() ):
    tx = ledger.send_tokens(destination_address, Helper.create_amount_mpx(amount), denom, wallet)
    return tx.wait_to_complete()._response

def delegate_tokens(wallet, validator_address, amount, ledger=config() ):
    tx = ledger.delegate_tokens(validator_address, Helper.create_amount_mpx(amount),  wallet)
    return tx.wait_to_complete()._response

def redelegate_tokens(wallet, validator_address, alternate_validator_address, amount, ledger=config() ):
    tx = ledger.redelegate_tokens(validator_address, alternate_validator_address, Helper.create_amount_mpx(amount), wallet)
    return tx.wait_to_complete()._response

def undelegate_tokens(wallet, validator_address, amount, ledger=config() ):
    tx = ledger.undelegate_tokens(validator_address, Helper.create_amount_mpx(amount),  wallet)
    return tx.wait_to_complete()._response

def claim_rewards(wallet, validator_address, ledger=config() ):
    tx = ledger.claim_rewards(validator_address, wallet)
    return tx.wait_to_complete()._response

def validator_commission(wallet, validator_address, ledger=config()):
    tx = Transaction()
    tx.add_message(
        MsgWithdrawValidatorCommission(
            validator_address=validator_address
        )
    )
    tx = prepare_and_broadcast_basic_transaction(ledger, tx, wallet)
    return tx.wait_to_complete()._response