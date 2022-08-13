from db import Base, session
import sqlalchemy as sq
from sqlalchemy.orm import relationship
from datetime import datetime

class Vote(Base):
    __tablename__: str = 'votes'

    id = sq.Column(sq.Integer(), primary_key=True)
    uuid = sq.Column(sq.String(64), unique=True)
    win_id = sq.Column(sq.Integer, sq.ForeignKey('users.id'))
    lose_id = sq.Column(sq.Integer, sq.ForeignKey('users.id'))
    timestamp = sq.Column(sq.DateTime(), default=datetime.utcnow)
    
    def __init__(self, uuid, win_id, lose_id):
        self.uuid = uuid
        self.win_id = win_id
        self.lose_id = lose_id
        
    def __repr__(self):
        return f"{self.id} : {self.uuid} : [{self.win_id, self.lose_id}]"
        
    def save(self):
        try:
            sq.session.add(self)
            sq.session.flush()
        except Exception as ex:
            self.save()

