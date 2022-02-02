from flask import jsonify, make_response

from datetime import datetime as dt

from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS, MOVIE_FIELDS, DATE_FORMAT
from .parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200)


def get_actor_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' not in data.keys():
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    try:
        row_id = int(data['id'])
    except ValueError:
        err = 'Id must be integer'
        return make_response(jsonify(error=err), 400)
    try:
        obj = Actor.query.filter_by(id=row_id).first()
        actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
    except:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)
    return make_response(jsonify(actor), 200)


# name, gender, date_of_birth
def add_actor():
    """
    Add actor
    """
    data = get_request_data()

    if 'date_of_birth' not in data.keys():
        err = 'No birth date specified'
        return make_response(jsonify(error=err), 400)
    if 'name' not in data.keys():
        err = 'No name specified'
        return make_response(jsonify(error=err), 400)
    try:
        birth = dt.strptime(data["date_of_birth"], DATE_FORMAT).date()
    except:
        err = 'Incorrect format'
        return make_response(jsonify(error=err), 400)

    for k in data.keys():
        if k not in ACTOR_FIELDS:
            err = 'Not all inputted fields exist'
            return make_response(jsonify(error=err), 400)

    new_actor = {k: v for k, v in data.items()}
    new_actor["date_of_birth"] = birth
    new_record = Actor.create(**new_actor)
    new_record = {k: v for k, v in new_record.as_dict().items() if k in ACTOR_FIELDS}
    return make_response(jsonify(new_record), 200)


# id, name, gender, date_of_birth
def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()

    if 'id' not in data.keys():
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    for k in data.keys():
        if k not in ACTOR_FIELDS:
            err = 'Not all inputted fields exist'
            return make_response(jsonify(error=err), 400)
    try:
        row_id = int(data['id'])
    except ValueError:
        err = 'Id must be integer'
        return make_response(jsonify(error=err), 400)
    if 'date_of_birth' in data.keys():
        try:
            data["date_of_birth"] = dt.strptime(data["date_of_birth"], DATE_FORMAT).date()
        except:
            err = 'Incorrect format'
            return make_response(jsonify(error=err), 400)
    try:
        obj = Actor.query.filter_by(id=row_id).first()
        actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        actor = {k: v for k, v in data.items()}
    except:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)
    del(actor['id'])
    Actor.update(row_id, **actor)
    obj = Actor.query.filter_by(id=row_id).first()
    return make_response(jsonify(obj.as_dict()), 200)


def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()

    if 'id' not in data.keys():
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    try:
        row_id = int(data['id'])
    except:
        err = 'Id must be integer'
        return make_response(jsonify(error=err), 400)
    try:
        obj = Actor.query.filter_by(id=row_id).first()
        actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
    except:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)
    Actor.delete(row_id)
    msg = 'Record successfully deleted'
    return make_response(jsonify(message=msg), 200)


# id, relation_id
def actor_add_relation():
    """
    Add a movie to actor's filmography
    """
    data = get_request_data()

    if 'id' not in data.keys() or 'relation_id' not in data.keys():
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    try:
        relation_id = int(data["relation_id"])
    except:
        err = 'Id must be integer'
        return make_response(jsonify(error=err), 400)
    try:
        row_id = int(data["id"])
    except:
        err = 'Id must be integer'
        return make_response(jsonify(error=err), 400)

    try:
        obj = Actor.query.filter_by(id=row_id).first()
        actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
    except:
        err = 'Actor record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    try:
        obj = Movie.query.filter_by(id=relation_id).first()
        movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
    except:
        err = 'Movie record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    movie = Movie.query.filter_by(id=relation_id).first()
    actor = Actor.query.filter_by(id=row_id).first()
    relation = Actor.add_relation(row_id, movie)
    rel_actor = {k: v for k, v in relation.as_dict().items()}
    rel_actor['filmography'] = str(actor.filmography)
    return make_response(jsonify(rel_actor), 200)


# id
def actor_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()

    if 'id' not in data.keys():
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    try:
        row_id = int(data["id"])
    except:
        err = 'Id must be integer'
        return make_response(jsonify(error=err), 400)
    try:
        obj = Actor.query.filter_by(id=row_id).first()
        actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
    except:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    actor = Actor.clear_relations(row_id)  # clear relations here
    rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
    rel_actor['filmography'] = str(actor.filmography)
    return make_response(jsonify(rel_actor), 200)

