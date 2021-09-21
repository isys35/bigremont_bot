from bigremont_app.bot.views import welcome, select_object, next_page_select_object, previos_page_select_object, \
    select_worktype, previos_page_select_worktype, next_page_select_worktype, select_material, \
    next_page_select_material, previos_page_select_material, input_count_materials_menu, input_count_materials, \
    menu_select_date_of_delivery, select_date_of_delivery, main_menu

urls = [
    (r'<wc:req>/start', welcome),
    (r'<wc:req>/главное меню', main_menu),

    (r'/выбрать объект', select_object),
    (r'/выбрать объект/<int:object_page_number>/следующая страница', next_page_select_object),
    (r'/выбрать объект/<int:object_page_number>/предыдущая страница', previos_page_select_object),

    (r'/выбрать объект/<int:object_page_number>/<int:object_id>', select_worktype),
    (r'/выбрать объект/<int:object_page_number>/<int:object_id>/<int:worktype_page_number>/следующая страница', next_page_select_worktype),
    (r'/выбрать объект/<int:object_page_number>/<int:object_id>/<int:worktype_page_number>/предыдущая страница', previos_page_select_worktype),

    (r'/выбрать объект/<int:object_page_number>/<int:object_id>/<int:worktype_page_number>/<int:worktype_id>', select_material),
    (r'/выбрать объект/<int:object_page_number>/<int:object_id>/<int:worktype_page_number>/<int:worktype_id>/<int:application_id>', select_material),
    (r'/выбрать объект/<int:object_page_number>/<int:object_id>/<int:worktype_page_number>/<int:worktype_id>/<int:application_id>/<int:material_page_number>/следующая страница', next_page_select_material),
    (r'/выбрать объект/<int:object_page_number>/<int:object_id>/<int:worktype_page_number>/<int:worktype_id>/<int:application_id>/<int:material_page_number>/предыдущая страница', previos_page_select_material),
    (r'/выбрать объект/<int:object_page_number>/<int:object_id>/<int:worktype_page_number>/<int:worktype_id>/<int:application_id>/<int:material_page_number>/завершить выбор материалов', menu_select_date_of_delivery),
    (r'/выбрать объект/<int:object_page_number>/<int:object_id>/<int:worktype_page_number>/<int:worktype_id>/<int:application_id>/<int:material_page_number>/завершить выбор материалов/<str:date_of_delivery>', select_date_of_delivery),
    (r'/выбрать объект/<int:object_page_number>/<int:object_id>/<int:worktype_page_number>/<int:worktype_id>/<int:application_id>/<int:material_page_number>/<int:material_id>', input_count_materials_menu),

    (r'/выбрать объект/<int:object_page_number>/<int:object_id>/<int:worktype_page_number>/<int:worktype_id>/<int:application_id>/<int:material_page_number>/<int:material_id>/<int:material_count>', input_count_materials),
    ]