from PyQt5.QtWidgets import QMessageBox


class UndefinedMessageBox(QMessageBox):
    def __init__(self, app_name="", undef_object=""):
        self.undef_object = undef_object
        self.app_name = app_name
        super().__init__(QMessageBox.Warning, self.app_name,
                        "{0} is not defined.\n" \
                        "Run a search to create a new one"
                        .format(self.undef_object),
                         QMessageBox.Ok, None)
        self.exec_()


class ExportSuccessMessageBox(QMessageBox):
    def __init__(self, app_name="", layer_name=""):
        self.app_name = app_name
        self.layer_name = layer_name
        super().__init__(QMessageBox.Information, self.app_name, 
                        "Layer {0} successfully exported".format(self.layer_name),
                        QMessageBox.Ok, None)
        self.exec_()


class ExportFailMessageBox(QMessageBox):
    def __init__(self, app_name="", layer_name="", export_error=""):
        self.app_name = app_name
        self.layer_name = layer_name
        self.export_error = export_error
        super().__init__(QMessageBox.Critical, self.app_name,
                        "Unable to save layer {0}, error{1}".format(
                        self.layer_name(), str(self.export_error)),
                        QMessageBox.Ok, None)
        self.exec_()


class StreamErrorMessageBox(QMessageBox):
    def __init__(self, app_name="", status_error=""):
        self.app_name = app_name
        self.status_error = status_error
        super().__init__(QMessageBox.Critical, self.app_name,
                        "An error occurred while streaming tweets, Status: {0}. " \
                        "The tweet stream is shut down ". format(self.status_error),
                        QMessageBox.Ok, None)
        self.exec_()
