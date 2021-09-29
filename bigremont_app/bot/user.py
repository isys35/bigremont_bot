import re

from bigremont_app.bot.handlers import UpdateHandler
from bigremont_app.models import TelegramUser, TelegramGroup
from bigremont_app.serializers import UpdateTelegramSerializer


def initialized(method):
    def decorator(self, *args):
        method(self, *args)
        self.initialized = True

    return decorator


class User:
    id = None
    update = None
    full_request = None
    request = None
    state = '/'
    callback = None

    def __init__(self, update: UpdateTelegramSerializer):
        self.update = update
        self.update_handler = UpdateHandler(update)
        self.initialized = False

    def create_user(self):
        tg_user = TelegramUser(pk=self.id,
                               username=self.update_handler.get_username())
        tg_user.save()

    def _init_request(self):
        if self.update_handler.type == "message":
            reg = re.compile("""[^a-zA-Zа-яА-Я";#().,0-9«»-№]""")
            self.request = reg.sub(' ', self.update_handler.get_text()).strip().lower()
        elif self.update_handler.type == "callback":
            self.request = 'callback'
            self.callback = self.update_handler.get_callback()
        if self.request == '':
            self.full_request = self.state
        elif self.state == '/':
            self.full_request = self.state + self.request
        else:
            self.full_request = f"{self.state}/{self.request}"

    @initialized
    def init_from_update(self):
        self.id = self.update_handler.get_user_id()
        self._init_request()
        self.create_user()

    def init_from_db(self):
        tg_user = TelegramUser.objects.filter(pk=self.update_handler.get_user_id())
        if tg_user:
            tg_user = tg_user.first()
            self.id = tg_user.pk
            self.state = tg_user.state
            self._init_request()
            self.initialized = True

    def save(self):
        tg_user = TelegramUser.objects.get(id=self.id)
        tg_user.state = self.state
        tg_user.save()

    # TODO: нарушает принципп единой ответственности
    def save_group(self):
        TelegramGroup.objects.get_or_create(tg_id=self.update_handler.get_chat_id(),
                                            title=self.update_handler.get_group_title())

    def save_state(self, new_state=None):
        if new_state is None:
            if self.state == '/':
                self.state = self.state + self.request
            else:
                self.state = self.state + '/' + self.request
        else:
            self.state = new_state
        self.save()
