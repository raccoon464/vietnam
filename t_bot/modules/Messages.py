from datetime import datetime, timezone
from django.utils.translation import gettext as _

from t_bot.config.main import API
from t_bot.models import User
from t_bot.modules import Helper

DEFAULT_OPTION = "default_options"


def save_message(data, chat, message_id, options=DEFAULT_OPTION):
    return Message.objects.create(
                profile=User.objects.get(telegram_id=chat),
                message_id=message_id,
                message_text=data,
                created_at=datetime.now(timezone.utc),
                options=options,
                status=1
            )


def exchange_message_text(obj, message_text, message_id=''):
    obj = Message.objects.get(id=obj.id)
    obj.message_text = message_text
    if message_id:
        obj.message_id = int(message_id)
    obj.save()


def exchange_status(data, status):
    obj = data
    obj.status = status
    obj.save()


def exchange_options2(obj, data):
    obj.options = data
    obj.save()


def exchange_options(m_id, options):
    obj = Message.objects.get(id=m_id)
    obj.options = options
    obj.save()

def last_message(user):
    try:
        m = Message.objects.filter(profile=user).order_by('-id')[0]
        if m.status == 1:
            return  m
        else: return False
    except:
        return False



