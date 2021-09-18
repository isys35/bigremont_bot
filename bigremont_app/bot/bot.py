from typing import Union

from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup

from bigremont_app.bot.keyboard import BotKeyboard
from bigremont_app.bot.telegram_context import TelegramContext
from bigremont_app.serializers import UpdateTelegramSerializer


def save_state(state: str = '/'):
    """
    Декоратор для сохранения состояния пользователя после
    выполнения запроса.
    Если state не передается, то сохраняет корневое состояние.
    :param state: str
    :return: _save_state (wrapper)
    """

    def _save_state(function):
        """
        Выполняет запрос, после сохраняет стейт
        :param function:
        :return: wrapper
        """

        def wrapper(bot, **kwargs):
            function(bot, **kwargs)
            bot.user.save_state(state)

        return wrapper

    return _save_state


class Bot:
    context = None
    user = None
    update = None

    def __init__(self, context: TelegramContext, update: UpdateTelegramSerializer):
        self.context = context
        self.keyboard = BotKeyboard(context)
        self.update = update
        self.user = self.context.get_user(update)

    def send_message(self, text: str, markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup] = None):
        return self.context.send_message(self.user.id,
                                         text,
                                         markup)

    def edit_message(self, text: str, message_id: int):
        return self.context.edit_message(self.user.id,
                                         text,
                                         message_id)