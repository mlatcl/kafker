from kafker.app import app
from kafker.posts.models import posts, timelines
from kafker.users.models import authors_by_name


@app.page("/timeline/{author}/")
@app.table_route(table=timelines, match_info="author")
async def timeline(web, request, author):
    return web.json(
        {
            author: [posts[post_id] for post_id in timelines[authors_by_name[author]]],
        }
    )
