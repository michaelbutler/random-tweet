import base64
from urllib import parse
import requests


class OAuthError(Exception):
    pass


def load_credentials(filepath: str) -> dict:
    """
    Load a file containing key and secret credentials, separated by a line break (\n)
    Returns a dict with the corresponding credentials
    """
    with open(filepath, 'r') as file_resource:
        data = file_resource.read().strip().split('\n')
    return {
        'consumer_key': data[0],
        'consumer_secret': data[1]
    }


def get_bearer_token(key: str, secret: str) -> str:
    """
    With key and secret, make a POST request to get a bearer token that is used in future API calls
    """
    creds = parse.quote_plus(key) + ':' + parse.quote_plus(secret)
    encoded_creds = base64.b64encode(creds.encode('ascii'))

    all_headers = {
        "Authorization": "Basic " + encoded_creds.decode(encoding='UTF-8'),
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent": "butlerpc.net Random-Tweet Search App"
    }

    body_content = {
        'grant_type': 'client_credentials'
    }

    resp = requests.post(
        'https://api.twitter.com/oauth2/token',
        data=body_content,
        headers=all_headers
    )

    json = resp.json()

    if json['token_type'] != 'bearer':
        raise OAuthError("Did not receive bearer token on initial POST")

    return json['access_token']


def get_tweets(term, bearer_token):
    """
    Given a search term and bearer_token, return a dict of tweets from the API
    """
    all_headers = {
        "Authorization": "Bearer " + bearer_token,
        "User-Agent": "butlerpc.net Random-Tweet Search App"
    }

    request_params = {
        'q': term
    }

    resp = requests.get(
        'https://api.twitter.com/1.1/search/tweets.json',
        params=request_params,
        headers=all_headers
    )

    return resp.json()


credentials = load_credentials('./credentials')

bearer_token = get_bearer_token(
        credentials['consumer_key'],
        credentials['consumer_secret']
)

tweets = get_tweets('html5', bearer_token)

print(tweets)
