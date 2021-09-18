import os
from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

from sqlalchemy.dialects import postgresql

db_string = os.getenv('CONNECTIONSTRING')

db = create_engine(db_string)
base = declarative_base()


class User(base):
    __tablename__ = 'users'

    email = Column(String, primary_key=True)
    wallet_address = Column(String)
    subscribed = relationship("Repo")

class LabelVector(base):
    __tablename__ = 'labelvectors'

    label = Column(String, primary_key=True)
    vector = Column(postgresql.ARRAY(postgresql.DOUBLE_PRECISION))

class Repo(base):
    __tablename__ = 'repos'

    fullname = Column(String, primary_key=True)
    labels = relationship("LabelVector")



Session = sessionmaker(db)
base.metadata.create_all(db)

session = Session()


def create(session):
    doctor_strange = User(title="Doctor Strange", director="Scott Derrickson", year="2016")
    session.add(doctor_strange)
    session.commit()


def get(session):
    films = session.query(User)
    for film in films:
        print(film.title)


def update(user, session):
    user.title = "Some2016Film"
    session.commit()


def delete(user, session):
    session.delete(user)
    session.commit()