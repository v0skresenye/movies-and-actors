from core import db
from sqlalchemy import Table, Column, Integer, ForeignKey

actor_id = Column(db.Integer, ForeignKey('actors.id'), primary_key=True)
movie_id = Column(db.Integer, ForeignKey('movies.id'), primary_key=True)
association = Table('association',
                    db.metadata,
                    Column('actor_id', db.Integer, ForeignKey('actors.id'), primary_key=True),
                    Column('movie_id', db.Integer, ForeignKey('movies.id'), primary_key=True))