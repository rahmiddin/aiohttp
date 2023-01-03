import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import AdsModel, Base, UserModel
import time

engine = create_engine('postgresql://app:1234@127.0.0.1:5431/app')
Session = sessionmaker(bind=engine)


@pytest.fixture(scope='session', autouse=True)
def init_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@pytest.fixture()
def create_ads():
    with Session() as session:
        new_ads = AdsModel(heading=f'des__{int(time.time())}', description='example', user_id=1)
        session.add(new_ads)
        session.commit()
        return {
            'id': new_ads.id,
            'heading': new_ads.heading,
            'creation_time': new_ads.creation_date,
        }


@pytest.fixture()
def create_user():
    with Session() as session:
        new_user = UserModel(name=f'name__{int(time.time())}', password='1234')
        session.add(new_user)
        session.commit()
        return {
            'id': new_user.id,
            'name': new_user.heading,
        }