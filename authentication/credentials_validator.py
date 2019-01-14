from ..gui.gui_messages import CredentialsValidationMessageBox, CredentialsTestMessagebox
from PyQt5.QtWidgets import QMessageBox
from ..authentication.mod_tweepy import TestTweetsAuthHandler


class CredentialsValidator:
    """ business logic behind the validate functions
        of the login window
    """
    def __init__(self, app_name=''):
        """ 
            Constructor

            This class holds function that perform a "light"
            validation on the credentials inputted by the user

            :param app_name: the name of the plugin
            :type app_name: string
        """
        self.app_name = app_name
        self.parent_dialog = None
        self.credentials = None
        self.consumer_key = None
        self.consumer_key_secret = None
        self.access_token = None
        self.access_token_secret = None
    
    @staticmethod
    def test_credentials(credentials):
        """
            static method that performs the validation of externally 
            passed credentials
            :param credentials: the dictonory storing all credentials
            :type credentials: dict
        """
        test_handler = TestTweetsAuthHandler(**credentials)
        test_passed = test_handler.test_credentials()
        CredentialsTestMessagebox(test_passed)

    def set_credentials(self, credentials):
        """ 
            sets the internal credentials object to those 
            passed from the user in the login dialog
            :param credentials: the dictonory storing all credentials
            :type credentials: dict
        """
        self.credentials = credentials
        self.consumer_key = self.credentials['CONSUMER_KEY']
        self.consumer_key_secret = self.credentials['CONSUMER_KEY_SECRET']
        self.access_token = self.credentials['ACCESS_TOKEN']
        self.access_token_secret = self.credentials['ACCESS_TOKEN_SECRET']

    def set_parent_dialog(self, parent_dialog):
        """
            sets the parent dialog to the one passed in the arguments
            :param parent_dialog: the passed parent dialog
            :type parent_dialog: QDialog
        """
        self.parent_dialog = parent_dialog

    def validate_consumer_keys(self):
        """ 
            performs the "light" validation of credentials
            on the length of inputted credentials 
            :returns True or False: boolean describing if the validation succeeded
            :rtype returns: Bool
        """
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
