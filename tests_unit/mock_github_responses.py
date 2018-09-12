"""Collects responses from github, used for creating mocks in tests.

Some responses are already hard coded as can be seen below.
Other live responses are added to predefined dictionary.
Save result to file with name given in EXPORT_FILE attribute.

Attributes:
    EXPORT_FILE (str): file name where to save serialized json string.
    GITHUB_ENDPOINTS (list(dict)): urls of endpoints and expected status codes.
    response_data (dict(dict(dict))): first level keys correspond with test names,
                                      second level keys - body and status code of response.


"""
import json
import requests


EXPORT_FILE = 'github_responses.json'

GITHUB_ENDPOINTS = [{'url': 'https://api.github.com/repos/octocat/Hello-World', 'status_code': 200},
                    {'url': 'https://api.github.com/rate_limit', 'status_code': 200},
                    {'url': 'https://api.github.com/repos/fakeuser/fakerepo', 'status_code': 404}]

response_data = {'rate_limit_exceeded': {'body': {'message': 'API rate limit exceeded.',
                                                  'documentation_url': 'https://developer.github.com/v3/#rate-limiting'},
                                         'status_code': 403},
                 'unauthorized': {'body': {'message': 'Bad credentials',
                                           'documentation_url': 'https://developer.github.com/v3'},
                                  'status_code': 401}}


def fetch_responses():
    """Get real responses from github and add them to response_data dictionary.

    Returns:
        dict: If at least one url will not respond with proper result,
              returns empty dict.

    """
    for endpoint in GITHUB_ENDPOINTS:
        try:
            response = requests.get(endpoint['url'])
        except requests.exceptions.ConnectionError:
            print('Can\'t connect to the {}. Exiting program.'.format(endpoint['url']))
            return {}
        if response.status_code != endpoint['status_code']:
            print('Unexpected response from {}. Exiting program.'.format(endpoint['url']))
            return {}

        response_data[endpoint['url']] = {'body': response.json(),
                                          'status_code': response.status_code}

    return response_data


if __name__ == '__main__':
    data = fetch_responses()
    if data:
        with open(EXPORT_FILE, 'w') as f:
            json.dump(data, f)
