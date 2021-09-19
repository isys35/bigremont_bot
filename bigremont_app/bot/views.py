from django.core.paginator import Paginator
from django.template.loader import render_to_string

from bigremont_app.bot.bot import save_state, Bot
from bigremont_app.models import RemontObject, WorkType
from bigremont_bot import settings


@save_state("/")
def welcome(bot: Bot, **kwargs):
    message = "Добро пожаловать!"
    bot.send_message(message, bot.keyboard.main())


def select_object(bot: Bot, object_page_number=None, **kwargs):
    page = object_page_number or 1
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


def next_page_select_object(bot: Bot, object_page_number):
    page = int(object_page_number) + 1
    select_object(bot, page)


def previos_page_select_object(bot: Bot, object_page_number):
    page = int(object_page_number) - 1
    select_object(bot, page)


def select_worktype(bot: Bot, object_page_number, object_id, work_type_page_number=None):
    # TODO: Можно зарефакторить, но лучше это сделать после написания клааса для вьюх
    remont_object = RemontObject.objects.filter(id=object_id)
    if not object:
        bot.error_500()
        return
    else:
        remont_object = remont_object.first()
    page = work_type_page_number or 1
    work_types = WorkType.objects.all().order_by('id')
    if not work_types:
        bot.send_message("В базе нету видов работ 😔", bot.keyboard.main())
        bot.user.save_state("/")
        return
    paginator = Paginator(work_types, settings.PAGINATOR_SIZE)
    сontext = {'object': remont_object,
               'work_types': paginator.page(page)}
    message = render_to_string('worktypes.html', context=сontext)
    bot.send_message(message, bot.keyboard.objects(paginator.page(page)))
    bot.user.save_state(f'/выбрать объект/{object_page_number}/{object_id}/{page}')