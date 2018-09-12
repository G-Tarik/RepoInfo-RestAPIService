import requests
import pytest
from . import expected_responses as expected

API_TOKEN_FILE = 'github_token.key'


class Client:
    """Class for sending HTTP request to API endpoints.

    Attributes:
        BASE_URL (str): address where application is running without trailing slash.

    """

    #BASE_URL = 'http://localhost:7000'
    BASE_URL = 'http://172.31.1.10:7000'

    def get(self, url):
        """Send http request to github.

        Returns:
            dict: response body.

        """
        response = requests.get(self.BASE_URL + url, headers={'Authorization': api_token()})

        return response.json()


def api_token():
    """Read API token from file.

    Returns:
        str: token if present in file, empty string otherwise.

    """
    token = ''
    try:
        with open(API_TOKEN_FILE, 'r') as f:
            for line in f:
                token = line.rstrip() if line.startswith('token') else token
    except FileNotFoundError:
        return ''
    else:
        return token


@pytest.fixture
def client():
    yield Client()
    if api_token() == '':
        print('Tested without api token.')


def test_root(client):
    response = client.get('/')
    assert response.keys() == expected.root.keys()


def test_github_repo(client):
    response = client.get('/github/repositories/octocat/Hello-World')
    assert response['fullName'] == expected.github_repo['fullName']
    assert response['createdAt'] == expected.github_repo['createdAt']
    assert response['cloneUrl'] == expected.github_repo['cloneUrl']
    assert 'message' not in response, response['message']


def test_github_rate_limit(client):
    response = client.get('/github/rate_limit')
    assert response.keys() == expected.github_rate_limit.keys()
    assert 'message' not in response, response['message']
