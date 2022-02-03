from PySide2 import QtWidgets

# pour une fenêtre plus complexe utiliser
# class MainWindow(QtWidgets.QMainWindow):
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Liste de Courses")
        self.setup_ui()

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        pass

    def create_layouts(self):
        pass

    def modify_widgets(self):
        pass

    def add_widgets_to_layouts(self):
        pass

    def setup_connections(self):
        pass
