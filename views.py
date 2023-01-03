from aiohttp import web
from models import Session, AdsModel, UserModel, Token
import json


def return_ads_json(ads):
    return web.json_response(
        {'id': ads.id,
         'heading': ads.heading,
         'creation_date': ads.creation_date.isoformat(),
         'owner': ads.user_id
         }
    )


def return_user_json(user):
    return web.json_response(
        {'id': user.id,
         'name': user.name,
         }
    )


def get_ads(ads_id, session: Session):
    ads = session.get(AdsModel, ads_id)
    if ads is None:
        raise web.HTTPNotFound(text=json.dumps({'status': 'error', 'descriptions': 'user not found'}),
                               content_type='application/json')
    return ads


class AdsView(web.View):

    @property
    def session(self):
        return self.request['session']

    async def get(self):
        ads_id = int(self.request.match_info['ads_id'])
        ads = await get_ads(ads_id, self.session)
        if ads is None:
            raise web.HTTPNotFound(text=json.dumps({'status': 'error', 'descriptions': 'user not found'}),
            content_type='application/json')
        return return_ads_json(ads)

    async def post(self):
        ads_data = await self.request.json()
        new_ads = AdsModel(**ads_data)
        self.session.add(new_ads)
        await self.session.commit()
        return return_ads_json(new_ads)

    async def patch(self):
        ads_id = int(self.request.match_info['ads_id'])
        ads_patch = await self.request.json()
        ads = await get_ads(ads_id, self.session)
        for field, value in ads_patch.items():
            setattr(ads, field, value)
        self.session.add(ads)
        await self.session.commit()
        return return_ads_json(ads)

    async def delete(self):
        ads_id = int(self.request.match_info['ads_id'])
        ads = await get_ads(ads_id, self.session)
        await self.session.delete(ads)
        await self.session.commit()
        return web.json_response({
            'status': 'delete'
        })


class UserView(web.View):

    @property
    def session(self):
        return self.request['session']

    async def post(self):
        user_data = await self.request.json()
        new_user = UserModel(**user_data)
        self.session.add(new_user)
        await self.session.commit()
        return return_user_json(new_user)
