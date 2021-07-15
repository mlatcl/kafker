import itertools as it
from datetime import datetime

from kafker.app import app
from kafker.posts.models import (
    IncomingPost,
    Post,
    Timeline,
    incoming_posts,
    new_posts,
    posts,
    posts_by_author,
    timeline_rebuilds,
    timelines,
)
from kafker.users.models import followers, followings


@app.agent(incoming_posts, sink=[new_posts])
async def validate_incoming_post(incoming_posts):
    async for incoming_post in incoming_posts.group_by(IncomingPost.author):
        yield Post(
            uid=incoming_post.uid,
            author=incoming_post.author,
            text=incoming_post.text,
            timestamp=datetime.now(),
        )


@app.agent(new_posts)
async def persist_post(new_posts):
    async for post in new_posts.group_by(Post.author):
        posts[post.uid.uid] = post
        posts_by_author[post.author].add(post.uid)


@app.agent(new_posts, sink=[timeline_rebuilds])
async def update_timelines_after_new_post(new_posts):
    async for post in new_posts.group_by(Post.author):
        for interested in (post.author, *followers[post.author]):
            yield interested


@app.agent(timeline_rebuilds)
async def rebuild_timeline(timeline_rebuilds):
    async for author in timeline_rebuilds.group_by(lambda x: x, name="by-author"):
        timelines[author] = Timeline(
            posts=list(
                sorted(
                    it.chain(
                        *(
                            posts_by_author[athr]
                            for athr in {author, *followings[author]}
                        )
                    ),
                    key=lambda post_id: posts[post_id.uid].timestamp,
                )
            )
        )
