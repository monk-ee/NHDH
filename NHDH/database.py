from NHDH import db
from NHDH import User


def init_db():
    db.create_all()
    admin = User.User('admin', 'admin@example.com')
    guest = User.User('guest', 'guest@example.com')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()