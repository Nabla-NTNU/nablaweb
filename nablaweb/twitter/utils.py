# For tweeting
import tweepy
import imp
import os


def authorize():
    """Autoriserer mot Twitter og returnerer et API"""
    # Importerer filen som inneholder API keys
    # Denne ligger utenfor Git av sikkerhetsgrunner
    key = imp.load_source("twitter_api_keys", '/home/andreros/twitter_api_keys.py')
    
    # Autoriser mot Twitter
    auth = tweepy.OAuthHandler(key.consumer_key, key.consumer_secret)
    auth.set_access_token(key.access_key, key.access_secret)
    return tweepy.API(auth)

def tweet(message):
    """Twitrer en melding fra nabla_ntnu"""
    api = authorize()
    api.update_status(message)
