# coding: utf-8

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from rest_method.method_lib import models
from rest_method.method_lib.models import active_models, BaseModel
from rest_method.settings import DB_URI


engine = create_engine(DB_URI, echo=False)
DB = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    login = Column(String(30), nullable=False)
    password = Column(String(30), nullable=False)

    def __repr__(self):
        return "<User('%s')>" % (self.username or self.login)

    @classmethod
    def get_authenticated(cls, login, password):
        try:
            user = DB.query(User).filter_by(login=login).one()
        except NoResultFound:
            user = None
        except MultipleResultsFound:
            user = None

        if user and user.password == password:
            return user

    @classmethod
    def get(cls, user_id):
        try:
            user = DB.query(User).filter_by(id=user_id).one()
        except NoResultFound:
            user = None
        return user


class Roles(Base):
    __tablename__ = 'user_roles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    model_name = Column(String(30), nullable=False)

    def get_model(self):
        for model in active_models:
            if self.model_name == model.name:
                return model
        return BaseModel()


User.roles = relationship("Roles", order_by=Roles.id)

users_table = User.__table__
metadata = Base.metadata


def create_all():
    try:
        Roles.__table__.drop(engine)
        User.__table__.drop(engine)
    except Exception:
        pass
    metadata.create_all(engine)


def init_db():
    create_all()
    users_data_map = (
        (('test1', 'pass1'), (models.BaseModel1(), )),
        (('test2', 'pass2'), (models.BaseModel2(),
                              models.BaseModel3())),
        (('test3', 'pass3'), (models.BaseModel4(),
                              models.BaseModel5(),
                              models.BaseModel6())),
    )
    for user_info, benefit_models in users_data_map:
        login, password = user_info
        user = User(login=login, password=password)
        user_id = user.id
        user.roles = [
            Roles(user_id=user_id, model_name=benefit_model.name)
            for benefit_model in benefit_models
        ]

        DB.add(user)
    DB.commit()
