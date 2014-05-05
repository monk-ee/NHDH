from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from NHDH import app

engine = create_engine(app.config['CONFIG']['db']['database_uri'],
                       convert_unicode=True,
                       **app.config['CONFIG']['db']['database_connect_options'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                        bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from models import User
    Base.metadata.create_all(bind=engine)

