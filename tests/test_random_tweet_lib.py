import unittest

from random_tweet import random_tweet_lib


class TestOAuthError(unittest.TestCase):
    def test_message(self):
        msg = 'Oh Foobar.'
        try:
            raise random_tweet_lib.OAuthError(msg)
        except random_tweet_lib.OAuthError as e:
            self.assertEqual(str(e), msg)


class TestOutput(unittest.TestCase):
    def test_format_of_tweet_without_media(self):
        tweet = {
            'user': {
                'screen_name': 'John',
            },
            'text': 'test text',
        }
        output = random_tweet_lib.format_tweet(tweet)

        self.assertEquals("@John: test text\n", output)

    def test_format_of_tweet_with_media(self):
        tweet = {
            'user': {
                'screen_name': 'John',
            },
            'text': 'test text',
            'entities': {
                'media': [{
                    'media_url_https': 'https://hello.com/test.jpg',
                }]
            }
        }
        output = random_tweet_lib.format_tweet(tweet)

        self.assertEquals("@John: test text\nmedia: https://hello.com/test.jpg\n", output)


if __name__ == "__main__":
    import os
    import sys
    sys.path[0:0] = [os.path.join(os.path.dirname(__file__), ".."),]
    print(sys.path)
    unittest.main()
