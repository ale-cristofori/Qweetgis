# -*- coding: utf-8 -*-

from qgis.core import QgsNetworkAccessManager
from PyQt5.QtNetwork import QNetworkRequest
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtRemoveInputHook
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebKitWidgets import QWebView, QWebPage
from PyQt5.QtWebKit import QWebSettings
import sys
import pdb


class Browser(QWebView):
    """
    Subclass of pyQt webview, when the user does not log in with its
    credentials it can get theirs from the web service I set up#
    this authentication is not viable as the user will always need 
    consumer keys and those cann be shared on a desktop application
    """
    def __init__(self):
        """Constructor"""
        self.view = QWebView.__init__(self)
        self.setWindowTitle('Loading...')
        self.titleChanged.connect(self.adjustTitle)
        
    def load(self, url):
        self.setUrl(QUrl(url))
        
    def adjustTitle(self):
        self.setWindowTitle(self.title())
        
    def disableJS(self):
        settings = QWebSettings.globalSettings()
        settings.setAttribute(QWebSettings.JavascriptEnabled, False)


class OauthCredentials:
    """ This class holds together all the interaction the user can 
     have on the authentication dialog, this is to keep separated
     the interfece from the business logic
    """

    def __init__(self, oauth_dlg, authorise_user):
        """ 
        Constructor method 

        :param oauth_dlg: the dialog where the authentication 
        process takes place
        :type oauth_dlg: QDialog

        :param authorise_user: the function called from the gui
        to save into the config file the inputted credentials
        :type authorise_user: function
        
        """
        self.oauth_dlg = oauth_dlg
        self.credentials = None
        self.oauth_dlg.show()
        self.authorise_user = authorise_user
        self.oauth_dlg.getCredentialsButton.setVisible(False)
        self.oauth_dlg.getCredentialsButton.clicked.connect(self.get_base_credentials)
        self.oauth_dlg.accepted.connect(lambda: self.authorise_user({
            'CONSUMER_KEY': self.oauth_dlg.consKeyLineEdit.text().strip(),
            'CONSUMER_KEY_SECRET': self.oauth_dlg.secretKeyLineEdit.text().strip(),
            'ACCESS_TOKEN': self.oauth_dlg.userTokenLineEdit.text().strip(),
            'ACCESS_TOKEN_SECRET': self.oauth_dlg.secretTokenLineEdit.text().strip()
        }))
        self.response = None
        self.base_request = None
        self.req_manager = None
        self.web_view = None
        
    def get_base_credentials(self):
        """ connects to the authentication page to download the oauth keys"""
        self.web_view = Browser()
        self.web_view.showMaximized()
        self.web_view.load('http://www.yomapo.com/authenticate.php')
      
    def get_response_data(self, data):
        bytes_string = data.readAll()
        print(str(bytes_string, 'utf-8'))
    
    def clear_text_fields(self):
        """ 
            when the plugi closes clear up all the text fields on 
            the authorisation window
        """
        self.oauth_dlg.consKeyLineEdit.setText('')
        self.oauth_dlg.secretKeyLineEdit.setText('')
        self.oauth_dlg.userTokenLineEdit.setText('')
        self.oauth_dlg.secretTokenLineEdit.setText('')
