import kafker
from kafker.app import app
from kafker.users.models import (
    Author,
    authors,
    Follow,
    followers,
    followings,
    follows,
    registers,
)
from kafker.posts.models import timeline_rebuilds


@app.agent(registers)
async def create_user(registers):
    async for new_author in registers.group_by(Author.name):
        if new_author.name not in authors:
            authors[new_author.name] = new_author


@app.agent(follows)
async def process_follows(follows):
    async for follow in follows.group_by(Follow.active_author):
        active = follow.active_author
        passive = follow.passive_author

        if follow.follow:
            followings[active].add(passive)
            followers[passive].add(active)
        else:
            followings[active].discard(passive)
            followers[passive].discard(active)

        await timeline_rebuilds.send(value=active)
