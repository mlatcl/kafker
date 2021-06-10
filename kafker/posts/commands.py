import faust.cli

from kafker.app import app
from kafker.models import UID
from kafker.posts.models import IncomingPost, incoming_posts


@app.command(
    faust.cli.option("-a", "--author", type=str, required=True),
    faust.cli.option("-t", "--text", type=str, required=True),
)
async def post(self, author, text):
    """Post a new keet."""

    await incoming_posts.send(
        value=IncomingPost(
            uid=UID.new(),
            author=author,
            text=text,
        ),
    )
