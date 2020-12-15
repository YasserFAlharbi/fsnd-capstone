import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movies, Actors
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # # create and configure the app
    # app = Flask(__name__)
    # CORS(app)
    # setup_db(app)
    # return app




  app=Flask(__name__)
  setup_db(app)

  CORS(app, resources = {"/": {'origins': '*'}})


  @ app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PATCH,POST,DELETE,OPTIONS')
    return response


  @ app.route('/')
  def working():
      return jsonify({
          'success': True
      }), 200


  @ app.route('/movies', methods = ['GET'])
  @ requires_auth('get:actors_movies')
  def get_movies(token):
      try:
          movies=Movies.query.all()
          details=[movie.details() for movie in movies]
          return jsonify({
              'success': True,
              'movies': details
          }), 200
      except:
          abort(500)


  @ app.route('/actors', methods = ['GET'])
  @ requires_auth('get:actors_movies')
  def get_actors(token):
      try:
          actors=Actors.query.all()
          details=[actor.details() for actor in actors]
          return jsonify({
              'success': True,
              'actors': details
          }), 200
      except:
          abort(500)


  @ app.route('/movies', methods = ['POST'])
  @ requires_auth('post:movies')
  def create_movie(token):
      if request.get_json():
          try:
              data=request.get_json()
              movie=Movies(
                  title = data['title'],
                  release_date = data['release_date']
              )
              movie.insert()
              return jsonify({
                  'success': True,
                  'movie': movie.details()
              }), 200
          except:
              abort(500)
      else:
          abort(502)
  
  
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actor(token):
      if request.get_json():
          try:
              data = request.get_json()
              movie = Actors(
                  name=data['name'],
                  age=data['age'],
                  gender=data['gender']
              )
              movie.insert()
              return jsonify({
                  'success': True,
                  'actor': movie.details()
              }), 200
          except:
              abort(500)
      else:
          abort(502)
  
  
  @app.route('/movies/<id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movies(token, id):
      try:
          movie = Movies.query.filter(Movies.id == id).one_or_none()
          try:
              movie.delete()
              return jsonify({
                  'success': True,
                  'delete': id
              }), 200
          except:
              abort(504)
      except:
          abort(404)
  
  
  @app.route('/actors/<id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actors(token, id):
      try:
          actor = Actors.query.filter(Actors.id == id).one_or_none()
          try:
              actor.delete()
              return jsonify({
                  'success': True,
                  'delete': id
              }), 200
          except:
              abort(503)
      except:
          abort(404)
  
  
  @app.route('/movies/<id>', methods=['PATCH'])
  @requires_auth('patch:actors_movies')
  def edit_movies(token, id):
      try:
          movie = Movies.query.filter(Movies.id == id).one_or_none()
          try:
              data = request.get_json()
              if 'title' in data:
                  movie.title = data['title']
              if 'release_date' in data:
                  movie.release_date = data['release_date']
              movie.update()
              return jsonify({
                  'success': True,
                  'movie': movie.details()
              }), 200
          except:
              abort(503)
      except:
          abort(404)
  
  
  @app.route('/actors/<id>', methods=['PATCH'])
  @requires_auth('patch:actors_movies')
  def edit_actors(token, id):
      try:
          actor = Actors.query.filter(Actors.id == id).one_or_none()
          try:
              data = request.get_json()
              if 'name' in data:
                  actor.name = data['name']
              if 'age' in data:
                  actor.age = data['age']
              if 'gender' in data:
                  actor.gender = data['gender']
              actor.update()
              return jsonify({
                  'success': True,
                  'actor': actor.details()
              }), 200
          except:
              abort(503)
      except:
          abort(404)
  
  
  @app.errorhandler(404)
  def bad_id(error):
      return jsonify({
          'success': False,
          'error': 404,
          'message': 'resource not found'
      }), 404
  
  
  @app.errorhandler(500)
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 500,
          'message': 'not getting data'
      }), 500
  
  
  @app.errorhandler(502)
  def miss_data(error):
      return jsonify({
          'success': False,
          'error': 502,
          'message': 'not enough data'
      }), 502
  
  
  @app.errorhandler(503)
  def update_error(error):
      return jsonify({
          'success': False,
          'error': 503,
          'message': 'error while updating'
      }), 503
  
  
  @app.errorhandler(504)
  def delete_error(error):
      return jsonify({
          'success': False,
          'error': 504,
          'message': 'error while deleteing'
      }), 504
  
  
  @app.errorhandler(AuthError)
  def auth_error(error):
      return jsonify(error.error), error.status_code
  
  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
