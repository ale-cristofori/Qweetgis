# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMessageBox


class NoTweepyMessageBox(QMessageBox):
    """autoexecuting message box when no tweepy is found"""
    
    def __init__(self):
        """Constructor"""
        super().__init__(QMessageBox.Critical, 'Geo Tweet',
                         'Could not import tweepy, '
                         'install tweepy to use the plugin',
                         QMessageBox.Ok, None)
        self.exec_()


class ConfigErrorMessageBox(QMessageBox):
    """autoexecuting message box when there is no access to config file"""

    def __init__(self, app_name=''):
        """Constructor

        :param app_name: the name of the plug-in to show on the 
        message box header
        :type app_name: str
        """
        self.app_name = app_name
        super().__init__(QMessageBox.Critical, self.app_name,
                         'Config file not found or not accessible' \
                         ' at config/config.json',
                         QMessageBox.Ok, None)
        self.exec_()


class UndefinedMessageBox(QMessageBox):
    """autoexecuting message box for undefined object (generic)"""

    def __init__(self, app_name='', undef_object=''):
        """Constructor
        
        :param app_name: the name of the plug-in to show on the 
        message box header
        :type app_name: str
        
        :param undef_object: the name of the variable found undefined
        :type undef_object: str
        
        """
        self.undef_object = undef_object
        self.app_name = app_name
        super().__init__(QMessageBox.Warning, self.app_name,
                         '{0} is not defined.\n' \
                         'Run a search to create a new one'
                         .format(self.undef_object),
                         QMessageBox.Ok, None)
        self.exec_()


class ExportSuccessMessageBox(QMessageBox):
    """autoexecuting message box when export to layer successful"""

    def __init__(self, app_name='', layer_name=''):
        """Constructor
        
        :param app_name: the name of the plug-in to show on the 
        message box header
        :type app_name: str
        
        :param layer: layer to be exported variable found undefined
        :type layer_name: str
        
        """
        self.app_name = app_name
        self.layer_name = layer_name
        super().__init__(QMessageBox.Information, self.app_name, 
                         'Layer {0} successfully exported'
                         .format(self.layer_name),
                         QMessageBox.Ok, None)
        self.exec_()


class ExportFailMessageBox(QMessageBox):
    """autoexecuting message box when export to layer successful"""

    def __init__(self, app_name='', layer_name='', export_error=''):
        """Constructor
        
        :param app_name: the name of the plug-in to show on the 
        message box header
        :type app_name: str
        
        :param layer: layer to be exported variable found undefined
        :type layer_name: str

        :param export error: the error message of the export failure
        :type export_error: str
        
        """
        self.app_name = app_name
        self.layer_name = layer_name
        self.export_error = export_error
        super().__init__(QMessageBox.Critical, self.app_name,
                         'Unable to save layer {0}, error{1}'.format(
                          self.layer_name(), str(self.export_error)),
                          QMessageBox.Ok, None)
        self.exec_()


class StreamErrorMessageBox(QMessageBox):
    """autoexecuting message box to report error in streaming shut down"""

    def __init__(self, app_name='', status_error=''):
        """Constructor
        
        :param app_name: the name of the plug-in to show on the 
        message box header
        :type app_name: str
        
        :param status_error: the code of tweepy describing the streaming staus error
        :type status_error: str

        """
        self.app_name = app_name
        self.status_error = status_error
        super().__init__(QMessageBox.Critical, self.app_name,
                         'An error occurred while streaming tweets, Status: {0}. '
                         'The tweet stream is shut down '. format(self.status_error),
                         QMessageBox.Ok, None)
        self.exec_()


class CredentialsValidationMessageBox(QMessageBox):
    """autoexecuting message box to warn the user if inputted
    credentials do not follow the usual twitter API lenght"""

    def __init__(self, app_name='', validation_type='', parent_dialog=None):
        """Constructor
        
        :param app_name: the name of the plug-in to show on the 
        message box header
        :type app_name: str
        
        :param validation_type: the type of credentials (consumer keys or oauth keys)
        which do not seem to be valid
        :type validation_type: str

        :param parent_dialog: the parent dialog of this message box
        :type parent_dialog: QDialog


        """
        self.app_name = app_name
        self.validation_type = validation_type
        super().__init__(QMessageBox.Question, self.app_name, '{0} don\'t seem to be valid. Proceed anyway ?'.format(validation_type),
                         QMessageBox.StandardButtons(QMessageBox.Yes | QMessageBox.No), parent_dialog)


class CredentialsTestMessagebox(QMessageBox):
    """ autoexecuting message box confirming succesusful test of credentials"""

    def __init__(self, message=(QMessageBox.NoIcon, '')):
        """Constructor """
        self.message = message[1]
        super().__init__(message[0], '', self.message,
                         QMessageBox.Ok, None)
        self.exec_()


class EmptyIntersectionMessageBox(QMessageBox):
    """
    autoexecuting message box telling the user the 
    selected area for geostream is outside the plug-in default area
       
    """
    
    def __init__(self, app_name=''):
        """Constructor

        :param app_name: The name of the plugin
        :type app_name: string
        """
        self.app_name = app_name
        super().__init__(QMessageBox.Critical, self.app_name,
                         'The selected area is outside allowed extent' \
                         ' (-180, -90, 180, 90)',
                         QMessageBox.Ok, None)
        self.exec_()


class EmptyTextMessageBox(QMessageBox):
    """
    autoexecuting message box telling the user the 
    search box for keyword search is empty
    """
    
    def __init__(self, app_name=''):
        """Constructor

        :param app_name: The name of the plugin
        :type app_name: string
        """
        self.app_name = app_name
        super().__init__(QMessageBox.Warning, self.app_name,
                         'The keyword search box is empty. \n Input at least one search keyword',
                         QMessageBox.Ok, None)
        self.exec_()

