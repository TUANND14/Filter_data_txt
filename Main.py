import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,QPushButton, QLineEdit, QFileDialog, QTableWidget, QLabel,QPlainTextEdit
import re
class MainWindow(QWidget):

    path_file = ""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("filter")

        # initialized
        self.input_file_path = QLineEdit()
        self.output_file_path = QLineEdit()
        self.filter_text = QPlainTextEdit()
        self.upload_input_button = QPushButton("Input")
        self.upload_output_button = QPushButton("Output")
        self.filter_button = QPushButton("Filter")
        self.table = QPlainTextEdit()
        self.status_label = QLabel("")

        # Layer
        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        output_layout = QHBoxLayout()
        filter_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        input_layout.addWidget(QLabel("File Input:"))
        input_layout.addWidget(self.input_file_path)
        input_layout.addWidget(self.upload_input_button)

        output_layout.addWidget(QLabel("File Output:"))
        output_layout.addWidget(self.output_file_path)
        output_layout.addWidget(self.upload_output_button)

        filter_layout.addWidget(QLabel("Filter:"))
        self.filter_text.setFixedSize(200,50)
        filter_layout.addWidget(self.filter_text)
        filter_layout.addWidget(self.filter_button)

        button_layout.addWidget(self.filter_button)

        layout.addLayout(input_layout)
        layout.addLayout(output_layout)
        layout.addLayout(filter_layout)
        layout.addWidget(self.table)
        layout.addWidget(self.status_label)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Excute when click on button
        self.upload_input_button.clicked.connect(self.upload_input_file)
        self.upload_output_button.clicked.connect(self.upload_output_file)
        self.filter_button.clicked.connect(self.filter_data)

    def upload_input_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "File Input", "", "Text Files (*.txt)", options=options
        )
        if file_path:
            # Display source file input
            file_name = file_path.split('/')[-1] 
            self.input_file_path.setText(file_name)
            
        self.path_file = file_path

    def upload_output_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Output", "", "Text Files (*.txt)", options=options
        )
        if file_path:
            self.output_file_path.setText(file_path)

    def getStringFilter()-> str:
        if self.filter_text != "":
            string = self.filter_text
        return string

    def updateTable(self,string)-> None:
        self.table.setPlainText(string)
        self.table.setReadOnly(True)

    def filter_data(self):
        string = self.filter_text.toPlainText()
        file_path = self.path_file
        result = ""
        text_block = ""
        string_list = string.split()
        for charecter in string_list:
            word = rf"\b{charecter.strip()}\b"
            is_in_block = False
            with open(file_path, 'r') as data:
                for line in data:
                    # if string in line:
                    if re.search(word, line):
                        is_in_block = True
                        text_block += line
                    elif is_in_block:
                        if not line.strip():
                            result+= text_block.split('\n')[1] + '\n' + '\n'
                            text_block = ""
                            is_in_block = False
                        text_block += line
                    else:
                        if not line.strip():
                            text_block = ""
                        text_block +=line
                        is_in_block = False
            if is_in_block:
                result+= text_block.split('\n')[1] + '\n' + '\n'
            
            result += "\n"
            self.updateTable(result)

        write_to_file(result)
        

def write_to_file(content):
    try:
        with open("ouput.txt", 'w') as file:  # fix output data into output.txt
            file.write(content)
        print("Write successful!")
    except Exception as e:
        print("Error occurred while writing to file:", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())