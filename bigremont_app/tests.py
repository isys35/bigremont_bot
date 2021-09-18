from django.conf import settings
from django.test import TestCase

from bigremont_app.bot.telegram_context import TelegramContext
from bigremont_app.serializers import UpdateTelegramSerializer

TEST_USER_ID = 1040023542

UPDATE_DATA = {
    "update_id": 157861985,
    "message": {
        "message_id": 10,
        "from": {
            "id": 1040023542,
            "is_bot": False,
            "first_name": "DZMITRY",
            "last_name": "DRAZDOU",
            "username": "dzmitrydrazdou",
            "language_code": "en"
        },
        "chat": {
            "id": 1040023542,
            "first_name": "DZMITRY",
            "last_name": "DRAZDOU",
            "username": "dzmitrydrazdou",
            "type": "private"
        },
        "date": 1627308878,
        "text": "/start"
    }
}


class TestTelegramContext(TestCase):

    def test_send_message(self):
        telegram_context = TelegramContext(settings.TELEGRAM_TOKEN)
        message = telegram_context.send_message(TEST_USER_ID, 'Это тестовое сообщение')
        telegram_context.delete_message(message.chat.id, message.message_id)

    def test_get_user(self):
        telegram_context = TelegramContext(settings.TELEGRAM_TOKEN)
        user = telegram_context.get_user(UpdateTelegramSerializer(**UPDATE_DATA))
        self.assertEqual(user.callback, None)
        self.assertEqual(user.full_request, '/start')
        self.assertEqual(user.initialized, True)
        self.assertEqual(user.request, 'start')
        self.assertEqual(user.state, '/')
