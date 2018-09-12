"""Expected results for tests.

Values which could change frequently
should be adjusted here after new mock data were generated.

"""

root = {"root_api.endpoints_list": "http://localhost/",
        "github_api.rate_limit": "http://localhost/github/rate_limit",
        "github_api.repository": "http://localhost/github/repositories/<owner>/<repo_name>"
        }


github_repo = {"fullName": "octocat/Hello-World",
               "description": "My first repository on GitHub!",
               "cloneUrl": "https://github.com/octocat/Hello-World.git",
               "stars": 1455,
               "createdAt": "2011-01-26"}

github_rate_limit = {"limit": 60,
                     "remaining": 59,
                     "reset": 1535227090
                     }

github_rate_limit_exceeded = {'message': 'API rate limit exceeded.',
                              'documentation_url': 'https://developer.github.com/v3/#rate-limiting'}

github_unauthorized = {'message': 'Bad credentials',
                       'documentation_url': 'https://developer.github.com/v3'}

connection_error = {'error': {'message': 'connection to github is not available'}}

invalid_json_error = {'error': {'message': 'response does not contain valid json'}}
