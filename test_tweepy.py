import tweepy
import requests
import pdb
from PyQt5 import QtCore


class Signals(QtCore.QObject):
    tweet_received = QtCore.pyqtSignal(dict)
    tweet_file = QtCore.pyqtSignal(str)
    stream_error = QtCore.pyqtSignal(int)


class TweetsHandler:
    def __init__(self):
        self.consumer_token = 'your consumer Key'
        self.consumer_secret = 'your consumer SECRET Key'
        self.auth = tweepy.OAuthHandler(self.consumer_token, self.consumer_secret)
        try:
            self.auth.set_access_token('your access token',
            'your access SECRET token') 
            self.api = tweepy.API(self.auth)
            # redirect_url = self.auth.get_authorization_url()
            # print(redirect_url)
            # print(self.auth.request_token.oauth_token)
            # print(self.auth.request_token.oauth_token_secret)
            # request_token = self.auth.request_token
            # verifier = input('Verifier:')
            # print(verifier)
            # self.auth.get_access_token(self.auth.request_token)
            # self.access_token = self.auth.access_token
            # self.access_token_secret = self.auth.access_token_secret
            # self.auth.set_access_token(self.auth.request_token['oauth_token'], self.auth.request_token['oauth_token_secret'])
            # self.auth = tweepy.OAuthHandler(self.consumer_token, self.consumer_secret)
            # self.auth.request_token = {
            #     'oauth_token': self.auth.request_token,
            #     'oauth_token_secret': verifier
            # }
            # self.auth.set_access_token
            # self.auth.get_access_token(verifier)

        except tweepy.TweepError:
            print('Error! Failed to get request token.')
        
    def search_tweets(self, query, language):
        searched_tweets = self.api.search(q=query, lang=language)
        texts = []
        for t in searched_tweets:
            texts.append(t.text)
        return texts


class BaseStreamListener(tweepy.StreamListener):
    def __init__(self, tweet_to_layer, stream_signal, error_signal, tweet_to_file, api=None):
        self.api = api
        self.tweet_to_layer = tweet_to_layer
        self.tweet_to_file = tweet_to_file
        self.error_signal = error_signal
        self.tweet_signals = Signals()
        self.tweet_signals.tweet_received.connect(self.tweet_to_layer)
        self.tweet_signals.tweet_file.connect(self.tweet_to_file)
        self.tweet_signals.stream_error.connect(self.error_signal)
        self.stream_signal = stream_signal
        self.stream_signal.connect(self.set_stream)
        self.stream_on = True

    def set_stream(self):
        self.stream_on = False
    
    def on_error(self, status_code):
        if status_code == 420:
            self.tweet_signals.stream_error.emit(status_code)
            #returning False in on_error disconnects the stream
            return False


class PlaceStreamListener(BaseStreamListener):
    def __init__(self, tweet_to_layer, stream_signal, error_signal, tweet_to_file, api=None):
        super().__init__(tweet_to_layer, stream_signal, error_signal, tweet_to_file, api=None)
    def on_status(self, status):
        while self.stream_on:
            output_object = {
                'status_id': status.id_str,
                'tweet':status.text,
                'user':status.user.screen_name,
                'place':status.place,
                'localization':status.user.location,
                'time_zone':status.user.time_zone,
                'time':status.timestamp_ms
            }
            if status.place is not None:
                self.tweet_signals.tweet_received.emit(output_object)
            return True
        return False


class GeoStreamListener(BaseStreamListener):
    def __init__(self, tweet_to_layer, stream_signal, error_signal, tweet_to_file, api=None):
        super().__init__(tweet_to_layer, stream_signal, error_signal, tweet_to_file, api=None)
    def on_status(self, status):
        while self.stream_on:
            output_object = {
                'status_id': status.id_str,
                'tweet':status.text,
                'user':status.user.screen_name,
                'geo':status.geo,
                'place':status.place,
                'localization':status.user.location,
                'time_zone':status.user.time_zone,
                'time':status.timestamp_ms
            }
            if status.geo is not None:
                self.tweet_signals.tweet_received.emit(output_object)
            return True
        return False


class TweetsAuthHandler():
    def __init__(self):
        self.consumer_token = 'your consumer Key'
        self.consumer_secret = 'your consumer SECRET Key'
        self.auth = tweepy.OAuthHandler(self.consumer_token, self.consumer_secret)
        try:
            self.auth.set_access_token('your access token',
            'your access SECRET token')
            self.api = tweepy.API(self.auth)
        except tweepy.TweepError:
            print('Error! Failed to get request token.')
    
    def get_api_obj(self):
        return self.api

if __name__ == "__main__":
    tweets_handler = TweetsHandler()
    # api_obj = tweets_handler.get_api_obj()
    # stream_listener = MyStreamListener()