import faust.cli

from kafker.app import app
from kafker.models import UID
from kafker.users.models import Author, Follow, authors_by_name, follows, registers


@app.command(
    faust.cli.option("-n", "--name", type=str, required=True),
)
async def register(self, name):
    """Register a new user."""

    await registers.send(
        value=Author(
            uid=UID.new(),
            name=name,
        ),
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
        ),
    )
