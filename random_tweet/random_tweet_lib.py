import random
from urllib import parse

import base64
import requests

# The maximum possible tweets to return in the search request. 100 is the max allowed by Twitter
MAX_PAYLOAD_TWEETS = 100

# Customize the user agent used in the Twitter HTTP requests
API_USER_AGENT = "butlerpc.net Random-Tweet Search App"


class OAuthError(Exception):
    """
    Basic exception for OAuth or token errors
    """
    pass


def _get_bearer_token(key, secret):
    """
    OAuth2 function using twitter's "Application Only" auth method.
    With key and secret, make a POST request to get a bearer token that is used in future API calls
    """

    creds = parse.quote_plus(key) + ':' + parse.quote_plus(secret)
    encoded_creds = base64.b64encode(creds.encode('ascii'))

    all_headers = {
        "Authorization": "Basic " + encoded_creds.decode(encoding='UTF-8'),
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "User-Agent": API_USER_AGENT,
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

    if json['token_type'] != 'bearer' or 'access_token' not in json:
        raise OAuthError("Did not receive proper bearer token on initial POST")

    return json['access_token']


def _get_tweets(term, bearer_token):
    """
    Given a search term and bearer_token, return a dict of tweets from the API
    """
    all_headers = {
        "Authorization": "Bearer " + bearer_token,
        "User-Agent": API_USER_AGENT
    }

    request_params = {
        'q': term,
        'count': MAX_PAYLOAD_TWEETS,
    }

    resp = requests.get(
        'https://api.twitter.com/1.1/search/tweets.json',
        params=request_params,
        headers=all_headers
    )

    return resp.json()


def get_random_tweet(term, credentials):
    """
    Given a search term and dict credentials, return a random tweet via Twitter search
    """
    bearer_token = _get_bearer_token(
            credentials['consumer_key'],
            credentials['consumer_secret']
    )
    tweets = _get_tweets(term, bearer_token)

    if not tweets.get('statuses'):
        return None

    return random.SystemRandom().choice(tweets['statuses'])


def format_tweet(tweet):
    """
    Basic output formatting of the tweet (dict)
    """
    buffer = ""
    buffer += "@" + tweet['user']['screen_name'] + ": "
    buffer += tweet['text'] + "\n"

    try:
        if len(tweet['entities']['media']) > 0:
            buffer += "media: " + tweet['entities']['media'][0]['media_url_https'] + "\n"
    except KeyError:
        pass  # No media
    except IndexError:
        pass  # No media

    return buffer
