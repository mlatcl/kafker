import itertools as it
import random

import click
import faust.cli

from kafker.app import app
from kafker.learning.models import bigram_weights, bigrams


@app.page("/generate/")
async def generate_post(web, request, length=50):
    def word_generator():
        current = "^"
        while True:
            next_words = list(bigrams[current])
            next_weights = [
                bigram_weights[current, next_word] for next_word in next_words
            ]
            if not next_words:
                return

            next_word = random.choices(next_words, weights=next_weights)[0]
            current = next_word
            yield current

    return web.json({"post": " ".join(it.islice(word_generator(), length))})
