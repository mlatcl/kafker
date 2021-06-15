from kafker.app import app
from kafker.users.models import followers, followings


@app.page("/followers/{author}/")
@app.table_route(table=followers, match_info="author")
async def view_followers(web, request, author):
    return web.json(
        {
            author: list(followers[author]),
        }
    )


@app.page("/followings/{author}/")
@app.table_route(table=followings, match_info="author")
async def view_followings(web, request, author):
    return web.json(
        {
            author: list(followings[author]),
        }
    )
