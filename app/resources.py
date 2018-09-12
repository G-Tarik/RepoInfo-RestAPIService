from flask import current_app, url_for, jsonify
from flask_restful import Resource


class ApiRoot(Resource):
    """Class for root endpoint.

    Show list of all endpoints.

    """

    def get(self):
        """Get list of all endpoints.

        Returns:
            tuple: (json message, status code (default 200))

        """
        urls = get_all_endpoints_urls()

        return urls


def get_all_endpoints_urls():
    """Generate list of urls for all endpoints.

    Returns:
        json message

    """
    root_url = url_for('root_api.endpoints_list', _external=True).rstrip('/')
    urls = {rule.endpoint: root_url + str(rule)
            for rule in current_app.url_map.iter_rules() if rule.endpoint != 'static'}
    urls = dict(sorted(urls.items()))

    return jsonify(urls)
