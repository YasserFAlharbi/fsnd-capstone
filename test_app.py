import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import *
from app import *


headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ3UjNVOFZ3OWwwaE96RFJKV2dlRyJ9.eyJpc3MiOiJodHRwczovL3lmYWxoYXJiaS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZkN2FmN2Q5YWJkNzAwMDZlNDQxNzM2IiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNjA3OTcwOTQwLCJleHAiOjE2MDgwNTczNDAsImF6cCI6InJqNUZRY0FUODUwZ1VkOUVQZVQ3RkNuVWo4WXJPR3g3Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnNfbW92aWVzIiwicGF0Y2g6YWN0b3JzX21vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.BJHQyaUhxuyjrAese2cZvYKRsN-YXz1HMqOUohKvX-_30qIzBIZSHi0zCrTKnJvLMVevvufnxcaXpE4u90w0rQCrJZ0JkIUVDQ0Wub1xisxv-3W4qxqYYxVrw_S3Vdd6u4ykoUgolNK4_3eqq05VmFUIJiBNex6UWS9f1zzoACmOhHREL_tKv3ndUjPIrBYfIRhhbD6iqp43ZYyXvzH6vlLnENPTcd0PXF1hXxC8nT4nnOSvhzvgo8drpbBzTYF-T7c0CL4rECilyvvdmE7UPKyW2GWj1CZP1Et6EDEskq7_6KgQ8PZjf3YBoaY6yjfpLrJEGR6LiiTVJPGVujs2QQ'
}
bad_headers = {
    'Content-Type': 'application/json',
    'Authorization': 'meow'
}
unauth_headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ3UjNVOFZ3OWwwaE96RFJKV2dlRyJ9.eyJpc3MiOiJodHRwczovL3lmYWxoYXJiaS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZkNzYxYzRjNTEwNjAwMDcyYTgwYTk2IiwiYXVkIjoiYWdlbmN5IiwiaWF0IjoxNjA4MDMwMzQ0LCJleHAiOjE2MDgxMTY3NDQsImF6cCI6InJqNUZRY0FUODUwZ1VkOUVQZVQ3RkNuVWo4WXJPR3g3Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzX21vdmllcyJdfQ.dxH6l3fb11m5jRj0O0h_hX7pAkdww1BTUr9minmJjgLOQvlfB02TFYbJapfSmxEr44RBOcMc7DOg5xFFl_kPvItNuu92Waxr73sOJfx8tsQ3JmzhU74KCZZ2nbtzsrv08gSfQuSoEWLOxKXrWZSPTe6yEGPh7VudR-KXuDt9Yxp83VKaAtXDLD-P76R6uLLShYSCW5_7I3RRE4gSfZSccqprm14qh9hlYjguzs0pQ6FJaNIeBpkCvO3PEU0hAQVy7ytI0rs5zSHhH5kl8RjvuB4ZjHlgBSA2AcKdZPqdAgmDPRWfNM40Ia2WlR7YiFgyeqxBpOytI3CXnjbJr2zw0Q'
}

# class Test(unittest.TestCase):
#     def retrive_movies(self):
#         res = self.client().get('/movies')
#         self.assertEqual(res.status_code, 200)


class Test(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def test1_App_working(self):
        response = self.client().get('/')
        self.assertEqual(response.status_code, 200)

    def test2_retrive_movies(self):
        response = self.client().get('/movies', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test2_retrive_actors(self):
        response = self.client().get('/actors', headers=headers)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test3_create_movies(self):
        response = self.client().post('/movies',
                                      json={
                                          "title": "Fox",
                                          "release_date": "1/1/2021"
                                      },
                                      headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test3_create_actors(self):
        response = self.client().post('/actors',
                                      json={
                                          "name": "meow",
                                          "age": "22",
                                          "gender": "Male"
                                      },
                                      headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test4_patch_movies(self):
        movie = Movies.query.order_by(Movies.id.desc()).first()
        response = self.client().patch('/movies/{}'.format(movie.id), json={
            "title": "meow1212",
            "release_date": "2/2/2022"
        }, headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test4_patch_actors(self):
        actor = Actors.query.order_by(Actors.id.desc()).first()
        response = self.client().patch('/actors/{}'.format(actor.id), json={
            "name": "meow111",
            "age": "222",
            "gender": "feMale"
        }, headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test5_delete_movies(self):
        movie = Movies.query.order_by(Movies.id.desc()).first()
        response = self.client().delete('/movies/{}'.format(movie.id), headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])

    def test5_delete_actors(self):
        actor = Actors.query.order_by(Actors.id.desc()).first()
        response = self.client().delete('/actors/{}'.format(actor.id), headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['delete'])

    def test6_bad_delete_movies(self):
        response = self.client().delete('/movies/9999', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test6_bad_delete_actors(self):
        response = self.client().delete('/actors/9999', headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test7_bad_patch_movies(self):
        response = self.client().patch('/movies/9999', json={
            "title": "meow1212",
            "release_date": "2/2/2022"
        }, headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test7_bad_patch_actors(self):
        response = self.client().patch('/actors/9999', json={
            "name": "meow111",
            "age": "222",
            "gender": "feMale"
        }, headers=headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test8_JWT_notFormat_create_movies(self):
        response = self.client().post('/movies',
                                      json={
                                          "title": "Fox",
                                          "release_date": "1/1/2021"
                                      },
                                      headers=bad_headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'Header not in format')
        self.assertTrue(data['description'])

    def test8_JWT_notFormat_create_actors(self):
        response = self.client().post('/actors',
                                      json={
                                          "name": "meow",
                                          "age": "22",
                                          "gender": "Male"
                                      },
                                      headers=bad_headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'Header not in format')
        self.assertTrue(data['description'])

    def test9_noAuth_create_movies(self):
        response = self.client().post('/movies',
                                      json={
                                          "title": "Fox",
                                          "release_date": "1/1/2021"
                                      },
                                      headers=unauth_headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertTrue(data['description'])

    def test9_noAuth_create_actors(self):
        response = self.client().post('/actors',
                                      json={
                                          "name": "meow",
                                          "age": "22",
                                          "gender": "Male"
                                      },
                                      headers=unauth_headers)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertTrue(data['description'])


if __name__ == "__main__":
    unittest.main()
