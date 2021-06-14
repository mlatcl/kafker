from kafker.app import app
from kafker.posts.models import posts, timelines


@app.page("/timeline/{author}/")
@app.table_route(table=timelines, match_info="author")
async def timeline(web, request, author):
    return web.json(
        {
            author: [posts[post_id.uid] for post_id in timelines[author].posts],
        }
    )
