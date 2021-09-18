from typing import Union

import telebot

# from telegram_bot.user import User
# from webhook.serializers import UpdateSerializer
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, Message

from bigremont_app.bot.user import User
from bigremont_app.serializers import UpdateTelegramSerializer


class TelegramContext:
    bot = None

    def __init__(self, token: str):
        """
        Инициализирует telebot.TeleBot(token)
        :param token: токен бота в Telegram
        """
        self.bot = telebot.TeleBot(token, threaded=False)

    @staticmethod
    def get_keyboard(buttons: list) -> telebot.types.ReplyKeyboardMarkup:
        """
        Создает и возвращает клавиатуру
        для показа пользователю в Telegram
        :param buttons: список с кнопками
        :return: telebot.types.ReplyKeyboardMarkup
        """
        markup = telebot.types.ReplyKeyboardMarkup(row_width=1,
                                                   resize_keyboard=True)
        for row in buttons:
            markup.row(*row)
        return markup

    def delete_message(self,
                       chat_id: int,
                       message_id: int):
        """
        Удаляет сообщение из чата
        :param chat_id: id чата
        :param message_id:
        :return:
        """
        self.bot.delete_message(chat_id=chat_id, message_id=message_id)

    def send_message(self,
                     receiver: int,
                     text: str,
                     markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup] = None) -> Message:
        """
        Отправляет сообщение пользователю в Telegram.
        :param receiver: id пользователя в Telegram
        :param text: строка с сообщением
        :param markup: клавиатура для показа пользователю
        :return: None
        """
        kwargs = {
            'chat_id': receiver,
            'text': text,
            'disable_web_page_preview': True,
            'disable_notification': True,
            'parse_mode': 'HTML',
            'reply_markup': markup,
            'timeout': 1
        }
        return self.bot.send_message(**kwargs)

    def edit_message(self, receiver: int, text: str, message_id: int):
        kwargs = {
            'chat_id': receiver,
            'text': text,
            'message_id': message_id
        }
        self.bot.edit_message_text(**kwargs)

    @staticmethod
    def get_user(update: UpdateTelegramSerializer):
        user = User(update)
        user.init_from_db()
        if not user.initialized:
            user.init_from_update()
        return user
