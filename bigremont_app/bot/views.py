from datetime import datetime

from django.core.paginator import Paginator
from django.template.loader import render_to_string

from bigremont_app.bot.bot import save_state, Bot
from bigremont_app.bot.utils import get_date_of_delivery_from_text
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


def select_object(bot: Bot):
    objects = RemontObject.objects.all().order_by('id')
    if not objects:
        bot.send_message("В базе нету объектов 😔", bot.keyboard.main())
        bot.user.save_state("/")
        return
    context = {'objects': objects}
    message = render_to_string('objects.html', context=context)
    bot.send_message(message, bot.keyboard.objects(objects))
    bot.user.save_state(f'/выбрать объект')


def select_worktype(bot: Bot, object_name: str):
    # TODO: Можно зарефакторить, но лучше это сделать после написания клааса для вьюх
    work_types = WorkType.objects.all().order_by('id')
    if not work_types:
        bot.send_message("В базе нету видов работ 😔", bot.keyboard.main())
        bot.user.save_state("/")
        return
    сontext = {'object': object_name,
               'work_types': work_types}
    message = render_to_string('worktypes.html', context=сontext)
    bot.send_message(message, bot.keyboard.objects(work_types))
    bot.user.save_state(f'/выбрать объект/{object_name}')


def select_material(bot: Bot, **params):
    object_name = params.get('object_name')
    worktype_name = params.get('worktype_name')
    material_page_number = params.get('material_page_number')
    application_id = params.get('application_id')
    remont_object = RemontObject.objects.filter(name__icontains=object_name).first()
    worktype = WorkType.objects.filter(name__icontains=worktype_name).first()
    if not application_id:
        application = Application.objects.create(remont_object_id=remont_object.id, worktype_id=worktype.id)
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
    state = f'/выбрать объект/{object_name}/{worktype_name}/{application.id}/{page}'
    bot.user.save_state(state)


# TODO: слишком длинный список параметров,
#  из **kwargs тоже не особо хочется доставать.
#  Возможно это исправится, если вьхи оформить через класс
def next_page_select_material(bot: Bot, **params):
    material_page_number = params.get('material_page_number')
    page = int(material_page_number) + 1
    params['material_page_number'] = str(page)
    select_material(bot, **params)


def previos_page_select_material(bot: Bot, **params):
    material_page_number = params.get('material_page_number')
    page = int(material_page_number) - 1
    params['material_page_number'] = str(page)
    select_material(bot, **params)


def input_count_materials_menu(bot: Bot, **params):
    material_id = params.get('material_id')
    material = Material.objects.get(id=material_id)
    bot.send_message('Введите кол-во материалов ({})'.format(material.unit_measurement), bot.keyboard.clear_keyboard())
    bot.user.save_state()


def input_count_materials(bot: Bot, **params):
    object_name = params.get('object_name')
    worktype_name = params.get('worktype_name')
    application_id = params.get('application_id')
    material_page_number = params.get('material_page_number')
    material_id = params.get('material_id')
    material_count = params.get('material_count')
    ApplicationMaterial.objects.create(material_id=material_id, application_id=application_id, count=material_count)
    select_material(bot,
                    object_name=object_name,
                    worktype_name=worktype_name,
                    application_id=application_id,
                    material_page_number=material_page_number)


def menu_select_date_of_delivery(bot: Bot, **params):
    bot.send_message("Введите дату поставки в формате dd.mm.yyyy или воспользуйтесь клавиатурой 👇", bot.keyboard.date_keyboard())
    bot.user.save_state('/выбрать объект/{object_name}/{worktype_name}/{application_id}/{material_page_number}/завершить выбор материалов'.format(**params))


def select_date_of_delivery(bot: Bot, **params):
    date_of_delivery_str = params.get('date_of_delivery')
    date_of_delivery = get_date_of_delivery_from_text(date_of_delivery_str)
    if not date_of_delivery:
        bot.send_message('Не верно введён формат даты', bot.keyboard.clear_keyboard())
        return
    object_name = params.get('object_name')
    worktype_name = params.get('worktype_name')
    application_id = params.get('application_id')
    materials = ApplicationMaterial.objects.filter(application_id=application_id).select_related('material')
    remont_object = RemontObject.objects.get(name__icontains=object_name)
    worktype = WorkType.objects.get(name__icontains=worktype_name)
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
