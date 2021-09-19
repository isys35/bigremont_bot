from bigremont_app.bot.views import welcome, select_object, next_page_select_object, previos_page_select_object, \
    select_worktype

urls = [
    (r'<wc:req>/start', welcome),
    (r'<wc:req>/главное меню', welcome),

    (r'/выбрать объект', select_object),
    (r'/выбрать объект/<int:object_page_number>/следующая страница', next_page_select_object),
    (r'/выбрать объект/<int:object_page_number>/предыдущая страница', previos_page_select_object),

    (r'/выбрать объект/<int:object_page_number>/<int:object_id>', select_worktype),
    ]