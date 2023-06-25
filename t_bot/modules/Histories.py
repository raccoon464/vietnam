from t_bot.models import User
from t_bot.models import History
from t_bot.models import NameHistory

from datetime import datetime, timedelta, tzinfo, timezone

from datetime import datetime, timedelta, tzinfo
from decimal import Decimal

from var_dump import var_dump

DEPOSIT = 'Deposit'
WITHDRAWAL = 'Withdrawal'
TRANSFER_GET = 'Transfer_get'
TRANSFER_SET = 'Transfer_set'
TARIFF = 'Tariff'

PROFIT = 'Profit'
REF_PROGRAM = 'Profit_from_ref_program'
DEPOSIT_TO_PROCESS_BALANCE= 'Deposit_to_process_balance'
DEPOSIT_TO_POOL = 'Deposit_to_pool'
WITHDRAWAL_FROM_POOL = 'Withdrawal_from_pool'
TRANSFER_TO_POOL = 'Transfer_to_pool'
RETURN_DEPOSIT = 'Return_deposit'

# VOUCHER= History.NameHistory.get(title='Активация ваучера')
# VOUCHER_DELETE = NameHistory.objects.get(title='Удаление ваучера')


def deposit(user, amount):
    History.objects.create(
        profile=user,
        name=NameHistory.objects.get(title=DEPOSIT),
        description=0,
        amount=Decimal(amount),
        status=1,
        created_at=datetime.now(timezone.utc)
    )

def transfer_set(user, amount, user1, user2):
    History.objects.create(
        profile=user,
        name=NameHistory.objects.get(title=TRANSFER_SET),
        description= user1+ "/" + user2,
        amount=Decimal(amount),
        status=1,
        created_at=datetime.now(timezone.utc)
    )
def transfer_get(user, amount, user2, user1):
    History.objects.create(
        profile=user,
        name=NameHistory.objects.get(title=TRANSFER_GET),
        description= user1+ "/" + user2,
        amount=Decimal(amount),
        status=1,
        created_at=datetime.now(timezone.utc)
    )
def withdrawal(user_id, amount, wallet):
    History.objects.create(
        profile=user_id,
        name= NameHistory.objects.get(title=WITHDRAWAL),
        description=str(wallet),
        amount=Decimal(amount),
        status=2,
        created_at=datetime.now(timezone.utc)
    )

def tariff(user, amount, tariff_name):
    History.objects.create(
        profile=user,
        name= NameHistory.objects.get(title=TARIFF),
        description=tariff_name,
        amount=Decimal(amount),
        status=1,
        created_at=datetime.now(timezone.utc)
    )

def ref_program(user, amount, name_ref):
    History.objects.create(
        profile=user,
        name=NameHistory.objects.get(title=REF_PROGRAM),
        description= name_ref,
        amount=Decimal(amount),
        status=1,
        created_at=datetime.now(timezone.utc)
    )

def profit(user, amount, tariff):
    History.objects.create(
        profile=user,
        name=NameHistory.objects.get(title=PROFIT),
        description=tariff,
        amount=Decimal(amount),
        status=1,
        created_at=datetime.now(timezone.utc)
    )

def return_deposit(user, amount, tariff):
    History.objects.create(
        profile=user,
        name=NameHistory.objects.get(title=RETURN_DEPOSIT),
        description=tariff,
        amount=Decimal(amount),
        status=1,
        created_at=datetime.now(timezone.utc)
    )

def total_depodit(user):
    try:
        history = list(History.objects.filter(profile=user, status=1, name=NameHistory.objects.get(title=DEPOSIT)))
        profit = 0
        for item in history:
            profit += item.amount
        return profit
    except:
        return 0

def total_withdrawal(user):
    try:
        history = list(History.objects.filter(profile=user, name=NameHistory.objects.get(title=WITHDRAWAL)))
        profit = 0
        for item in history:
            if item.status == 1 or item.status == 2: profit += item.amount
        return profit
    except:
        return 0

def total_transfer_set(user):
    try:
        history = list(History.objects.filter(profile=user, status=1, name=NameHistory.objects.get(title=TRANSFER_SET)))
        profit = 0
        for item in history:
            profit += item.amount
        return profit
    except:
        return 0

def total_transfer_get(user):
    try:
        history = list(History.objects.filter(profile=user, status=1, name=NameHistory.objects.get(title=TRANSFER_GET)))
        profit = 0
        for item in history:
            profit += item.amount
        return profit
    except:
        return 0
















def total_profit(user):
    try:
        history = list(History.objects.filter(profile=user, name=NameHistory.objects.get(title=PROFIT)))
        profit = 0
        for item in history:
            profit += item.amount
        return profit
    except:
        return 0

def profit_user_partners(user):
    try:
        history = list(History.objects.filter(profile=user, name=NameHistory.objects.get(title=REF_PROGRAM)))
        profit = 0
        for item in history:
            profit += item.amount
        return profit
    except:
        return 0

def total_plex(user):
    try:
        history = list(History.objects.filter(profile=user, status=1, name=NameHistory.objects.get(title=DEPOSIT_TO_BALANCE_PLEX)))
        profit = 0
        for item in history:
            profit += item.amount
        return profit
    except:
        return 0



def total_transfer_plex_set(user):
    try:
        history = list(History.objects.filter(profile=user, name=NameHistory.objects.get(title=TRANSFER_PLEX_SET)))
        profit = 0
        for item in history:
            profit += item.amount
        return profit
    except:
        return 0

def total_transfer_mine_set(user):
    try:
        history = list(History.objects.filter(profile=user, name=NameHistory.objects.get(title=TRANSFER_MINE_SET)))
        profit = 0
        for item in history:
            profit += item.amount
        return profit
    except:
        return 0

def total_transfer_plex_get(user):
    try:
        history = list(History.objects.filter(profile=user, name=NameHistory.objects.get(title=TRANSFER_PLEX_GET)))
        profit = 0
        for item in history:
            profit += item.amount
        return profit
    except:
        return 0

def total_transfer_mine_get(user):
    try:
        history = list(History.objects.filter(profile=user, name=NameHistory.objects.get(title=TRANSFER_MINE_GET)))
        profit = 0
        for item in history:
            profit += item.amount
        return profit
    except:
        return 0

def last_exchange(user):
    # return 15
    try:
        history = list(History.objects.filter(profile=user, name=NameHistory.objects.get(title=EXCHANGE)).order_by('-id')[:1])
        data = datetime.now(timezone.utc) - history[0].created_at
        return data.days
    except:
        return 360