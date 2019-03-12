import tweepy
from credentials import *
from time import sleep
import sys

def setup():
    api = None
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    while api is None:
        try:
            api = tweepy.API(auth)
            return api

        except tweepy.TweepError as e:
            print(e)
            if e.api_code == 429:
                wait_fifteen_minutes(e)


def run_search(cursor):
    blacklist = ['designs', 'company', 'mr dad official', 'co', 'store', 'trainer']

    # counter to 100 so that we periodically get a new batch of tweets instead of running through ALL of the
    # historic tweets
    count = 0
    GET_NEW_TWEETS = 100

    for tweet in cursor:
        if count > GET_NEW_TWEETS:
            break
        try:

            # if this post has a picture or video AND it is not a retweet AND it is not in our blacklist list
            if 'media' in tweet.entities \
                    and 'RT ' not in tweet.full_text\
                    and not any(s in tweet.author.screen_name.lower() for s in blacklist):

                # retweet
                # tweet.retweet()
                # print('Retweeted a tweet')
                print(tweet.entities['media'][0]['media_url'], "\n")

                # wait 5:00
                sleep(0)
                count += 1

        except tweepy.TweepError as e:
            if e.api_code == 429:
                wait_fifteen_minutes(e)

        except KeyError:
            print("No media to retweet")

        except StopIteration:
            break

        except:
            print("Unexpected error:", sys.exc_info()[0])
            print("something else went wrong")


def wait_fifteen_minutes(error):
    print("waiting 15 min")
    print(error.reason)
    sleep(300)


if __name__ == '__main__':
    api = setup()
    # filte
    # gooddog filter:media -filter:retweets
    # run forever
    while True:
        try:
            # make cursor with hashtags, including 280char tweets
            tweepy_cursor = tweepy.Cursor(api.search, q='#gooddog OR #cutedog OR #dogsoftwitter', tweet_mode='extended').items()

            # perform search and retweets
            run_search(tweepy_cursor)

        # if getting the cursor fails, it most likely means we have hit the 15 requests in 15 minutes error
        except tweepy.TweepError as e:
            if e.api_code == 429:
                wait_fifteen_minutes(e)


