import dateutil.parser


def read_github_token_from_file():
    """Read github api token from file.

    Returns:
        str: token or empty string if no file or empty file.

    """
    token = ''
    try:
        with open('github_token.key', 'r') as f:
            for line in f:
                token = line.rstrip() if line.startswith('token') else token
    except FileNotFoundError:
        return ''
    else:
        return token


def parse_datetime(datetime_string):
    """Parse ISO 8601 datetime string.

    Args:
        datetime_string (str): date and time in format '2016-02-23T13:44:18Z'

    Returns:
        str: only date

    """
    dt = dateutil.parser.parse(datetime_string)
    date_string = str(dt.date())

    return date_string
