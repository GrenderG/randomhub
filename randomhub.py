#!/usr/bin/python

import tweepy
import requests

import threading
import time
import json
from random import randint


## Load keys and tokens

with open('secret.json') as secret_json:
    secret = json.load(secret_json)


## Twitter

# Consumer keys and access tokens, used for OAuth
consumer_key = secret['twitter']['consumer_key']
consumer_secret = secret['twitter']['consumer_secret']
access_token = secret['twitter']['access_token']
access_token_secret = secret['twitter']['access_token_secret']
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)


## Github

base_url = 'https://api.github.com/'
repo_endpoint = 'repositories'

access_token = secret['github']['access_token']

random_repo_url = base_url + repo_endpoint

def generate_random_id():
    last_id = 105604879
    return randint(0, last_id)

def get_random_repo():
    repo_id = generate_random_id()
    repo_payload = {'since': str(repo_id), 'access_token':access_token}
    r = requests.get(random_repo_url, params=repo_payload)
    return r.json()[0]

def generate_tweet():
    repo = get_random_repo()
    repo_name = repo['name']
    repo_url = repo['html_url']
    return '%s %s' % (repo_name, repo_url)

def update_status():
    threading.Timer(3600.0, update_status).start() # Every 1 hour
    tweet = generate_tweet()
    print '[%s] Randomhub - Generated tweet: %s' % (str(time.strftime("%H:%M:%S")), tweet)
    api.update_status(tweet)

if __name__ == '__main__':
    update_status()
