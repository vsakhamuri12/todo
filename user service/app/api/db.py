from enum import Enum
from mongoengine import (
    Document,
    StringField,
    ListField,
    BooleanField,
    DateTimeField,
    EnumField,
    EmailField,
)


class StatusEnum(Enum):
    DONE = "done"
    NDONE = "ndone"
    ARCHIVED = "ARCHIVED"


# class Todos(Document):
#     title = StringField(required=True)
#     desc = StringField()
#     tags = ListField(StringField(max_length=20))
#     flag = BooleanField()
#     date = DateTimeField()
#     time = DateTimeField()
#     status = EnumField(StatusEnum, default=StatusEnum.NDONE)
#     meta = {"db_alias": "todo", "collection": "Todos"}


class User(Document):
    first_name = StringField(required=True)
    last_name = StringField()
    email = EmailField(required=True)
    password = StringField(required=True)
    disabled = BooleanField()
    meta = {"db_alias": "todo", "collection": "Users"}
