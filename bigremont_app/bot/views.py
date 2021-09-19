from django.template.loader import render_to_string

from bigremont_app.bot.bot import save_state, Bot


@save_state("/")
def welcome(bot: Bot, **kwargs):
    message = "Добро пожаловать!"
    bot.send_message(message, bot.keyboard.main())

