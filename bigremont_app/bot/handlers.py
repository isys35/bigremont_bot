from abc import ABC, abstractmethod

from bigremont_app.serializers import UpdateTelegramSerializer


class HandlerInterface(ABC):

    @abstractmethod
    def get_user_id(self):
        pass

    @abstractmethod
    def get_first_name(self):
        pass

    @abstractmethod
    def get_last_name(self):
        pass

    @abstractmethod
    def get_username(self):
        pass

    @abstractmethod
    def get_text(self):
        pass

    @abstractmethod
    def get_message_id(self):
        pass

    @abstractmethod
    def get_callback(self):
        pass


class MessageHandler(HandlerInterface):

    def __init__(self, update: UpdateTelegramSerializer):
        self.update = update

    def get_user_id(self):
        return self.update.message.from_user.id

    def get_first_name(self):
        return self.update.message.from_user.first_name

    def get_last_name(self):
        return self.update.message.from_user.last_name

    def get_username(self):
        return self.update.message.from_user.username

    def get_text(self):
        return self.update.message.text

    def get_message_id(self):
        return self.update.message.message_id

    def get_callback(self):
        return None


class UpdateHandler(HandlerInterface):

    def __init__(self, update: UpdateTelegramSerializer):
        self.update = update
        if self.update.message:
            self.type = "message"
            self.handler = MessageHandler(update)