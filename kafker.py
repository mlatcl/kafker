from datetime import datetime
import itertools as it
from typing import List, Set
import faust
import faust.cli


class Keet(faust.Record):
    author: str
    text: str
    timestamp: int = 0


class Follow(faust.Record):
    active_author: str
    passive_author: str
    follow: bool


app = faust.App(
    "kafker",
    broker="kafka://localhost:9092",
)

incoming_keets = app.topic("incoming_keets", value_type=Keet)
new_keets = app.topic("new_keets", value_type=Keet)
follows = app.topic("follows", value_type=Follow)
timeline_rebuilds = app.topic("timeline_rebuild", value_type=str)

keets = app.Table("keets", default=list)
timelines = app.Table("timelines", default=list)
followings = app.SetTable("followings", default=set)
followers = app.SetTable("followers", default=set)


@app.agent(incoming_keets, sink=[new_keets])
async def process_incoming_keets(incoming_keets):
    async for keet in incoming_keets:
        yield Keet(
            author=keet.author,
            text=keet.text,
            timestamp=int(datetime.now().timestamp()),
        )


@app.agent(new_keets)
async def persist_keet(new_keets):
    async for keet in new_keets.group_by(Keet.author):
        author_keets = keets[keet.author]
        author_keets.append(keet)
        keets[keet.author] = author_keets


@app.agent(new_keets)
async def append_timelines_with_new_keets(new_keets):
    async for keet in new_keets.group_by(Keet.author):
        for author in {keet.author, *followers[keet.author]}:
            timeline = timelines[author]
            timeline.append(keet)
            timelines[author] = timeline


@app.agent(follows)
async def process_follows(follows):
    async for follow in follows.group_by(Follow.passive_author):
        if follow.follow:
            followings[follow.active_author].add(follow.passive_author)
            followers[follow.passive_author].add(follow.active_author)
        else:
            followings[follow.active_author].discard(follow.passive_author)
            followers[follow.passive_author].discard(follow.active_author)

        await timeline_rebuilds.send(value=follow.active_author)


@app.agent(timeline_rebuilds)
async def rebuild_timeline(timeline_rebuilds):
    async for author in timeline_rebuilds.group_by(lambda x: x, name="by-author"):
        timelines[author] = sorted(
            it.chain(*(keets[athr] for athr in {author, *followings[author]})),
            key=lambda keet: keet.timestamp,
        )


@app.page("/timeline/{author}/")
@app.table_route(table=timelines, match_info="author")
async def get_count(web, request, author):
    return web.json(
        {
            author: timelines[author],
        }
    )


@app.command(
    faust.cli.option("-a", "--active", type=str, required=True),
    faust.cli.option("-p", "--passive", type=str, required=True),
    faust.cli.option("--follow/--unfollow", default=True),
)
async def follow(self, active, passive, follow):
    """Follow or unfollow somebody."""
    await follows.send(
        value=Follow(
            active_author=active,
            passive_author=passive,
            follow=follow,
        )
    )


@app.command(
    faust.cli.option("-a", "--author", type=str, required=True),
    faust.cli.option("-t", "--text", type=str, required=True),
)
async def post(self, author, text):
    """Post a new keet."""
    await incoming_keets.send(
        value=Keet(
            author=author,
            text=text,
        )
    )


if __name__ == "__main__":
    app.main()
