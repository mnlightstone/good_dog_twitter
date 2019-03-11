import tweepy
from credentials import *
from time import sleep


def setup():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def run_search(cursor):
    for tweet in cursor:
        try:

            # if this post has a picture or video AND it is not a retweet
            if 'media' in tweet.entities and 'RT ' not in tweet.full_text:

                # retweet
                tweet.retweet()
                print('Retweeted a tweet')
                print(tweet.entities['media'][0]['media_url'], "\n")

                # wait 2:00
                sleep(120)
            # else:
            #     print("skipping id" + tweet.id)

        except tweepy.TweepError as e:
            print(e.reason)

        except KeyError:
            print("No media to retweet")

        except StopIteration:
            break


if __name__ == '__main__':
    first = True
    api = setup()


    # run forever
    while True:

        # if running for the first time, start at the beginning
        if first:
            starting_id = 0

        # otherwise, start where I last tweeted
        else:
            starting_id = api.user_timeline("gooddogs10", count=1)
            starting_id = starting_id[0].id
            first = False

        # make cursor with hashtags, starting ID, and getting 280char tweets
        tweepy_cursor = tweepy.Cursor(api.search, q='#gooddog OR #cutedog OR #dogsoftwitter', since_id=starting_id, tweet_mode='extended').items()

        # perform search and retweets
        run_search(tweepy_cursor)
