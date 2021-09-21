from datetime import datetime

from django.core.paginator import Paginator
from django.template.loader import render_to_string
from telegram_bot_calendar import DetailedTelegramCalendar

from bigremont_app.bot.bot import save_state, Bot
from bigremont_app.models import RemontObject, WorkType, Material, Application, ApplicationMaterial, Recipient
from bigremont_bot import settings


@save_state("/")
def welcome(bot: Bot, **kwargs):
    message = render_to_string('welcome_message.html')
    bot.send_message(message, bot.keyboard.main())


@save_state("/")
def main_menu(bot: Bot, **kwargs):
    message = render_to_string('main_menu.html')
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


def next_page_select_object(bot: Bot, object_page_number: str):
    page = int(object_page_number) + 1
    select_object(bot, page)


def previos_page_select_object(bot: Bot, object_page_number: str):
    page = int(object_page_number) - 1
    select_object(bot, page)


def select_worktype(bot: Bot, object_page_number: str, object_id: str, work_type_page_number: str = None):
    # TODO: Можно зарефакторить, но лучше это сделать после написания клааса для вьюх
    remont_object = RemontObject.objects.get(id=object_id)
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


def next_page_select_worktype(bot: Bot, object_page_number: str, object_id: str, work_type_page_number: str):
    page = int(work_type_page_number) + 1
    select_worktype(bot, object_page_number, object_id, str(page))


def previos_page_select_worktype(bot: Bot, object_page_number: str, object_id: str, work_type_page_number: str):
    page = int(work_type_page_number) - 1
    select_worktype(bot, object_page_number, object_id, str(page))


def select_material(bot: Bot, **params):
    object_page_number = params.get('object_page_number')
    worktype_page_number = params.get('worktype_page_number')
    object_id = params.get('object_id')
    worktype_id = params.get('worktype_id')
    material_page_number = params.get('material_page_number')
    application_id = params.get('application_id')
    remont_object = RemontObject.objects.get(id=object_id)
    worktype = WorkType.objects.get(id=worktype_id)
    if not application_id:
        application = Application.objects.create(remont_object_id=object_id, worktype_id=worktype_id)
        added_materials = None
    else:
        application = Application.objects.get(id=application_id)
        added_materials = ApplicationMaterial.objects.filter(application_id=application_id).select_related('material')
    page = material_page_number or 1
    materials = worktype.materials.all().order_by('id')
    if not materials:
        bot.send_message("В базе нету материалов 😔", bot.keyboard.main())
        bot.user.save_state("/")
        return
    paginator = Paginator(materials, settings.PAGINATOR_SIZE)
    сontext = {'object': remont_object,
               'work_type': worktype,
               'application': application,
               'added_materials': added_materials,
               'materials': paginator.page(page)}
    message = render_to_string('application.html', context=сontext)
    bot.send_message(message, bot.keyboard.materials(paginator.page(page), added_materials))
    state = f'/выбрать объект/{object_page_number}/{object_id}/{worktype_page_number}/{worktype_id}/{application.id}/{page}'
    bot.user.save_state(state)


# TODO: слишком длинный список параметров,
#  из **kwargs тоже не особо хочется доставать.
#  Возможно это исправится, если вьхи оформить через класс
def next_page_select_material(bot: Bot, **params):
    material_page_number = params.get('material_page_number')
    page = int(material_page_number) + 1
    params['material_page_number'] = str(page)
    select_worktype(bot, **params)


def previos_page_select_material(bot: Bot, **params):
    material_page_number = params.get('material_page_number')
    page = int(material_page_number) - 1
    params['material_page_number'] = str(page)
    select_worktype(bot, **params)


def input_count_materials_menu(bot: Bot, **params):
    material_id = params.get('material_id')
    material = Material.objects.get(id=material_id)
    bot.send_message('Введите кол-во материалов ({})'.format(material.unit_measurement), bot.keyboard.clear_keyboard())
    bot.user.save_state()


def input_count_materials(bot: Bot, **params):
    object_page_number = params.get('object_page_number')
    object_id = params.get('object_id')
    worktype_page_number = params.get('worktype_page_number')
    worktype_id = params.get('worktype_id')
    application_id = params.get('application_id')
    material_page_number = params.get('material_page_number')
    material_id = params.get('material_id')
    material_count = params.get('material_count')
    ApplicationMaterial.objects.create(material_id=material_id, application_id=application_id, count=material_count)
    select_material(bot,
                    object_page_number=object_page_number,
                    object_id=object_id,
                    worktype_page_number=worktype_page_number,
                    worktype_id=worktype_id,
                    application_id=application_id,
                    material_page_number=material_page_number)


def menu_select_date_of_delivery(bot: Bot, **params):
    bot.send_message("Введите дату поставки в формате dd.mm.yyyy", bot.keyboard.clear_keyboard())
    bot.user.save_state()


def select_date_of_delivery(bot: Bot, **params):
    date_of_delivery_str = params.get('date_of_delivery')
    try:
        date_of_delivery = datetime.strptime(date_of_delivery_str, "%d.%m.%Y")
    except Exception:
        bot.send_message('Не верно введён формат даты', bot.keyboard.clear_keyboard())
        bot.user.request = ''
        menu_select_date_of_delivery(bot, **params)
        return
    object_id = params.get('object_id')
    worktype_id = params.get('worktype_id')
    application_id = params.get('application_id')
    materials = ApplicationMaterial.objects.filter(application_id=application_id).select_related('material')
    remont_object = RemontObject.objects.get(id=object_id)
    worktype = WorkType.objects.get(id=worktype_id)
    application = Application.objects.get(id=application_id)
    application.date_of_delivery = date_of_delivery
    application.save()
    сontext = {'object': remont_object,
               'work_type': worktype,
               'application': application,
               'selected_materials': materials}
    message = render_to_string('application_final.html', context=сontext)
    bot.send_message(message, bot.keyboard.clear_keyboard())
    recepients = Recipient.objects.all()
    for recepient in recepients:
        bot.context.send_message(recepient.telegram_user_id, message)
    main_menu(bot, **params)