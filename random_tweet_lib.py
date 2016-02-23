import random
from urllib import parse

import base64
import requests

MAX_PAYLOAD_TWEETS = 100


class OAuthError(Exception):
    pass


def get_bearer_token(key, secret):
    """
    OAuth2 function using twitter's "Application Only" auth method.
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
        'q': term,
        'count': MAX_PAYLOAD_TWEETS,
        'geocode': get_random_geocode(),
    }

    resp = requests.get(
        'https://api.twitter.com/1.1/search/tweets.json',
        params=request_params,
        headers=all_headers
    )

    return resp.json()


def get_random_geocode() -> str:
    """
    Return a random geocode string to use in a twitter query
    :return:
    """
    geo_codes = [
        '40.7255839,-73.9885036,100mi',  # New York City
        '34.041474,-118.260043,100mi',  # Los Angeles
        '37.787976,-122.403191,100mi',  # San Francisco
        '30.270878,-97.741725,100mi',  # Austin
        '51.507171,-0.127768,100mi',  # London
        '43.657580,-79.387678,100mi',  # Toronto
        '25.809785,-80.278805,100mi',  # Florida
        '33.750689,-84.389658,100mi',  # Atlanta
        # Blank entries will randomly disable geo fencing feature
        '',
        '',
        '',
        '',
        '',
    ]
    return random.SystemRandom().choice(geo_codes)


def get_random_tweet(term, credentials):
    """
    Given a search term and dict credentials, return a random tweet via Twitter search
    """
    bearer_token = get_bearer_token(
            credentials['consumer_key'],
            credentials['consumer_secret']
    )
    tweets = get_tweets(term, bearer_token)

    if len(tweets['statuses']) == 0:
        return None

    return random.SystemRandom().choice(tweets['statuses'])


def format_tweet(tweet):
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
