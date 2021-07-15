from kafker.app import app
from kafker.posts.models import timeline_rebuilds
from kafker.users.models import (
    Author,
    Follow,
    authors,
    followers,
    followings,
    follows,
    registers,
)


@app.agent(registers)
async def create_user(registers):
    async for new_author in registers.group_by(Author.name):
        if new_author.name not in authors:
            authors[new_author.name] = new_author


@app.agent(follows)
async def process_active(follows):
    async for follow in follows.group_by(Follow.active_author):
        active = follow.active_author
        passive = follow.passive_author

        if follow.follow:
            followings[active].add(passive)
        else:
            followings[active].discard(passive)


@app.agent(follows, sink=[timeline_rebuilds])
async def update_timelines_after_follow(follows):
    async for follow in follows.group_by(Follow.active_author):
        yield follow.active_author


@app.agent(follows)
async def process_follows_passive(follows):
    async for follow in follows.group_by(Follow.passive_author):
        active = follow.active_author
        passive = follow.passive_author

        if follow.follow:
            followers[passive].add(active)
        else:
            followers[passive].discard(active)
