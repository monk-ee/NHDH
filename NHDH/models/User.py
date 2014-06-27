from NHDH import db
from datetime import datetime


roles = {1: 'admin', 2:'user'}


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email',db.String(200), unique=True, index=True)
    password = db.Column(db.String(64))
    role = db.Column(db.Integer)
    registered_on = db.Column('registered_on', db.DateTime)

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
