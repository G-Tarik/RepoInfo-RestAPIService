from functools import wraps
import requests
from flask import request, jsonify
from flask_restful import Resource
from .utils import read_github_token_from_file, parse_datetime


GITHUB_URL = 'https://api.github.com/'
GITHUB_CONNECTION_ERROR = ({'error': {'message': 'connection to github is not available'}}, 504)
GITHUB_RESPONSE_ERROR = ({'error': {'message': 'response does not contain valid json'}}, 502)


class GithubRepos(Resource):
    """Class for connecting to https://api.github.com/repos endpoint.

    Attributes:
        url (str): url https://api.github.com/repos

    """

    def __init__(self):
        self.url = GITHUB_URL + 'repos'
        super().__init__()

    def get(self, owner, repo_name):
        """Send http request to github.

        Args:
            owner (str): user name of repository owner.
            repo_name (str): repository name.

        Returns:
            tuple: (json message, status code (default 200)) if connection successful,
                    GITHUB_CONNECTION_ERROR otherwise.

        """
        req_url = '/'.join([self.url, owner, repo_name])
        try:
            response = requests.get(req_url, headers=get_auth_token())
        except (requests.ConnectionError, requests.Timeout):
            return GITHUB_CONNECTION_ERROR
        else:
            resp = response_repository(response)

        return resp


class GithubRateLimit(Resource):
    """Class for connecting to https://api.github.com/rate_limit endpoint.

    Attributes:
        url (str): url https://api.github.com/rate_limit

    """

    def __init__(self):
        self.url = GITHUB_URL + 'rate_limit'
        super().__init__()

    def get(self):
        """Send http request to github.

        Returns:
            tuple: (json message, status code (default 200)) if connection successful,
                    GITHUB_CONNECTION_ERROR otherwise.

        """
        try:
            response = requests.get(self.url, headers=get_auth_token())
        except (requests.ConnectionError, requests.Timeout):
            return GITHUB_CONNECTION_ERROR
        else:
            resp = response_rate_limit(response)

        return resp


def cache_auth_token(func):
    """Decorate function for reading token from file.

    Store token in memory instead of reading from file every time.

    Args:
        func (function): original function

    Returns:
        decorator function

    """
    cache = {}

    @wraps(func)
    def get_cache():
        if 'headers' not in cache:
            cache['headers'] = func()
        return cache['headers']

    return get_cache


@cache_auth_token
def get_auth_token():
    """Get github API token.

    If file does not contain token then read token from client's request Authorization header.

    Returns:
        dict: header with token or empty header if no token found.

    """
    github_token = read_github_token_from_file()
    if github_token:
        headers = {'Authorization': github_token}
    else:
        auth_token = request.headers.get('Authorization', '')
        headers = {'Authorization': auth_token}

    return headers


def response_repository(resp):
    """Parse response from github and format response for the client.

    Args:
        resp (object Response): response from github.

    Returns:
        tuple: (json message, status code (default 200)) if there were no error during parsing.
                If 'resp' does not have Response object return GITHUB_RESPONSE_ERROR.
                If github response does not contain expected fields then forward original response
                as is to the client.

    """
    try:
        _resp = resp.json()
    except ValueError:
        return GITHUB_RESPONSE_ERROR

    try:
        _resp = jsonify({'fullName': _resp['full_name'],
                         'description': _resp['description'],
                         'cloneUrl': _resp['clone_url'],
                         'stars': _resp['stargazers_count'],
                         'createdAt': parse_datetime(_resp['created_at'])})
    except KeyError:
        _resp = (resp.json(), resp.status_code)

    return _resp


def response_rate_limit(resp):
    """Parse response from github and format response for the client.

    Args:
        resp (object Response): response from github.

    Returns:
        tuple: (json message, status code (default 200)) if there were no error during parsing.
                If 'resp' does not have Response object return GITHUB_RESPONSE_ERROR.
                If github response does not contain expected fields then forward original response
                as is to the client.

    """
    try:
        _resp = resp.json()
    except ValueError:
        return GITHUB_RESPONSE_ERROR

    try:
        _resp = jsonify(_resp['rate'])
    except KeyError:
        _resp = (resp.json(), resp.status_code)

    return _resp
