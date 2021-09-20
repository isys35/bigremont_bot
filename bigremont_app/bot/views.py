from django.core.paginator import Paginator
from django.template.loader import render_to_string

from bigremont_app.bot.bot import save_state, Bot
from bigremont_app.models import RemontObject, WorkType, Material, Application, ApplicationMaterial
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
    work_type_page_number = params.get('worktype_page_number')
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
        added_materials = ApplicationMaterial.objects.\
            annotate(material_name='material__name', material_unit='material__unit_measurement').\
            filter(application_id=application_id)
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
    bot.send_message(message, bot.keyboard.objects(paginator.page(page)))
    state = f'/выбрать объект/{object_page_number}/{object_id}/{work_type_page_number}/{worktype_id}/{application.id}/{page}'
    bot.user.save_state(state)


# TODO: слишком длинный список параметров,
#  из **kwargs тоже не особо хочется доставать.
#  Возможно это исправится, если вьхи оформить через класс
def next_page_select_material(bot: Bot, **kwargs):
    material_page_number = kwargs.get('material_page_number')
    page = int(material_page_number) + 1
    kwargs['material_page_number'] = str(page)
    select_worktype(bot, **kwargs)


def previos_page_select_material(bot: Bot, **kwargs):
    material_page_number = kwargs.get('material_page_number')
    page = int(material_page_number) - 1
    kwargs['material_page_number'] = str(page)
    select_worktype(bot, **kwargs)