from datetime import datetime as dt
from core import db
from models.base import Model
from models.relations import association


class Actor(Model, db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(11))
    date_of_birth = db.Column(db.DateTime)

    movies = db.relationship('Movie', secondary='association', uselist=False, lazy='subquery',
        backref=db.backref('cast', lazy=False))

    def __repr__(self):
        return '<Actor {}>'.format(self.name)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}