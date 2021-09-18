from typing import List

from pydantic import BaseModel, Field
from datetime import datetime


class UserTelegramSerializer(BaseModel):
    id: int
    is_bot: bool
    first_name = ""
    last_name = ""
    username: str = None
    language_code: str = None


class ChatTelegramSerializer(BaseModel):
    id: int
    first_name: str = ""
    last_name: str = ""
    username: str = None
    type: str
    title: str = None
    all_members_are_administrators: bool = None


class EntityTelegramSerializer(BaseModel):
    offset: int
    length: int
    type: str


class MessageTelegramSerializer(BaseModel):
    message_id: int
    date: datetime
    text: str = None
    from_user: UserTelegramSerializer = Field(alias="from")
    chat: ChatTelegramSerializer
    entities: List[EntityTelegramSerializer] = None


class ChatMemberSerializer(BaseModel):
    user: UserTelegramSerializer
    status: str


class MyChatMemberSerializer(BaseModel):
    chat: ChatTelegramSerializer
    from_user: UserTelegramSerializer = Field(alias="from")
    date: datetime
    old_chat_member: ChatMemberSerializer
    new_chat_member: ChatMemberSerializer


class UpdateTelegramSerializer(BaseModel):
    update_id: int
    message: MessageTelegramSerializer = None
    my_chat_member: MyChatMemberSerializer = None