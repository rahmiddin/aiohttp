import datetime
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

engine = create_async_engine('postgresql+asyncpg://app:1234@127.0.0.1:5431/app')
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)


class AdsModel(Base):
    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    heading = Column(String, nullable=False)
    description = Column(String, nullable=False)
    creation_date = Column(DateTime, default=lambda: datetime.datetime.utcnow())
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship(UserModel, lazy='joined')


class Token(Base):
    __tablename__ = 'user_token'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    creation_date = Column(DateTime, default=lambda: datetime.datetime.utcnow())
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship(UserModel, lazy='joined')
