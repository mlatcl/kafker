import click
import faust.cli

from kafker.app import app
from kafker.learning.models import new_texts


@app.command(
    faust.cli.argument("input-file", type=click.File("r")),
)
async def ingest_text(self, input_file):
    """Ingest text from a file."""

    for line in input_file:
        await new_texts.send(value=line.strip())
