from getpass import getpass
from pyjokes import get_joke
from time import sleep, time
import util
import logging

class Token:
    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token


def time_logger(fn):
    def wrapper(*args, **kwargs):
        start = time()
        res = fn(*args, **kwargs)
        print(f'(time taken: {time() - start} ms')
        return res
    return wrapper

def login():
    print("Please login to your account")

    username = input("Username: ")
    password = getpass()

    data = {"username": username,
            "password": password}
    headers = {"Content-type": "application/json"}
    
    print("logging in ...")
    result = util.NetworkRequest.post(endpoint='/api/auth', data=data, headers=headers)

    while(not (result.__contains__('code') and result['code']==200)):
        print("\nLogin failed. Try again ...")
        result = login()
    
    print('Log in successful')
    return result


def refreshToken(refresh_token):
    data = {"refresh_token": refresh_token}
    headers = {"Content-type": "application/json"}
    
    return util.NetworkRequest.post(endpoint='/api/auth/token', data=data, headers=headers)


@time_logger
def getRecentTweets(access_token):
    print('Checking recent tweets ...')
    headers = {"Authorization": f"Bearer {access_token}"}
    return util.NetworkRequest.get(endpoint='/api/tweets', headers=headers)

@time_logger
def postATweet(access_token, tweet):
    data = {"text": tweet}
    headers = { "Authorization": f"Bearer {access_token}",
                "Content-type": "application/json"}

    return util.NetworkRequest.post(endpoint='/api/tweets', headers=headers, data=data)
    
def getUserTokens(tokens):
    return Token(tokens['body']['access_token'], 
                 tokens['body']['refresh_token'])

def main():
    tokens = login()

    userTokens = getUserTokens(tokens)
    
    recentTweets = getRecentTweets(userTokens.access_token)
    if(recentTweets['code'] == 401):
        tokens = refreshToken(userTokens.refresh_token)
        userTokens = getUserTokens(tokens)
        recentTweets = getRecentTweets(tokens.access_token)

    alreadyPostedTweets = set()
    for tweet in recentTweets['body']:
        print(f"({tweet['id']}) {tweet['author']['firstname']} tweeted at {tweet['author']['created_at']}")
        print(f"{tweet['text']}\n")
        alreadyPostedTweets.add(tweet['text'])

    for i in range(10):
        joke = get_joke()
        while(alreadyPostedTweets.__contains__(joke)):
            joke = get_joke()

        print('Posting tweet')
        print(joke)

        result = postATweet(userTokens.access_token, joke)

        if(result.__contains__('code') and result['code'] == 201):
            alreadyPostedTweets.add(joke)
            print('posted tweet. Sleeping 1 min now\n')
            sleep(60)
        elif(result.__contains__('code') and result['code'] == 401):
            tokens = refreshToken(userTokens.refresh_token)
            userTokens = getUserTokens(tokens)
            result = postATweet(userTokens.access_token, joke)

            if(result.__contains__('code') and result['code'] == 201):
                alreadyPostedTweets.add(joke)
                print('posted tweet. Sleeping 1 min now\n')
                sleep(60)


if __name__ == '__main__':
    main()
