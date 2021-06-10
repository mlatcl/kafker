import kafker
from kafker.app import app
from kafker.users.models import (
    authors,
    authors_by_name,
    followers,
    followings,
    follows,
    registers,
)
from kafker.posts.models import timeline_rebuilds


@app.agent(registers)
async def create_user(registers):
    async for new_author in registers:
        if new_author.name not in authors_by_name:
            authors[new_author.uid] = new_author
            authors_by_name[new_author.name] = new_author.uid


@app.agent(follows)
async def process_follows(follows):
    async for follow in follows:
        active = authors_by_name[follow.active_author]
        passive = authors_by_name[follow.passive_author]

        if follow.follow:
            followings[active].add(passive)
            followers[passive].add(active)
        else:
            followings[active].discard(passive)
            followers[passive].discard(active)

        await timeline_rebuilds.send(value=active)
