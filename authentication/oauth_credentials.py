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
    def __init__(self):
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
    def __init__(self, oauth_dlg, authorise_user):
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
        self.web_view = Browser()
        self.web_view.showMaximized()
        self.web_view.load('http://www.yomapo.com/authenticate.php')
      
    def get_response_data(self, data):
        bytes_string = data.readAll()
        print(str(bytes_string, 'utf-8'))
    
    def clear_text_fields(self):
        self.oauth_dlg.consKeyLineEdit.setText('')
        self.oauth_dlg.secretKeyLineEdit.setText('')
        self.oauth_dlg.userTokenLineEdit.setText('')
        self.oauth_dlg.secretTokenLineEdit.setText('')

# if __name__ == "__main__":
#     """these lines are only for standalone test"""
#     app = QApplication(sys.argv)
#     op = OauthCredentials()
#     op.get_base_credentials()
#     sys.exit(app.exec_())
