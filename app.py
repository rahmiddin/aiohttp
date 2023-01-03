from aiohttp import web
from views import AdsView, UserView
from models import Base, AdsModel, engine, Session
from middlewares import session_middleware

app = web.Application(middlewares=[session_middleware])


async def orm_context(app: web.Application):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()




app.cleanup_ctx.append(orm_context)


app.add_routes([
    web.get('/ads/{ads_id:\d+}', AdsView),
    web.patch('/ads/{ads_id:\d+}', AdsView),
    web.delete('/ads/{ads_id:\d+}', AdsView),
    web.post('/ads/', AdsView),
])

app.add_routes([
    web.post('/user/create/', UserView)
])


if __name__ == '__main__':
    web.run_app(app)

