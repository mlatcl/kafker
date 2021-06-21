from kafker.app import app
from kafker.markov.models import (
    bigram_weights,
    bigrams,
    new_bigrams,
    new_texts,
    personal_dictionary,
    personal_dictionary_rebuilds,
)
from kafker.posts.models import Post, new_posts, posts, posts_by_author


@app.agent(new_posts, sink=[new_texts])
async def submit_text(new_posts):
    async for post in new_posts.group_by(Post.author):
        await personal_dictionary_rebuilds.send(value=post.author)
        yield post.text


@app.agent(new_texts, sink=[new_bigrams])
async def build_ngrams(new_texts):
    async for text in new_texts:
        words = text.split(" ")
        words = [word for word in words if word]
        for bigram in zip(["^", *words], words):
            yield bigram


@app.agent(new_bigrams)
async def persist_bigrams(new_bigrams):
    async for lhs, rhs in new_bigrams:
        bigrams[lhs].add(rhs)
        bigram_weights[lhs, rhs] += 1


@app.agent(personal_dictionary_rebuilds)
async def rebuild_personal_weights(personal_dictionary_rebuilds):
    async for author in personal_dictionary_rebuilds.group_by(
        lambda x: x, name="by-author"
    ):
        print(f"Rebuilding {author}")
        for post_id in posts_by_author[author]:
            post = posts.get(post_id.uid, None)
            print(f"{post_id=} with {post=}")
            if post is not None:
                text = post.text
                words = text.split(" ")
                for word in words:
                    personal_dictionary[author].add(word)
