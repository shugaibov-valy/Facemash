from db import Base, session
import sqlalchemy as sq
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__: str = 'users'

    id = sq.Column(sq.Integer(), primary_key=True)
    vk_id = sq.Column(sq.Integer())
    photo = sq.Column(sq.String(1024))
    rating = sq.Column(sq.Float(), default=0)
    times = sq.Column(sq.Integer(), default=0)


    def __repr__(self):
        return str(self.vk_id)


    @classmethod
    def get_top_users(cls):
        users = reversed(session.query(cls).order_by(cls.rating).all()[-10:])
        return users

    @classmethod
    def update_rating(cls, vk_id, points):
        user = session.query(cls).filter(cls.vk_id == vk_id).first()
        user.rating += points
        session.commit()


    def update_times(self, vk_id, point):
        pass

    @classmethod
    def create_new_user(cls, vk_id, photo):
        new_user = User()
        new_user.vk_id = vk_id
        new_user.photo = photo
        session.add(new_user)
        session.commit()

    @classmethod
    def get_user_by_vkid(cls, vk_id):
        user = session.query(cls).filter(cls.vk_id == vk_id).first()
        return user

    def get_times_by_id(self, vk_id):
        user = session.query(cls).filter(cls.vk_id == vk_id).first()
        return user.times

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

