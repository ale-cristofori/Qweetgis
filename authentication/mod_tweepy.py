# -*- coding: utf-8 -*-

import tweepy
import pdb
import simplejson
import os
from PyQt5.QtCore import QObject, pyqtSignal, pyqtRemoveInputHook
from PyQt5.QtWidgets import QMessageBox
from ..gui.gui_messages import ConfigErrorMessageBox


class Signals(QObject):
    tweet_received = pyqtSignal(dict)
    tweet_file = pyqtSignal(str)
    stream_error = pyqtSignal(int)
    update_progress = pyqtSignal(int)


class TweetsHandler:
    def __init__(self):
        self.consumer_token = ''
        self.consumer_secret = ''
        self.auth = tweepy.OAuthHandler(self.consumer_token, self.consumer_secret)
        try:
            second_public_token=''
            second_secret_token=''
            third_public_token=''
            third_secret_token=''
            # self.auth.set_access_token('',
            # '')
            # self.auth.set_access_token(third_public_token, third_secret_token)
            # self.api = tweepy.API(self.auth)
            redirect_url = self.auth.get_authorization_url()
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
    def __init__(self, tweet_to_layer, stream_signal, error_signal, update_progress,
                 tweet_to_file, emit_stop, api=None, limit=None, limit_type=None):
        self.api = api
        self.tweet_to_layer = tweet_to_layer
        self.tweet_to_file = tweet_to_file
        self.update_progress = update_progress
        self.emit_stop = emit_stop
        self.limit = limit
        self.limit_type = limit_type
        self.error_signal = error_signal
        self.tweet_signals = Signals()
        self.tweet_signals.tweet_received.connect(self.tweet_to_layer)
        self.tweet_signals.tweet_file.connect(self.tweet_to_file)
        self.tweet_signals.update_progress.connect(self.update_progress)
        self.tweet_signals.stream_error.connect(self.error_signal)
        self.stream_signal = stream_signal
        self.stream_signal.connect(self.set_stream)
        self.stream_on = True
        self.counter = 1
        if self.limit_type == 'absolute':
            self.stream_on = bool(self.stream_on and
                                  self.counter <= self.limit)
                                  
    def set_stream(self):
        self.stream_on = False
    
    def on_error(self, status_code):
        if status_code == 420:
            self.tweet_signals.stream_error.emit(status_code)
            # returning False in on_error disconnects the stream
            return False
    
    def check_limit(self):
        self.stream_on = bool(self.stream_on and self.counter <= self.limit)
    
    def get_tweet_text(self, status):
        if hasattr(status, 'retweeted_status'):
            try:
                text = status.retweeted_status.extended_tweet["full_text"]
            except:
                text = status.retweeted_status.text
        else:
            try:
                text = status.extended_tweet["full_text"]
            except AttributeError:
                text = status.text
        return text


class PlaceStreamListener(BaseStreamListener):
    def __init__(self, tweet_to_layer, stream_signal,
                 error_signal, update_progress, tweet_to_file, 
                 emit_stop, api=None, limit=None, limit_type=None):
        super().__init__(tweet_to_layer, stream_signal,
                         error_signal, update_progress, tweet_to_file,
                         emit_stop, api, limit, limit_type)

    def on_status(self, status):
        try: 
            while self.stream_on:
                output_object = {
                    'status_id': status.id_str,
                    'tweet': self.get_tweet_text(status),
                    'user': status.user.screen_name,
                    'place': status.place,
                    'localization': status.user.location,
                    'time_zone': status.user.time_zone,
                    'time': status.timestamp_ms
                }
                if status.place is not None:
                    self.tweet_signals.tweet_received.emit(output_object)
                    self.counter += 1
                    if self.limit_type == 'absolute':
                        progress = (self.counter * 100) / self.limit
                        self.tweet_signals.update_progress.emit(progress)
                        self.check_limit()
                return True
            self.emit_stop()
            return False
        except Exception as e:
            self.tweet_signals.stream_error.emit("Fatal Error")
            return False


class GeoStreamListener(BaseStreamListener):
    def __init__(self, tweet_to_layer, stream_signal, error_signal,
                 update_progress, tweet_to_file, emit_stop,
                 api=None, limit=None, limit_type=None):
        super().__init__(tweet_to_layer, stream_signal, error_signal,
                         update_progress, tweet_to_file, emit_stop, 
                         api, limit, limit_type)
    
    def on_status(self, status):
        try:
            while self.stream_on:
                output_object = {
                    'status_id': status.id_str,
                    'tweet':  self.get_tweet_text(status),
                    'user': status.user.screen_name,
                    'geo': status.geo,
                    'place': status.place,
                    'localization': status.user.location,
                    'time_zone': status.user.time_zone,
                    'time': status.timestamp_ms
                }
                if status.geo is not None:
                    self.tweet_signals.tweet_received.emit(output_object)
                    self.counter += 1
                    if self.limit_type == 'absolute':
                        progress = (self.counter * 100) / self.limit
                        self.tweet_signals.update_progress.emit(progress)
                        self.check_limit()
                return True
            self.emit_stop()
            return False
        except Exception as e:
            self.tweet_signals.stream_error.emit("Fatal Error:")
            return False


class TweetsAuthHandler():
    def __init__(self, **kwargs):
        self.consumer_token = kwargs['CONSUMER_KEY']
        self.consumer_secret = kwargs['CONSUMER_KEY_SECRET']
        self.access_token = kwargs['ACCESS_TOKEN']
        self.access_token_secret = kwargs['ACCESS_TOKEN_SECRET']
        self.auth = tweepy.OAuthHandler(self.consumer_token, self.consumer_secret)
        try:
            self.auth.set_access_token(self.access_token, self.access_token_secret)
            self.proxy = self.get_user_proxy()
            self.api = tweepy.API(self.auth, proxy=self.proxy)
        except tweepy.TweepError:
            print('Error! Failed to set request token.')
    
    def get_user_proxy(self):
        """ read-in the config proxy server from the 
            config/config.json file
        """
        try:
            proxy = None
            with open(os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 'config', 'config.json'), 'r') as f:
                config = simplejson.load(f)
                proxy = config['PROXY'] if config['PROXY'] != '' else None
        except IOError:
            proxy = None
        finally:
            return proxy
    
    def get_api_obj(self):
        return self.api


class TestTweetsAuthHandler(TweetsAuthHandler):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def test_credentials(self):
        try:
            searched_tweets = self.api.search(q='belen', lang='it')
            texts = []
            for t in searched_tweets:
                texts.append(t.text)
            if len(texts) == 0:
                return (QMessageBox.Warning, 'Credentials are correct \n'
                        ' but API test returned 0 results')
            return (QMessageBox.Information, 'Credentials are correct')
        except tweepy.TweepError as e:
            message = simplejson.loads(e.response.text)['errors'][0]['message']
            return(QMessageBox.Critical, message)

if __name__ == "__main__":
    cred = {
        'CONSUMER_KEY': '',
        'CONSUMER_KEY_SECRET': '',
        'ACCESS_TOKEN': '',
        'ACCESS_TOKEN_SECRET': ''
        }
    tweets_handler = TestTweetsAuthHandler(**cred)
    tweets_handler.test_credentials()
#    print('success')
    # js_handler = JSHandler()
    # api_obj = tweets_handler.get_api_obj()
    # stream_listener = MyStreamListener()