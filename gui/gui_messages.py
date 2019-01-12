from PyQt5.QtWidgets import QMessageBox


class ConfigErrorMessageBox(QMessageBox):
    def __init__(self, app_name=''):
        self.app_name = app_name
        super().__init__(QMessageBox.Critical, self.app_name,
                        'Config file not found or not accessible' \
                        ' at config/config.json',
                        QMessageBox.Ok, None)
        self.exec_()


class UndefinedMessageBox(QMessageBox):
    def __init__(self, app_name='', undef_object=''):
        self.undef_object = undef_object
        self.app_name = app_name
        super().__init__(QMessageBox.Warning, self.app_name,
                        '{0} is not defined.\n' \
                        'Run a search to create a new one'
                        .format(self.undef_object),
                         QMessageBox.Ok, None)
        self.exec_()


class ExportSuccessMessageBox(QMessageBox):
    def __init__(self, app_name='', layer_name=''):
        self.app_name = app_name
        self.layer_name = layer_name
        super().__init__(QMessageBox.Information, self.app_name, 
                        'Layer {0} successfully exported'.format(self.layer_name),
                        QMessageBox.Ok, None)
        self.exec_()


class ExportFailMessageBox(QMessageBox):
    def __init__(self, app_name='', layer_name='', export_error=''):
        self.app_name = app_name
        self.layer_name = layer_name
        self.export_error = export_error
        super().__init__(QMessageBox.Critical, self.app_name,
                        'Unable to save layer {0}, error{1}'.format(
                        self.layer_name(), str(self.export_error)),
                        QMessageBox.Ok, None)
        self.exec_()


class StreamErrorMessageBox(QMessageBox):
    def __init__(self, app_name='', status_error=''):
        self.app_name = app_name
        self.status_error = status_error
        super().__init__(QMessageBox.Critical, self.app_name,
                        'An error occurred while streaming tweets, Status: {0}. ' \
                        'The tweet stream is shut down '. format(self.status_error),
                        QMessageBox.Ok, None)
        self.exec_()


class CredentialsValidationMessageBox(QMessageBox):
    def __init__(self, app_name='', validation_type='', parent_dialog=None):
        self.app_name = app_name
        self.validation_type = validation_type
        super().__init__(QMessageBox.Question, self.app_name, '{0} don\'t seem to be valid. Proceed anyway ?'.format(validation_type),
                         QMessageBox.StandardButtons(QMessageBox.Yes | QMessageBox.No), parent_dialog)


class CredentialsTestMessagebox(QMessageBox):
    def __init__(self, message=(QMessageBox.NoIcon, '')):
        self.message = message[1]
        super().__init__(message[0], '', self.message,
                        QMessageBox.Ok, None)
        self.exec_()


class EmptyIntersectionMessageBox(QMessageBox):
    def __init__(self, app_name=''):
        self.app_name = app_name
        super().__init__(QMessageBox.Critical, self.app_name,
                        'The selected area is outside allowed extent' \
                        ' (-180, -90, 180, 90)',
                        QMessageBox.Ok, None)
        self.exec_()

