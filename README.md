# Capstone Project for Full Stack Developer Nanodegree
## Casting Agency
The Casting Agency models a company that is responsible for creating movies and managing and actors to those movies.
There are three roles:
- Casting Assistant: Can view actors and movies
- Casting Director: All permissions a Casting Assistant has, Add or delete an actor from the database and Modify actors or movies
- Executive Producer: All permissions a Casting Director has and add or delete a movie from the database.

## Getting Started

The app is hosted on: https://yfalharbi.herokuapp.com/

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

### Run Test

```bash
python test_app.py
```

## API Reference

### Error Handling

The error codes:

* 401 - Authorization Error
* 404 – resource not found
* 405 - No permissions
* 500 – not getting data
* 502 - not enough data
* 503 - error while updating
* 504 - error while deleteing


Errors are in this format:

```json
      {
        "success": "False",
        "error": 404,
        "message": "resource not found",
      }
```

### Endpoints

#### GET /movies
- General:
  - return a list of Movies

- Sample: `curl --location --request GET "127.0.0.1:5000/movies" \ --header "Content-Type: application/json" \ --header "Authorization: Bearer <Auth_Token>"`

- Response:
```json
{
    "movies": [
        {
            "id": 1,
            "release_date": "1/1/2020",
            "title": "ِmovie 1"
        },
        {
            "id": 2,
            "release_date": "2/2/2022",
            "title": "movie2"
        }
    ],
    "success": true
}
```

#### GET /actors
- General:
  - return a list of Actors

- Sample: `curl --location --request GET "127.0.0.1:5000/actors" \ --header "Content-Type: application/json" \ --header "Authorization: Bearer <Auth_Token>"`

- Response:
```json
{
    "actors": [
        {
            "age": 26,
            "gender": "Male",
            "id": 1,
            "name": "Yasser"
        }
    ],
    "success": true
}
```

#### POST /movies
- General:
  - add Movies to the database

- Sample: `curl --location --request POST "127.0.0.1:5000/movies" \ --header "Content-Type: application/json" \ --header "Authorization: Bearer <Auth_Token>" \ --data-raw "{ "title":<title>, "release_date": <release_date> }"`

- Response:
```json
{
    "movie": {
        "id": 3,
        "release_date": "1/1/2020",
        "title": "movie3"
    },
    "success": true
}
```

#### POST /actors
- General:
  - add Actors to the database

- Sample: `curl --location --request POST "127.0.0.1:5000/actors" \ --header "Content-Type: application/json" \ --header "Authorization: Bearer <Auth_Token>" \ --data-raw "{ "name":<name>, "age": <age>, "gender": <gender> }"`

- Response:
```json
{
    "actor": {
        "age": 26,
        "gender": "Male",
        "id": 1,
        "name": "Yasser"
    },
    "success": true
}
```

#### DELETE /movies
- General:
  - DELETE Movies from the database

- Sample: `curl --location --request DELETE "127.0.0.1:5000/movies/<movie_id>" \ --header "Content-Type: application/json" \ --header "Authorization: Bearer <Auth_token>"`

- Response:
```json
{
    "delete": "3",
    "success": true
}
```

#### DELETE /actors
- General:
  - DELETE Actors from the database

- Sample: `curl --location --request DELETE "127.0.0.1:5000/actors/<actor_id>" \ --header "Content-Type: application/json" \ --header "Authorization: Bearer <Auth_token>"`

- Response:
```json
{
    "delete": "3",
    "success": true
}
```

#### PATCH /movies
- General:
  - Edit Movies data

- Sample: `curl --location --request PATCH "127.0.0.1:5000/movies/<movie_id>" \ --header "Content-Type: application/json" \ --header "Authorization: Bearer <Auth_Token>" \ --data-raw "{ "title":<title>, "release_date": <release_date> }"`

- Response:
```json
{
    "movie": {
        "id": 2,
        "release_date": "1/1/2020",
        "title": "SSS"
    },
    "success": true
}
```

#### PATCH /actors
- General:
  - Edit Actors data

- Sample: `curl --location --request PATCH "127.0.0.1:5000/actors/<actor_id>" \ --header "Content-Type: application/json" \ --header "Authorization: Bearer <Auth_Token>" \ --data-raw "{ "name":<name>, "age": <age>, "gender": <gender> }"`

- Response:
```json
{
    "actor": {
        "age": 26,
        "gender": "Male",
        "id": 1,
        "name": "yfa"
    },
    "success": true
}
```

