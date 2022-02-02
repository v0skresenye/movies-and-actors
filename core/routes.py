from flask import request
from flask import current_app as app

from controllers.actor import *
from controllers.movie import *


@app.route('/api/actors', methods=['GET'])
def actors():
    return get_all_actors()


@app.route('/api/movies', methods=['GET'])
def movies():
    return get_all_movies()


@app.route('/api/actor', methods=['GET', 'POST', 'PUT', 'DELETE'])
def actor():
    return {'GET': get_actor_by_id,
            'POST': add_actor,
            'PUT': update_actor,
            'DELETE': delete_actor
            }[request.method]()


@app.route('/api/movie', methods=['GET', 'POST', 'PUT', 'DELETE'])
def movie():
    return {'GET': get_movie_by_id,
            'POST': add_movie,
            'PUT': update_movie,
            'DELETE': delete_movie
            }[request.method]()


@app.route('/api/actor-relations', methods=['PUT', 'DELETE'])
def actor_relation():
    return {'PUT': actor_add_relation, 'DELETE': actor_clear_relations}[request.method]()


@app.route('/api/movie-relations', methods=['PUT', 'DELETE'])
def movie_relation():
    return {'PUT': movie_add_relation, 'DELETE': movie_clear_relations}[request.method]()
