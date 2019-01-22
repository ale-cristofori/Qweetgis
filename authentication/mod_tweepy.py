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
    update_progress = pyqtSignal(int, int)
    stop_stream = pyqtSignal()


class TweetsHandler:
    """ this class is just for standalone testing"""
    def __init__(self):
        self.consumer_token = ''
        self.consumer_secret = ''
        self.auth = tweepy.OAuthHandler(self.consumer_token, self.consumer_secret)
        redirect_url = self.auth.get_authorization_url()
        verifier = self.auth.request_token['oauth_verifier']
        request_token = self.auth.request_token['oauth_token']
        self.auth.request_token = { 'oauth_token' : token, 'oauth_token_secret' : verifier }
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
    """ Base subclass of tweepy stream listener performing the stream process """
    def __init__(self, tweet_to_layer, shut_down_signal, error_signal, update_progress,
                 tweet_to_file, reset_main_dialog, api=None, limit=None, limit_type=None):
        """ 
        Constructor the class is initalised with the parameters needed to start a 
        streaming session

        :param tweet_to_layer: the slot function on the main class that 
        responds when a new tweet is received from the stream
        :type tweet_to_layer: function

        :param shut_down_signal: the signal coming from the main thread that 
        sets the parameter stream on to False, pausing the current
        streaming session
        :type shut_down_signal: pyQtsignal

        :param error_signal: the signal emitted from this class to the main 
        thread when an error occurs during streaming 
        :type error_signal: pyQtsignal

        :param update_progress: the signal emitted from this class to the main
        thread informing the progress bar of the staus fo the job 
        (percentage completed)
        :type update_progress: function

        :param tweet_to_file: the slot onthe main thread that prints the
        tweets to a text file 
        :type tweet_to_file: function

        :param reset_main_dialog: the slot on the main thread that stops the stream, 
        emitting the shut_down_signal that stops the stream on this thread
        type reset_main_dialog: function

        :param api: the tweepy API object required to connect to twitter and
        perform any action
        :type api: Tweepy.API 

        :param limit: the maximum number of tweet to retreive when streaming
        :type limit: int

        :param limit_type: the type of limit requires (absolute or dynamic)
        :type limit_type: string

        """
        self.api = api
        self.tweet_to_layer = tweet_to_layer
        self.tweet_to_file = tweet_to_file
        self.update_progress = update_progress
        self.reset_main_dialog = reset_main_dialog
        self.limit = limit
        self.limit_type = limit_type
        self.error_signal = error_signal
        self.tweet_signals = Signals()
        self.tweet_signals.tweet_received.connect(self.tweet_to_layer)
        self.tweet_signals.tweet_file.connect(self.tweet_to_file)
        self.tweet_signals.update_progress.connect(self.update_progress)
        self.tweet_signals.stream_error.connect(self.error_signal)
        self.tweet_signals.stop_stream.connect(self.reset_main_dialog)
        self.shut_down_signal = shut_down_signal
        self.shut_down_signal.connect(self.shut_stream)
        self.stream_on = True
        self.counter = 0
        if self.limit_type == 'absolute':
            self.stream_on = bool(self.stream_on and
                                  self.counter < self.limit)
                                  
    def shut_stream(self):
        """ slot for the stop to tweet signal coming from the main thread"""
        self.stream_on = False
    
    def on_error(self, status_code):
        """
        function that calls the emit signal to the main thread if an 
        error occurred while streaming

        :param status_code: the code associated with the error produced 
        from the twitter API to describe the error

        :type status_code: int

        """
        if status_code == 420:
            self.tweet_signals.stream_error.emit(status_code)
            # returning False in on_error disconnects the stream
            return False
    
    def check_limit(self):
        """ 
        function that checks at every iteration if the limit set by 
        the user has been reached or not, if so stops the tweet stream 
        
        """
        self.stream_on = bool(self.counter < self.limit)
    
    def get_tweet_text(self, status):
        """ 
        function that gets the full text from a tweet (if exists)

        :param status: the full status streamed from the Twitter API
        :type status: Object

        """
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
    def __init__(self, tweet_to_layer, shut_down_signal,
                 error_signal, update_progress, tweet_to_file, 
                 reset_main_dialog, api=None, limit=None, limit_type=None):
        super().__init__(tweet_to_layer, shut_down_signal,
                         error_signal, update_progress, tweet_to_file,
                         reset_main_dialog, api, limit, limit_type)

    def on_status(self, status):
        """ 
            This method is overridden the streaming tweepy method and runs
            on a loop on a separate thread, streaming all tweets in a loop
            at each iteration the function returns, if returns True the stream 
            continues, if returns False the stream stops

            :param status: the status returned from twitter
            :type status: Object
        """
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
                    self.counter += 1
                    tweets_count = self.counter
                    self.tweet_signals.tweet_received.emit(output_object)
                    self.tweet_signals.update_progress.emit(None, tweets_count)
                    if self.limit_type == 'absolute':
                        progress = (self.counter * 100) / self.limit
                        self.tweet_signals.update_progress.emit(progress, tweets_count)
                        self.check_limit()
                return True
            self.tweet_signals.stop_stream.emit()
            return False
        except Exception as e:
            self.tweet_signals.stream_error.emit("Fatal Error:")
            return False

