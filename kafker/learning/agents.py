from kafker.app import app
from kafker.learning.models import (
    Bigram,
    bigram_weights,
    bigrams,
    new_bigrams,
    new_texts,
)
from kafker.posts.models import Post, new_posts


@app.agent(new_posts, sink=[new_texts])
async def submit_text(new_posts):
    async for post in new_posts.group_by(Post.author):
        yield post.text


@app.agent(new_texts, sink=[new_bigrams])
async def build_ngrams(new_texts):
    async for text in new_texts:
        words = text.split(" ")
        words = [word for word in words if word]
        for bigram in zip(["^", *words], words):
            yield Bigram(*bigram)


@app.agent(new_bigrams)
async def persist_bigrams(new_bigrams):
    async for bigram in new_bigrams:
        bigrams[bigram.lhs].add(bigram.rhs)
        bigram_weights[bigram] += 1
