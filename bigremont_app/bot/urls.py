from bigremont_app.bot.views import welcome, select_object, \
    select_worktype, select_material, \
    next_page_select_material, previos_page_select_material, input_count_materials_menu, input_count_materials, \
    menu_select_date_of_delivery, select_date_of_delivery, main_menu

urls = [
    (r'<wc:req>/start', welcome),
    (r'<wc:req>/главное меню', main_menu),

    (r'/выбрать объект', select_object),

    (r'/выбрать объект/<str:object_name>', select_worktype),

    (r'/выбрать объект/<str:object_name>/<str:worktype_name>', select_material),
    (r'/выбрать объект/<str:object_name>/<str:worktype_name>/<int:application_id>', select_material),
    (r'/выбрать объект/<str:object_name>/<str:worktype_name>/<int:application_id>/<int:material_page_number>/следующая страница', next_page_select_material),
    (r'/выбрать объект/<str:object_name>/<str:worktype_name>/<int:application_id>/<int:material_page_number>/предыдущая страница', previos_page_select_material),
    (r'/выбрать объект/<str:object_name>/<str:worktype_name>/<int:application_id>/<int:material_page_number>/завершить выбор материалов', menu_select_date_of_delivery),
    (r'/выбрать объект/<str:object_name>/<str:worktype_name>/<int:application_id>/<int:material_page_number>/завершить выбор материалов/<str:date_of_delivery>', select_date_of_delivery),
    (r'/выбрать объект/<str:object_name>/<str:worktype_name>/<int:application_id>/<int:material_page_number>/<int:material_id>', input_count_materials_menu),

    (r'/выбрать объект/<str:object_name>/<str:worktype_name>/<int:application_id>/<int:material_page_number>/<int:material_id>/<int:material_count>', input_count_materials),
    ]