class GeoStreamListener(BaseStreamListener):
    def __init__(self, tweet_to_layer, shut_down_signal, error_signal,
                 update_progress, tweet_to_file, reset_main_dialog,
                 api=None, limit=None, limit_type=None):
        super().__init__(tweet_to_layer, shut_down_signal, error_signal,
                         update_progress, tweet_to_file, reset_main_dialog, 
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
                    self.counter += 1
                    tweets_count = self.counter
                    self.tweet_signals.tweet_received.emit(output_object)
                    self.tweet_signals.update_progress.emit(None, tweets_count)
                    if self.limit_type == 'absolute':
                        progress = (self.counter * 100) / self.limit
                        self.tweet_signals.update_progress.emit(progress, tweets_count)
                        self.check_limit()
                return True
            self.tweet_signals.stop_stream.emit()
            return False
        except Exception as e:
            self.tweet_signals.stream_error.emit("Fatal Error:")
            return False


class TweetsAuthHandler():
    """ Wrapper custom class for the Tweepy API object, passed to stream 
    listener to perfomr the streaming
    """
    def __init__(self, **kwargs):
        """ 
            Constructor
            :param **kwargs: all the four items of credentials needed from the user to 
            create an authenticated valid tweepy API object
            :type **kwargs: dict
        
        """
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
        """ returns the tweepy API object 
            :returns self.api: the instantiated API object
            :rtype self.api: Object 
        """
        return self.api


class TestTweetsAuthHandler(TweetsAuthHandler):
    """ This class is a utilty test for the credentials
        inputted from the user in case they want to 
        test if they are correct or not
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """ 
            Constructor
            :param **kwargs: all the four items of credentials needed from the user to 
            create an authenticated valid tweepy API object
            :type **kwargs: dict
        
        """

    def test_credentials(self):
        """ The method instantiate an API object connects to tweepy and 
        downloads the first 15 tweets with the simple search method, if unsuccessful
        tells the user that the credentials submitted may not be valid
        
        :returns QMessageBox: the message box displaying if the test was successful or not
        :rtype QMessageBox: QMessageBox
        """
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

# if __name__ == "__main__":
#    tweets_handler = TweetsHandler()
#     cred = {
#         'CONSUMER_KEY': '',
#         'CONSUMER_KEY_SECRET': '',
#         'ACCESS_TOKEN': '',
#         'ACCESS_TOKEN_SECRET': ''
#         }
#     
#     tweets_handler.test_credentials()
#    print('success')
    # js_handler = JSHandler()
    # api_obj = tweets_handler.get_api_obj()
    # stream_listener = MyStreamListener()