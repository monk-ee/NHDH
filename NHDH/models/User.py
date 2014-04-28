from NHDH.database import Model
from sqlalchemy import Column, Integer, String, DateTime, event
from datetime import datetime

roles = {1: 'admin', 2:'user'}


class User(Model):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    email = Column('email',String(200), unique=True, index=True)
    password = Column(String(64))
    role = Column(Integer)
    registered_on = Column('registered_on', DateTime)

    def __init__(self, password, email):
        self.email = email
        self.password = password
        self.role_name = None
        self.registered_on = datetime.utcnow()

    def to_json(self):
        return dict(name=self.name, email=self.email, role=roles.get(self.role, None))

    def __eq__(self, other):
        return type(self) is type(other) and self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.email)

def load_monitor(target, context):
    if target.role:
        target.role_name = roles.get(target.role, None)

event.listen(User, 'load', load_monitor)