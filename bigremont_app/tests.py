from django.conf import settings
from django.test import TestCase

from bigremont_app.bot.telegram_context import TelegramContext

TEST_USER_ID = 1040023542


class TestTelegramContext(TestCase):

    def test_send_message(self):
        telegram_context = TelegramContext(settings.TELEGRAM_TOKEN)
        telegram_context.send_message(TEST_USER_ID, 'Это тестовое сообщение')
