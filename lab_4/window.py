import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QFileDialog)

from dehash_functions import find_card_data, luhn_algorithm, time_measurement


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        """Initializes the main application window with buttons and layouts."""
        super(MainWindow, self).__init__()
        self.setWindowIcon(QIcon('img/img.png'))
        self.setFixedSize(QSize(500, 300))
        self.setWindowTitle("Getting card number by hash")
        widget = QWidget()
        layout = QVBoxLayout()

        self.btn_bins = QLineEdit(placeholderText="Enter the list of bins")
        self.btn_hash_card = QLineEdit(placeholderText="Enter hash")
        self.btn_last_number = QLineEdit(placeholderText="Enter 4 last numbers of card")

        self.btn_number_search = QPushButton("Find card number by hash")
        self.btn_number_search.clicked.connect(self.find_number)
        self.btn_luhn = QPushButton("Check card number by Luhn Algorithm")
        self.btn_luhn.clicked.connect(self.luhn_algorithm)
        self.btn_graph = QPushButton("Draw a graphic")
        self.btn_graph.clicked.connect(self.graph_draw)
        self.btn_exit = QPushButton("Exit Program")
        self.btn_exit.clicked.connect(lambda: self.exit_program())

        self.card_number_label = QLabel()
        self.card_number_label.setText("Card number: ")
        self.card_number_label.setFixedSize(500, 15)
        self.card_number_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.card_number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.card_number = ""

        layout.addWidget(self.btn_bins)
        layout.addWidget(self.btn_hash_card)
        layout.addWidget(self.btn_last_number)
        layout.addWidget(self.btn_number_search)
        layout.addWidget(self.card_number_label)
        layout.addWidget(self.btn_luhn)
        layout.addWidget(self.btn_graph)
        layout.addWidget(self.btn_exit)

        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()

    def find_number(self) -> None:
        """
        Checks the data entered by the user and calls the function to search for the card number by hash.
        """
        file_path = QFileDialog.getSaveFileName(
            self,
            "Choose file to save card number:",
            "",
            "JSON File(*.json)",
        )[0]
        bins = self.btn_bins.text().replace(' ', '').split(",")
        hash_card = self.btn_hash_card.text()
        last_number = self.btn_last_number.text()
        if (
                (bins == [])
                or (hash_card == "")
                or (last_number == "")
        ):
            QMessageBox.warning(
                self,
                "Warning!",
                "You have not entered some fields",
            )
        else:
            result = find_card_data(
                bins,
                hash_card,
                last_number,
                file_path
            )
            if result:
                self.card_number_label.setText("Card number: " + result)
                self.card_number = result
                QMessageBox.information(None, "Successfully", f"Card number found and saved in {file_path}")
            else:
                QMessageBox.information(None, "Error", "Card number wasn't found")

    def luhn_algorithm(self) -> None:
        """
        Calls a function to verify the validity of the card number using the Luhn algorithm.
        """
        if self.card_number == "":
            QMessageBox.warning(
                None, "Before take the card number", "Card number wasn't taken"
            )
        else:
            result = luhn_algorithm(self.card_number)
            if result is not False:
                QMessageBox.information(
                    None, "Luhn Algorithm result", "Card number existing"
                )
            else:
                QMessageBox.information(
                    None, "Luhn Algorithm result", "Card number isn't existing"
                )

    def graph_draw(self) -> None:
        """
        Calls a function to plot the execution time depending on the number of processes.
        """
        bins = self.btn_bins.text().split(",")
        if (bins == "") or (self.btn_hash_card == "") or (self.btn_last_number == ""):
            QMessageBox.information(
                None,
                "Warning!",
                "You have not entered some fields",
            )
        else:
            time_measurement(bins, self.btn_hash_card.text(), self.btn_last_number.text())
            QMessageBox.information(None, "Successfully", "Graphic was drawn")

    def exit_program(self):
        """
        Closes the application window with a confirmation request from the user.
        """
        reply = QMessageBox.question(self, 'Exit program', 'Are you sure that you wanna exit the program?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.close()
        else:
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
