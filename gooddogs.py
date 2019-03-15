import tweepy
from time import sleep
import sys

from os import environ


def setup():
    api = None
    consumer_key = environ['consumer_key']
    consumer_secret = environ['consumer_secret']
    access_token = environ['access_token']
    access_token_secret = environ['access_token_secret']

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

    # words in the author's name that we won't retweet
    blacklist = ['designs', 'company', 'co', 'store', 'trainer', 'mr dad official', ]

    # counter to 100 so that we periodically get a new batch of tweets instead of running through
    # every tweet in the history of Good Dogs
    GET_NEW_CURSOR = 100
    count = 0


    for tweet in cursor:
        # if we've run more than 100 times, break and get a new cursor
        if count > GET_NEW_CURSOR:
            break
        try:

            # if this tweet's author's name is not in our blacklist
            if not any(s in tweet.author.screen_name.lower() for s in blacklist):

                # retweet
                tweet.retweet()

                # print some stuff to the console
                print('Retweeted a tweet:', tweet.full_text[:50] + "...")
                print(tweet.entities['media'][0]['media_url'], "\n")

                # wait 15:00
                sleep(900)
                count += 1

        except tweepy.TweepError as e:
            if e.api_code == 429:
                wait_fifteen_minutes(e)

        except KeyError:
            print("No media to retweet")

        except StopIteration:
            break

        except:
            print("Something went wrong...")
            print(sys.exc_info()[0])


def wait_fifteen_minutes(error):
    print("Hit the API limit - waiting 15 minutes to re-try")
    print(error.reason)
    sleep(300)


if __name__ == '__main__':
    api = setup()

    # run forever
    while True:
        try:

            # make cursor with hashtags. tweet_mode argument includes 280char tweets
            tweepy_cursor = tweepy.Cursor(api.search,
                                          q='#gooddog OR #cutedog OR #dogsoftwitter ' +
                                            'filter:media ' +
                                            '-filter:retweets ' +
                                            'min_faves:200',
                                          tweet_mode='extended').items()

            # perform search and retweets
            run_search(tweepy_cursor)

        # if getting the cursor fails, it most likely means we have hit the 15 requests in 15 minutes error
        except tweepy.TweepError as e:
            if e.api_code == 429:
                wait_fifteen_minutes(e)


