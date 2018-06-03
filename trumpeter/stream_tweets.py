"""
Get tweets for Trump by walking his timeline,
create a JSON file for each, identified by its ID.
"""

from os import environ, remove
import tweepy
import json
from google.cloud import storage

# Global vars: user ID to fetch tweets for and API params
TRUMP_USER_ID = environ['TRUMP_USER_ID']
TWITTER_API_KEY = environ['TWITTER_API_KEY']
TWITTER_API_SECRET = environ['TWITTER_API_SECRET']
TWITTER_API_ACCESS_TOKEN = environ['TWITTER_API_ACCESS_TOKEN']
TWITTER_API_ACCESS_TOKEN_SECRET = environ['TWITTER_API_ACCESS_TOKEN_SECRET']


def connect_to_twitter(api_key,
                       api_secret,
                       api_access_token,
                       api_access_token_secret):
    """
    Connect to the Twitter API, autorizing via OAuth.
    Allows 900 requests per 15 minutes window.
    """

    twitter_auth = tweepy.OAuthHandler(api_key, api_secret)
    twitter_auth.set_access_token(api_access_token, api_access_token_secret)

    return tweepy.API(twitter_auth,
                      wait_on_rate_limit=True,
                      wait_on_rate_limit_notify=True)


def fetch_tweets(user_id, bucket):
    """
    Fetch user's tweets and create a JSON dump for each.

    Queries the user_timeline endpoint with Tweepy, which yields the 3200
    most recent tweets. Retweets excluded; mind that user might have still
    typed "RT" in a tweet though, to mentions someone else's tweet.
    """

    # Get the IDs of all tweets in the bucket
    existing_tweets_ids = [blob.name.split('.')[0]
                           for blob in bucket.list_blobs()]

    print('Number of existing tweets: ', len(existing_tweets_ids))

    # Query the user timeline and put into bucket new ones
    # (unless same ID is encountered, as tweets are sorted by recency)
    c = tweepy.Cursor(tweepy_api.user_timeline,
                      user_id=TRUMP_USER_ID).items()
    while True:
        try:
            tweet = c.next()
            tweet_id = str(tweet.id)

            print(tweet_id)

            if tweet_id in existing_tweets_ids:
                break

            # write to JSON file by ID
            json.dump(tweet._json, open(tweet_id + '.json', 'w'))

            blob = bucket.blob(tweet_id + '.json')
            blob.upload_from_file(open(tweet_id + '.json', 'rb'),
                                  content_type='application/json')

            remove(tweet_id + '.json')

        except StopIteration:
            break

    # print current API limits
    print('API limits: ', tweepy_api.rate_limit_status()['resources'])


if __name__ == '__main__':

    # Connect to the Twitter API
    tweepy_api = connect_to_twitter(TWITTER_API_KEY,
                                    TWITTER_API_SECRET,
                                    TWITTER_API_ACCESS_TOKEN,
                                    TWITTER_API_ACCESS_TOKEN_SECRET)

    # Client and bucket to connect to Google Storage
    client = storage.Client()
    bucket = client.get_bucket('tweepy-trump-tweets')

    # Fetch tweets for user
    fetch_tweets(TRUMP_USER_ID, bucket)
