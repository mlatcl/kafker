import itertools as it
import random

from kafker.app import app
from kafker.markov.models import bigram_weights, bigrams, personal_dictionary

PERSONAL_WORDS_WEIGHT = 10.0


@app.page("/generate/{author}/")
@app.table_route(table=personal_dictionary, match_info="author")
async def generate_post(web, request, author, length=50):
    def word_generator():
        current_word = "^"
        personal_words = personal_dictionary[author]
        while True:
            next_words = list(bigrams[current_word])
            next_weights = [
                (PERSONAL_WORDS_WEIGHT if next_word in personal_words else 1.0)
                * bigram_weights[current_word, next_word]
                for next_word in next_words
            ]
            if not next_words:
                return

            next_word = random.choices(next_words, weights=next_weights)[0]
            current_word = next_word
            yield current_word

    return web.json({"post": " ".join(it.islice(word_generator(), length))})
