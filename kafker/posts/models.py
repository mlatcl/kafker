from datetime import datetime
from typing import List, Set

import faust

from kafker.app import app
from kafker.models import UID


class IncomingPost(faust.Record, coerce=True):
    uid: UID
    author: str
    text: str


class Post(faust.Record, coerce=True):
    uid: UID
    author: UID
    text: str
    timestamp: datetime


incoming_posts = app.topic("incoming_posts", internal=True, value_type=IncomingPost)
new_posts = app.topic("new_posts", internal=True, key_type=UID, value_type=Post)
posts = app.Table("posts", key_type=UID, value_type=Post)
posts_by_author = app.SetTable(
    "posts_by_author", key_type=UID, value_type=Set[UID], default=set
)

timeline_rebuilds = app.topic("timeline_rebuilds", internal=True, value_type=UID)
timelines = app.Table("timelines", key_type=UID, value_type=List[UID], default=list)
