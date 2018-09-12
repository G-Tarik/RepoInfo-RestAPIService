import json
import requests
import pytest
from app import create_app
from . import expected_app_responses as expected

MOCK_DATA_FILE = 'github_responses.json'


def get_mock_github_data():
    """Get github responses used for mocking.

    To prepare data file use module mock_github_responses.py.

    Returns:
        dict: see module mock_github_responses.py for structure.

    """
    with open(MOCK_DATA_FILE, 'r') as f:
        data = json.load(f)

    return data


MOCK_DATA = get_mock_github_data()


class MockGithubResponse:
    """Used for mocking requests.get method.

    Attributes:
        url (str): used for choosing mocked response from MOCK_DATA dictionary.

    """

    url = None

    def __init__(self, url, **kwargs):
        if not self.url:
            self.url = url
        self.status_code = MOCK_DATA[self.url]['status_code']
        self.body = MOCK_DATA[self.url]['body']

    def json(self):
        """Simulate json method of mocked requests.get.

        Returns:
            dict: mocked response body

        """
        return self.body


class MockConnectionError:
    """Mock requests.get method.

    Raises:
        ConnectionError: simulate network connection error

    """

    def __init__(self, *args, **kwargs):
        raise requests.exceptions.ConnectionError


class MockInvalidJson:
    """Mock response object which does not have proper json content."""

    def __init__(self, *args, **kwargs):
        pass

    def json(self):
        raise ValueError


class Client:
    """Class for interacting with Flask application."""

    def get(self, url):
        """Send request.

        Args:
            url(str): url of endpoint.

        Returns:
            dict: response from application to be compared in tests with expected result.

        """
        app = create_app()
        client = app.test_client()
        response = client.get(url)

        return response.get_json()


@pytest.fixture
def client():
    yield Client()


def get_mock_object(test_name=None):
    """Allow reusing same class with several test functions.

    Only 'url' class attribute need to be changed for reusing class.

    Args:
        test_name (str): optional, used to choose appropriate mocked response
                         from MOCK_DATA in class MockGithubResponse

    Returns:
        class: with dynamically modified class attribute 'url'

    """
    MockGithubResponse.url = test_name

    return MockGithubResponse


def test_github_repo(client, monkeypatch):
    monkeypatch.setattr("requests.get", get_mock_object())
    response = client.get('/github/repositories/octocat/Hello-World')
    assert response == expected.github_repo


def test_github_rate_limit(client, monkeypatch):
    monkeypatch.setattr("requests.get", get_mock_object())
    response = client.get('/github/rate_limit')
    assert response == expected.github_rate_limit


def test_github_rate_limit_exceeded(client, monkeypatch):
    monkeypatch.setattr("requests.get", get_mock_object('rate_limit_exceeded'))
    response = client.get('/github/repositories/octocat/Hello-World')
    assert response == expected.github_rate_limit_exceeded


def test_github_unauthorized(client, monkeypatch):
    monkeypatch.setattr("requests.get", get_mock_object('unauthorized'))
    response = client.get('/github/repositories/octocat/Hello-World')
    assert response == expected.github_unauthorized


def test_connection_error(client, monkeypatch):
    monkeypatch.setattr("requests.get", MockConnectionError)
    response = client.get('/github/repositories/octocat/Hello-World')
    assert response == expected.connection_error


def test_invalid_json_error(client, monkeypatch):
    monkeypatch.setattr("requests.get", MockInvalidJson)
    response = client.get('/github/repositories/octocat/Hello-World')
    assert response == expected.invalid_json_error
