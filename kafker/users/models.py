from typing import Set

import faust

from kafker.app import app
from kafker.models import UID


class Author(faust.Record):
    uid: UID
    name: str


class Follow(faust.Record):
    active_author: str
    passive_author: str
    follow: bool


registers = app.topic("registers", internal=True, value_type=Author)
follows = app.topic("follows", internal=True, value_type=Follow)

authors = app.Table("authors", key_type=UID, value_type=Author)
authors_by_name = app.Table("authors_by_name", key_type=str, value_type=UID)

followings = app.SetTable("followings", key_type=UID, value_type=Set[UID], default=set)
followers = app.SetTable("followers", key_type=UID, value_type=Set[UID], default=set)
