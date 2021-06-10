import faust

from kafker.app import app
from kafker.users.models import followers, followings


@app.page("/followers/{author}/")
@app.table_route(table=followers, match_info="author")
async def get_count(web, request, author):
    return web.json(
        {
            author: list(followers[author]),
        }
    )


@app.page("/followings/{author}/")
@app.table_route(table=followings, match_info="author")
async def get_count(web, request, author):
    return web.json(
        {
            author: list(followings[author]),
        }
    )
