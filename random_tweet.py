import sys

from random_tweet.random_tweet_lib import get_random_tweet, format_tweet


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


if __name__ == "__main__":
    """
    Main entry point for the command line application
    """

    term = ""

    try:
        term = sys.argv[1]
    except IndexError:
        print("Error: No search term entered.")
        print("Usage: python random_tweet.py <search_term>")
        exit(1)

    credentials = {}

    try:
        credentials = load_credentials('./credentials')
    except IOError:
        print('"Credentials" file not found')
        exit(1)

    tweet = get_random_tweet(term, credentials)

    if not tweet:
        print("No tweets were found with that search term. You can try a different term or try again later.")
        exit(1)

    print(format_tweet(tweet))
