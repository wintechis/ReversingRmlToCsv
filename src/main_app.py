from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
import sys
import os

from convert_files import convert_files_to_csv

class FileConverterApp(QWidget):
    """
    A GUI application for converting RDF and RML files to CSV format.

    This class creates a graphical user interface that allows users to select RDF and RML files,
    convert them to CSV, and view the output. It includes features for file browsing, conversion
    status display, and error handling.
    """
   
    def __init__(self):
        """
        Initializes the GUI application window and sets up the user interface components.
        """
        super().__init__()
        self.init_ui()

   
    def init_ui(self):
        """
        Sets up the user interface layout, including all GUI elements and their configurations.
        """
        self.setWindowTitle('File to CSV Converter')
        self.setGeometry(100, 100, 600, 225)  # Sets the window's position and size

        # Define consistent widths
        label_width = 180
        input_width = 300
        button_width = 80

        #RDF File input
        file1_label = QLabel('Select RDF File (.nq):', self)
        file1_label.setFixedWidth(label_width)
        self.file1_input = QLineEdit(self)
        self.file1_input.setPlaceholderText('Select rdf file ".nq" ')
        
        self.file1_input.setFixedWidth(input_width)
        self.file1_input.setTextMargins(5, 0, 5, 0)
        self.file1_input.setAlignment(Qt.AlignLeft)
        self.file1_input.setCursorPosition(0)
        self.file1_input.setReadOnly(True)
        
        file1_browse_btn = QPushButton('Browse', self)
        file1_browse_btn.clicked.connect(self.browse_file1)

        file1_layout = QHBoxLayout()
        file1_layout.addWidget(file1_label)
        file1_layout.addWidget(self.file1_input)
        file1_layout.addWidget(file1_browse_btn)


        #Mapping file Input
        file2_label = QLabel('Select RML Mapping file (.ttl): ', self)
        file2_label.setFixedWidth(label_width)
        self.file2_input = QLineEdit(self)
        self.file2_input.setPlaceholderText('Select rml file ".ttl" ')
        self.file2_input.setFixedWidth(input_width)
        self.file2_input.setTextMargins(5, 0, 5, 0)
        self.file2_input.setAlignment(Qt.AlignLeft)
        self.file2_input.setCursorPosition(0)
        self.file2_input.setReadOnly(True)
        
        file2_browse_btn = QPushButton('Browse', self)
        file2_browse_btn.clicked.connect(self.browse_file2)

        file2_layout = QHBoxLayout()
        file2_layout.addWidget(file2_label)
        file2_layout.addWidget(self.file2_input)
        file2_layout.addWidget(file2_browse_btn)

        convert_btn = QPushButton('Convert to CSV', self)
        convert_btn.clicked.connect(self.convert_to_csv)
        convert_btn.setFixedHeight(40)

        self.status_label = QLabel('', self)
        self.status_label.setWordWrap(True)
        self.status_label.setOpenExternalLinks(True)


        main_layout = QVBoxLayout()
        main_layout.addLayout(file1_layout)
        main_layout.addLayout(file2_layout)
        main_layout.addWidget(convert_btn)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

    def browse_file1(self):
        """
        Opens a file dialog for selecting the RDF file and updates the input field with the selected file path.
        """
        self.clear_status()  # Clear previous status when selecting a new file
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*)')
        if file_name:
            self.file1_input.setText(file_name)

    def browse_file2(self):
        """
        Opens a file dialog for selecting the RML mapping file and updates the input field with the selected file path.
        """
        self.clear_status()  # Clear previous status when selecting a new file
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*)')
        if file_name:
            self.file2_input.setText(file_name)

    

    def convert_to_csv(self):
        """
        Initiates the conversion of RDF and RML files to CSV format.

        Retrieves the file paths from the input fields, validates the inputs, and performs the conversion.
        Displays status messages indicating success or failure.
        """
        file1 = self.file1_input.text()
        file2 = self.file2_input.text()
        output_file = os.path.abspath("output.csv")

        if not file1 or not file2:
            self.status_label.setText('Please select both files before converting.')
            self.status_label.setStyleSheet("color: red;") 
            return
        if not file1.endswith('.nq') or not file2.endswith('.ttl'):
            self.status_label.setText('Please check the file format. RDF file should be .nq and RML file should be .ttl.')
            self.status_label.setStyleSheet("color: red;") 

            return

        try:
            result = convert_files_to_csv(file1, file2)
            hyperlink = f'<a href="file://{output_file}">Open output.csv</a>'
            self.status_label.setText(f'{result}<br>{hyperlink}')
            self.status_label.setStyleSheet("color: green;") 

            self.clear_inputs()  # Clear the input text boxes after successful conversion


        except Exception as e:
            error_message = str(e)
            self.status_label.setStyleSheet("color: red;")
            self.status_label.setText(f'\n{error_message}')
            

    def clear_inputs(self):
        """
        Clears the input fields after a successful conversion.
        """
        self.file1_input.clear()
        self.file2_input.clear()

    def clear_status(self):
        """
        Clears the status label to remove previous messages.
        """
        self.status_label.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    converter = FileConverterApp()
    converter.show()
    sys.exit(app.exec_())