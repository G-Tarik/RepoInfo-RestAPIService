from flask import Blueprint
from flask_restful import Api
from . import github_resources as github
from .resources import ApiRoot

root_api_bp = Blueprint('root_api', __name__)
root_api = Api(root_api_bp)

github_api_bp = Blueprint('github_api', __name__, url_prefix='/github')
github_api = Api(github_api_bp)

github_api.add_resource(github.GithubRepos, '/repositories/<owner>/<repo_name>', endpoint='repository')
github_api.add_resource(github.GithubRateLimit, '/rate_limit', endpoint='rate_limit')

root_api.add_resource(ApiRoot, '/', endpoint='endpoints_list')
