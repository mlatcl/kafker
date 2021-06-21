import itertools as it
import random

from kafker.app import app
from kafker.markov.models import bigram_weights, bigrams


@app.page("/generate/")
async def generate_post(web, request, length=50):
    def word_generator():
        current_word = "^"
        while True:
            next_words = list(bigrams[current_word])
            next_weights = [
                bigram_weights[current_word, next_word] for next_word in next_words
            ]
            if not next_words:
                return

            next_word = random.choices(next_words, weights=next_weights)[0]
            current_word = next_word
            yield current_word

    return web.json({"post": " ".join(it.islice(word_generator(), length))})
