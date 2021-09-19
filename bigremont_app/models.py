from django.db import models


class TelegramUser(models.Model):
    username = models.CharField(max_length=100, db_index=True, default=None)
    state = models.CharField(max_length=200, default='/')


class RemontObject(models.Model):
    name = models.CharField(max_length=100, db_index=True)
