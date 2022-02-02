from datetime import datetime as dt

from core import db
from models.base import Model
from models.relations import association

class Movie(Model, db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer)
    genre = db.Column(db.String(20))

    actors = db.relationship('Actor', secondary='association', uselist=False, lazy='subquery',
        backref=db.backref('filmography', lazy=False))

    def __repr__(self):
        return '<Movie {}>'.format(self.name)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}