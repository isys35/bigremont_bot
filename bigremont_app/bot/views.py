from django.core.paginator import Paginator
from django.template.loader import render_to_string

from bigremont_app.bot.bot import save_state, Bot
from bigremont_app.models import RemontObject
from bigremont_bot import settings


@save_state("/")
def welcome(bot: Bot, **kwargs):
    message = "Добро пожаловать!"
    bot.send_message(message, bot.keyboard.main())


def select_object(bot: Bot, page_number=None, **kwargs):
    if page_number is None:
        page = 1
    else:
        page = int(page_number)
    objects = RemontObject.objects.all().order_by('id')
    if not objects:
        bot.send_message("В базе нету объектов 😔", bot.keyboard.main())
        bot.user.save_state("/")
        return
    paginator = Paginator(objects, settings.PAGINATOR_SIZE)
    context = {'objects': paginator.page(page)}
    message = render_to_string('objects.html', context=context)
    bot.send_message(message, bot.keyboard.objects(paginator.page(page)))
    bot.user.save_state(f'/выбрать объект/{page}')


def next_page_select_object(bot: Bot, page_number):
    page = int(page_number) + 1
    select_object(bot, page)


def previos_page_select_object(bot: Bot, page_number):
    page = int(page_number) - 1
    select_object(bot, page)