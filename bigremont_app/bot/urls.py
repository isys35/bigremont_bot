from bigremont_app.bot.views import welcome, select_object, next_page_select_object, previos_page_select_object, \
    select_worktype, previos_page_select_worktype, next_page_select_worktype, select_material

urls = [
    (r'<wc:req>/start', welcome),
    (r'<wc:req>/главное меню', welcome),

    (r'/выбрать объект', select_object),
    (r'/выбрать объект/<int:object_page_number>/следующая страница', next_page_select_object),
    (r'/выбрать объект/<int:object_page_number>/предыдущая страница', previos_page_select_object),

    (r'/выбрать объект/<int:object_page_number>/<int:object_id>', select_worktype),
    (r'/выбрать объект/<int:object_page_number>/<int:object_id>/<int:worktype_page_number>/следующая страница', next_page_select_worktype),
    (r'/выбрать объект/<int:object_page_number>/<int:object_id>/<int:worktype_page_number>/предыдущая страница', previos_page_select_worktype),

    (r'/выбрать объект/<int:object_page_number>/<int:object_id>/<int:worktype_page_number>/<int:worktype_id>', select_material),
    ]