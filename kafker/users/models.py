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

authors = app.GlobalTable("authors", key_type=str, value_type=Author)

followings = app.SetTable("followings", value_type=str, default=set)
followers = app.SetTable("followers", value_type=str, default=set)
