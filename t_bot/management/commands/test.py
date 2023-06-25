
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet, Wallet
from cosmpy.crypto.keypairs import PrivateKey
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins


from django.core.management.base import BaseCommand
from var_dump import var_dump
from t_bot.modules import MP_explorer, Coingeco, Helper, Cosmos,XFI_explorer
from decimal import Decimal
def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e

    return inner


class Command(BaseCommand):
    help = 'setWebhook'



    def handle(self, *args, **options):
        var_dump(XFI_explorer.price_xfi())
        # mnemonic = "extend day mean park cannon hungry loyal matrix property crunch enemy cool"
        # seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
        # bip44_def_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.COSMOS).DeriveDefaultPath()
        #
        # wallet = LocalWallet(PrivateKey(bip44_def_ctx.PrivateKey().Raw().ToBytes()), prefix="mx")
        # # r = Cosmos.validator_commission(wallet, 'mxvaloper15vaxer4jfr2mhg6qaqspr0z44aj3jvfepw9kf4')
        #
        # # r = Cosmos.send_tokens(wallet, 'mx175jyetpvdtrg4xqhdmrxytcmraw7g6cx666mda', 3)
        # var_dump(wallet)


        # cfg = NetworkConfig(
        #     chain_id="mineplex-mainnet-1",
        #     url="grpc+http://164.68.98.163:9090",
        #     fee_minimum_gas_price=10000000000000,
        #     fee_denomination="mpx",
        #     staking_denomination="mpx",
        #
        # )
        # ledger = LedgerClient(cfg)
        # a = ledger.query_bank_all_balances('mx12qsp97p4rzpseeayey3ttye5y449s4tfynntd2')
        # var_dump(a)
        # # s = ledger.query_staking_summary('mx12qsp97p4rzpseeayey3ttye5y449s4tfynntd2')
        # # print(f"Summary: Staked: {s.total_staked} Unbonding: {s.total_unbonding} Rewards: {s.total_rewards}")
        #
        #
        #
        # pass

        #
        # validator_address = 'mxvaloper12qsp97p4rzpseeayey3ttye5y449s4tfsc24v4'
        # tx = ledger.delegate_tokens(validator_address, Helper.create_amount_mpx(1), wallet)
        #
        # var_dump(tx.wait_to_complete()._response)
        #
        # pass

        # mnemonic = "extend day mean park cannon hungry loyal matrix property crunch enemy cool"
        # seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
        # bip44_def_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.COSMOS).DeriveDefaultPath()
        #
        # wallet = LocalWallet(PrivateKey(bip44_def_ctx.PrivateKey().Raw().ToBytes()), prefix="mx")
        #
        # pass

        # cfg = NetworkConfig(
        #     chain_id="cosmoshub-4",
        #     url="grpc+https://cosmoshub-grpc.lavenderfive.com:443",
        #     fee_minimum_gas_price=1,
        #     fee_denomination="uatom",
        #     staking_denomination="uatom",
        # )
        # ledger_client = LedgerClient(cfg)
        # balance = ledger_client.query_bank_balance('cosmos1ak3feyld2pysv0dhxchu46wscw4p5znmjc75gd')
        # var_dump(balance)
        #
        # pass


        # ledger = LedgerClient(NetworkConfig.fetch_mainnet())
        # balance = ledger.query_bank_balance('fetch17zr49k6tmcz7eezxgl7x0pfxa9e92h7lfw657k')
        # var_dump(NetworkConfig.fetch_mainnet())
        # var_dump(balance)


    # for infobot

    # ledger.query_bank_all_balances('mx12qsp97p4rzpseeayey3ttye5y449s4tfynntd2') // текущие балансы

    # ledger.query_staking_summary('mx12qsp97p4rzpseeayey3ttye5y449s4tfynntd2') // стейки
    # print(f"Summary: Staked: {s.total_staked} Unbonding: {s.total_unbonding} Rewards: {s.total_rewards}")

    # ledger.query_tx('39992A6F9742FBF0279FCB52E86993112AC4B0A8BA1A0905B68D2687CCE6230B') // транзакции

    # ledger.query_validators() // валидаторы


