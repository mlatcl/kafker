import itertools as it
from datetime import datetime

import faust

from kafker.app import app
from kafker.posts.models import (
    Post,
    incoming_posts,
    new_posts,
    posts,
    posts_by_author,
    timeline_rebuilds,
    timelines,
)
from kafker.users.models import followers, followings, authors_by_name


@app.agent(incoming_posts, sink=[new_posts])
async def validate_incoming_post(incoming_posts):
    async for incoming_post in incoming_posts:
        author = authors_by_name[incoming_post.author]
        yield {
            author: Post(
                uid=incoming_post.uid,
                author=author,
                text=incoming_post.text,
                timestamp=datetime.now(),
            )
        }


@app.agent(new_posts)
async def persist_post(new_post):
    async for post in new_posts:
        posts[post.uid] = post
        posts_by_author[post.author].add(post.uid)

        for interested in (post.author, *followers[post.author]):
            timeline_rebuilds.send_soon(key=interested, value=interested)


@app.agent(timeline_rebuilds)
async def rebuild_timeline(timeline_rebuilds):
    async for author in timeline_rebuilds:
        timelines[author] = sorted(
            it.chain(
                *(posts_by_author[athr] for athr in {author, *followings[author]})
            ),
            key=lambda post_id: posts[post_id].timestamp,
        )
