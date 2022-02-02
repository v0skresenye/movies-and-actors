from flask import jsonify, make_response

from models.actor import Actor
from models.movie import Movie
from settings.constants import MOVIE_FIELDS, ACTOR_FIELDS
from .parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        act = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(act)
    return make_response(jsonify(movies), 200)


def get_movie_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except ValueError:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        try:
            obj = Movie.query.filter_by(id=row_id).first()
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)
        return make_response(jsonify(movie), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


# name, year, genre
def add_movie():
    """
    Add movie
    """
    data = get_request_data()

    for k in data.keys():
        if k not in MOVIE_FIELDS:
            print(k)
            err = 'Not all inputted fields exist'
            return make_response(jsonify(error=err), 400)
    if 'name' not in data.keys():
        err = 'No name specified'
        return make_response(jsonify(error=err), 400)
    if 'year' in data.keys():
        try:
            year = int(data['year'])
        except ValueError:
            err = 'Year must be integer'
            return make_response(jsonify(error=err), 400)
    new_movie = {k: v for k, v in data.items() if k in MOVIE_FIELDS}
    if 'year' in data.keys():
        new_movie["year"] = year
    new_record = Movie.create(**new_movie)
    new_record = new_record.as_dict()
    obj = Movie.query.filter_by(id=new_record['id']).first()
    return make_response(jsonify(obj.as_dict()), 200)


# id, name, year, genre
def update_movie():
    """
    Update movie record by id
    """
    data = get_request_data()

    if 'id' not in data.keys():
        err = 'Id not specified'
        return make_response(jsonify(error=err), 400)

    try:
        row_id = int(data['id'])
    except:
        err = 'Id must be integer'
        return make_response(jsonify(error=err), 400)

    for k in data.keys():
            if k not in MOVIE_FIELDS:
                err = 'Not all inputted fields exist'
                return make_response(jsonify(error=err), 400)
    if 'year' in data.keys():
        try:
            year = int(data['year'])
        except ValueError:
            err = 'Year must be integer'
            return make_response(jsonify(error=err), 400)
    try:
        obj = Movie.query.filter_by(id=row_id).first()
        movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        movie = {k: v for k, v in data.items() if k in MOVIE_FIELDS}
    except:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)
    del(movie['id'])
    Movie.update(row_id, **movie)
    obj = Movie.query.filter_by(id=row_id).first()
    return make_response(jsonify(obj.as_dict()), 200)


def delete_movie():
    """
    Delete movie by id
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
        obj = Movie.query.filter_by(id=row_id).first()
        movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
    except:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)
    Movie.delete(row_id)
    msg = 'Record successfully deleted'
    return make_response(jsonify(message=msg), 200)


def movie_add_relation():
    """
    Add actor to movie's cast
    """
    data = get_request_data()

    if 'id' not in data.keys() or 'relation_id' not in data.keys():
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    try:
        relation_id = int(data["relation_id"])
    except ValueError:
        err = 'Id must be integer'
        return make_response(jsonify(error=err), 400)
    try:
        row_id = int(data["id"])
    except ValueError:
        err = 'Id must be integer'
        return make_response(jsonify(error=err), 400)

    try:
        obj = Actor.query.filter_by(id=relation_id).first()
        actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
    except:
        err = 'Actor record with such id does not exist'
        return make_response(jsonify(error=err), 400)
    try:
        obj = Movie.query.filter_by(id=row_id).first()
        movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
    except:
        err = 'Movie record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    movie = Movie.query.filter_by(id=row_id).first()
    actor = Actor.query.filter_by(id=relation_id).first()
    relation = Movie.add_relation(row_id, actor)
    rel_movie = {k: v for k, v in relation.as_dict().items()}
    rel_movie['cast'] = str(movie.cast)
    return make_response(jsonify(rel_movie), 200)


def movie_clear_relations():
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
        obj = Movie.query.filter_by(id=row_id).first()
        movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
    except:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    movie = Movie.clear_relations(row_id)  # clear relations here
    rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
    rel_movie['cast'] = str(movie.cast)
    return make_response(jsonify(rel_movie), 200)