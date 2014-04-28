from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relation
from sqlalchemy.ext.declarative import declarative_base

from NHDH import app

engine = create_engine(app.config['CONFIG']['db']['database_uri'],
                       convert_unicode=True,
                       **app.config['CONFIG']['db']['database_connect_options'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                        bind=engine))
def init_db():
    from NHDH.models.user import User
    Model.metadata.create_all(bind=engine)

Model = declarative_base(name='Model')
Model.query = db_session.query_property()