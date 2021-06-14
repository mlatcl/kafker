from datetime import datetime
from typing import List

import faust

from kafker.app import app
from kafker.models import UID


class IncomingPost(faust.Record, coerce=True):
    uid: UID
    author: str
    text: str


class Post(faust.Record, coerce=True):
    uid: UID
    author: str
    text: str
    timestamp: datetime


class Timeline(faust.Record, coerce=True):
    posts: List[UID] = []


incoming_posts = app.topic("incoming_posts", internal=True, value_type=IncomingPost)
new_posts = app.topic("new_posts", internal=True, value_type=Post)
posts = app.Table("posts", value_type=Post)
posts_by_author = app.SetTable("posts_by_author", value_type=UID, default=set)

timeline_rebuilds = app.topic("timeline_rebuilds", internal=True, value_type=str)
timelines = app.Table("timelines", value_type=Timeline, default=Timeline)
