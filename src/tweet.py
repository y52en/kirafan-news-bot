import os
import tweepy

# 認証に必要なキーとトークン
API_KEY = os.environ["twitter_newsbot_api_key"]
API_SECRET = os.environ["twitter_newsbot_api_secret"]
ACCESS_TOKEN = os.environ["twitter_newsbot_access_token"]
ACCESS_TOKEN_SECRET = os.environ["twitter_newsbot_token_secret"]

# APIの認証
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


def tweet(tweet_str):
    api.update_status(tweet_str)
