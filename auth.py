import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'yfalharbi.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'agency'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    token_auth_header = request.headers.get('Authorization', None)
    if not token_auth_header:
        raise AuthError({'code': 'NO header is Present',
                         'description': 'Could not find Authorization Token'}, 401)
    headerParts = token_auth_header.split()
    if len(headerParts) > 2 or len(headerParts) == 1 or headerParts[0].lower() != 'bearer':
        raise AuthError({'code': 'Header not in format',
                         'description': 'Header must start with bearer and token after that'}, 401)
    return headerParts[1]


def check_permissions(permission, payload):
    #print(permission ,payload)
    if 'permissions' not in payload:
        raise AuthError({'code': 'No permissions',
                         'description': 'permissions are not included in the payload'}, 405)
    if permission not in payload['permissions']:
        raise AuthError(
            {'code': 'unauthorized', 'description': 'permission string is not in the payload permissions'}, 401)
    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    if 'kid' not in unverified_header:
        raise AuthError({'code': 'Header not in format',
                         'description': 'token should be an Auth0 token with key id (kid)'}, 401)
    rsa_key = {}
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if not rsa_key:
        raise AuthError(
            {'code': 'No Key', 'description': 'Could not find the key'}, 401)
    else:
        try:
            # print('hello')
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            # print(payload)
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError(
                {'code': 'expired', 'description': 'token expired'}, 401)
        except jwt.JWTClaimsError:
            raise AuthError(
                {'code': 'claim error', 'description': 'bad audience and issuer'}, 401)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
