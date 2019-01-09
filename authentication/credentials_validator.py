from ..gui.gui_messages import CredentialsValidationMessageBox, CredentialsTestMessagebox
from PyQt5.QtWidgets import QMessageBox
from ..authentication.mod_tweepy import TestTweetsAuthHandler


class CredentialsValidator:
    def __init__(self, app_name=''):
        self.app_name = app_name
        self.parent_dialog = None
        self.credentials = None
        self.consumer_key = None
        self.consumer_key_secret = None
        self.access_token = None
        self.access_token_secret = None
    
    @staticmethod
    def test_credentials(credentials):
        test_handler = TestTweetsAuthHandler(**credentials)
        test_passed = test_handler.test_credentials()
        CredentialsTestMessagebox(test_passed)

    def set_credentials(self, credentials):
        self.credentials = credentials
        self.consumer_key = self.credentials['CONSUMER_KEY']
        self.consumer_key_secret = self.credentials['CONSUMER_KEY_SECRET']
        self.access_token = self.credentials['ACCESS_TOKEN']
        self.access_token_secret = self.credentials['ACCESS_TOKEN_SECRET']

    def set_parent_dialog(self, parent_dialog):
        self.parent_dialog = parent_dialog

    def validate_consumer_keys(self):
        consumer_key_valid = len(self.consumer_key) == 25       
        consumer_key_secret_valid = len(self.consumer_key_secret) == 50
        if not consumer_key_valid and not consumer_key_secret_valid:
            msg_box = CredentialsValidationMessageBox(
                self.app_name, 'Consumer Keys', self.parent_dialog
            )
            result = msg_box.exec_()
            if result == QMessageBox.No:
                return False
        return True
