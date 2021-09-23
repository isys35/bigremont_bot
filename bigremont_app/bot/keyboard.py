from django.core.paginator import Page
from django.db.models import QuerySet
from telebot.types import ReplyKeyboardRemove


class State:
    __state = None

    @property
    def state(self):
        return self.__state

    def __init__(self, state):
        self.__state = state
        self.__state.context = self

    def transition_to(self, state):
        self.__state = state
        self.__state.context = self


def keyboard(method):
    def decorator(self, *args):
        self.kb_data = []
        method(self, *args)
        return self.get_keyboard(self.kb_data)

    return decorator


class BotKeyboard(State):
    kb_data = None

    def __init__(self, context):
        State.__init__(self, context)

    def row(self, *args):
        button_row = [*args]
        self.kb_data.append(button_row)

    def get_keyboard(self, buttons):
        """
        Вызывает одноименную функцию из созданного state
        :param buttons:
        :return:
        """
        return self.state.get_keyboard(buttons)

    @keyboard
    def main(self) -> None:
        """
        Функция генерации клавиатуры главного меню.
        :return: None
        """
        self.row('🏠 Выбрать объект')

    @keyboard
    def objects(self, objects: QuerySet):
        for object in objects:
            self.row(object.name)
        self.row('🏠 Главное меню')

    @keyboard
    def date_keyboard(self):
        self.row('Сегодня')
        self.row('Завтра')
        self.row('Послезавтра')

    @keyboard
    def materials(self, material_page: Page, added_materials):
        materials_keys = [str(material_object.id) for material_object in material_page.object_list]
        self.row(*materials_keys)
        if material_page.has_next() and material_page.has_previous():
            self.row('⬅️Предыдущая страница', 'Следующая страница ▶️')
        elif material_page.has_next():
            self.row('Следующая страница ▶️')
        elif material_page.has_previous():
            self.row('⬅️ Предыдущая страница')
        if added_materials:
            self.row('✔️ Завершить выбор материалов')
        self.row('🏠 Главное меню')

    def clear_keyboard(self):
        return ReplyKeyboardRemove()