from django.db import models
import datetime
# Create your models here.
class User(models.Model):
    telegram_id = models.BigIntegerField(verbose_name='id telegram', unique=True)
    name = models.CharField('Name', max_length=100)
    description = models.CharField('Description', max_length=250)
    admin = models.ForeignKey(to='Admin_rule', verbose_name='Admin',  on_delete=models.PROTECT,)
    lang = models.ForeignKey(to='Lang', verbose_name='Lang', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.telegram_id} /  {self.name}'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'




class Message(models.Model):
    profile = models.ForeignKey(
        to='User',
        verbose_name='Profile',
        on_delete=models.PROTECT,
    )
    message_id = models.PositiveIntegerField(
        verbose_name='id message',
        # unique=True,
    )
    message_text = models.TextField(
        verbose_name='text',
    )
    options = models.TextField(
        verbose_name='Option'
    )
    created_at = models.DateTimeField(
        verbose_name='Data',
        # auto_now_add=True,
    )
    status = models.PositiveIntegerField(
        verbose_name='Status',
        # unique=True,
    )

    def __str__(self):
        return f'Сообщение:{self.id} / {self.message_text} от {self.profile.name} =>  {self.status}'

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class Error(models.Model):
    text = models.TextField('text')

    class Meta:
        verbose_name = 'Error'
        verbose_name_plural = 'Error'


class Admin_rule(models.Model):
    name = models.CharField('name', max_length=100)
    rules = models.CharField('rules', max_length=250)

    def __str__(self):
        return f'# {self.id} / {self.name}'



class Lang(models.Model):
    name = models.CharField('Language', max_length=100)
    flag = models.CharField('Flag', max_length=100)
    icon = models.CharField('icon', max_length=5, default=0)

    def __str__(self):
        return f'# {self.id} / {self.name}'

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
