import os
import csv
import sys
import requests
import string
from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication,
    QMessageBox,
)
from PyQt6 import uic
from PyQt6.QtGui import QIcon, QPixmap
from rate_update import update_currency_rate
from rate_update_crypto import update_currency_rate_crypto

script_path = os.path.dirname(os.path.abspath(__file__))
currency_path = os.path.join(script_path, "bin", "currency.csv")
crypto_currency_path = os.path.join(script_path, "bin", "crypto_currency.csv")
GUI_path = os.path.join(script_path, "GUI", "EzConv_design3.ui")
last_values_path = os.path.join(script_path, "bin", "last_values.txt")
icon_path = os.path.join(script_path, "img", "Bitcoin.svg.png")

crypto_list = ("BTC", "ETH", "USDT", "SOL", "BNB", "DOGE", "TRX", "XRP", "TON")

currency_list = {
    "USD": os.path.join(script_path, "img", "USD20.png"),
    "RUB": os.path.join(script_path, "img", "RUB20.png"),
    "BTC": os.path.join(script_path, "img", "BTC20.png"),
    "ETH": os.path.join(script_path, "img", "ETH20.png"),
    "USDT": os.path.join(script_path, "img", "USDT20.png"),
    "EUR": os.path.join(script_path, "img", "EUR20.png"),
    "AED": os.path.join(script_path, "img", "AED20.png"),
    "CNY": os.path.join(script_path, "img", "CNY20_fixed.png"),
    "JPY": os.path.join(script_path, "img", "JPY20.png"),
    "KZT": os.path.join(script_path, "img", "KZT20.png"),
    "SOL": os.path.join(script_path, "img", "SOL20.png"),
    "BNB": os.path.join(script_path, "img", "BNB20.png"),
    "DOGE": os.path.join(script_path, "img", "DOGE20.png"),
    "TRX": os.path.join(script_path, "img", "TRX20.png"),
    "XRP": os.path.join(script_path, "img", "XRP20.png"),
    "TON": os.path.join(script_path, "img", "TON20.png"),
}


class Converter(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(GUI_path, self)
        self.setFixedSize(270, 343)

        icon = QIcon(icon_path)
        self.setWindowIcon(icon)

        try:
            with open(last_values_path) as file:
                values = file.read().split()
                if len(values) >= 5:
                    self.currency1.setCurrentText(values[0])
                    self.currency2.setCurrentText(values[1])
                    self.currency3.setCurrentText(values[2])
                    self.currency4.setCurrentText(values[3])
                    self.currency5.setCurrentText(values[4])
        except FileNotFoundError:
            pass

        if self.check_internet():
            if not update_currency_rate():
                self.curr_fiat_update_error_msg()
        else:
            self.internet_connection_error_msg()

        self.read_currency()

        self.reset_curr.triggered.connect(self.reset)

        self.reset_values_btn.clicked.connect(self.reset_values)

        self.reset_values_menu.triggered.connect(self.reset_values)

        self.exit_btn.triggered.connect(self.execution)

        self.refresh_rate.triggered.connect(self._refresh_fiat_rates)

        self.refresh_rate.triggered.connect(
            self.curr_error_test
        )
        self.refresh_rate.triggered.connect(self.read_currency)

        self.last_changed = None

        self.img_change()

        self.currency1.activated.connect(self.img_change)
        self.currency2.activated.connect(self.img_change)
        self.currency3.activated.connect(self.img_change)
        self.currency4.activated.connect(self.img_change)
        self.currency5.activated.connect(self.img_change)

        self.lineEdit_1.textChanged.connect(lambda: self.convert(0))
        self.lineEdit_2.textChanged.connect(lambda: self.convert(1))
        self.lineEdit_3.textChanged.connect(lambda: self.convert(2))
        self.lineEdit_4.textChanged.connect(lambda: self.convert(3))
        self.lineEdit_5.textChanged.connect(lambda: self.convert(4))

        self.line_edits = [
            self.lineEdit_1,
            self.lineEdit_2,
            self.lineEdit_3,
            self.lineEdit_4,
            self.lineEdit_5,
        ]
        self.combo_boxes = [
            self.currency1,
            self.currency2,
            self.currency3,
            self.currency4,
            self.currency5,
        ]

    def read_currency(self):
        with open(currency_path, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";", quotechar='"')
            self.curr_rows = [[value[0], value[1], value[2]] for value in reader]

        with open(crypto_currency_path, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";", quotechar='"')
            self.crypto_rows = [[value[0], value[1], value[2]] for value in reader]

    def convert(self, line):
        self._block_all_signals()
        changing_line_text = self.line_edits[line].text()

        if changing_line_text == "":
            self.reset_values()
            self.last_changed = None
        elif not self._is_valid_number(changing_line_text):
            self._show_error_dialog("Введите корректное значение")
            self.line_edits[line].setText(changing_line_text[:-1])
            self._unblock_all_signals()
            return
        else:
            changing_currency = self.combo_boxes[line].currentText()
            changing_rate, changing_multiplicator = self._get_currency_rate(
                changing_currency
            )

            other_indices = [i for i in range(5) if i != line]
            for idx in other_indices:
                making_currency = self.combo_boxes[idx].currentText()
                making_rate, making_multiplicator = self._get_currency_rate(
                    making_currency
                )
                converted_value = self._calculate_conversion(
                    float(changing_line_text),
                    changing_rate,
                    changing_multiplicator,
                    making_rate,
                    making_multiplicator,
                )
                self.line_edits[idx].setText(str(converted_value))

        self._unblock_all_signals()
        self.last_changed = line
        print(self.last_changed)

    def _block_all_signals(self):
        for le in self.line_edits:
            le.blockSignals(True)

    def _unblock_all_signals(self):
        for le in self.line_edits:
            le.blockSignals(False)

    def _is_valid_number(self, text: str) -> bool:
        if text.isalpha():
            return False
        if text[0] == ".":
            return False
        if not (text[-1].isdigit() or text[-1] == "."):
            return False
        if text.count(".") > 1:
            return False
        return True

    def _show_error_dialog(self, message: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(message)
        msg.setWindowTitle("Ошибка")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setModal(True)
        msg.exec()

    def _get_currency_rate(self, currency: str) -> tuple[float, float]:
        if currency in crypto_list:
            rows = self.crypto_rows
        else:
            rows = self.curr_rows

        for row in rows:
            if row[0] == currency:
                _, rate, multiplicator = row
                return float(rate), float(multiplicator)
        raise ValueError(f"Currency not found: {currency}")

    def _calculate_conversion(
        self,
        amount: float,
        from_rate: float,
        from_mult: float,
        to_rate: float,
        to_mult: float,
    ) -> float:
        return round(amount * ((from_rate / from_mult) / (to_rate / to_mult)), 4)

    def img_change(self):
        self.img1.setPixmap(QPixmap(currency_list[self.currency1.currentText()]))
        self.img2.setPixmap(QPixmap(currency_list[self.currency2.currentText()]))
        self.img3.setPixmap(QPixmap(currency_list[self.currency3.currentText()]))
        self.img4.setPixmap(QPixmap(currency_list[self.currency4.currentText()]))
        self.img5.setPixmap(QPixmap(currency_list[self.currency5.currentText()]))
        values = [
            self.currency1.currentText(),
            self.currency2.currentText(),
            self.currency3.currentText(),
            self.currency4.currentText(),
            self.currency5.currentText(),
        ]
        with open(last_values_path, mode="w", encoding="UTF-8") as file:
            file.write(" ".join(values))

    def reset(self):
        self.currency1.setCurrentText("BTC")
        self.currency2.setCurrentText("USDT")
        self.currency3.setCurrentText("USD")
        self.currency4.setCurrentText("EUR")
        self.currency5.setCurrentText("RUB")
        self.lineEdit_1.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")
        self.img_change()

    def reset_values(self):
        self.lineEdit_1.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")

    def check_internet(self):
        try:
            response = requests.get("https://www.google.com", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def internet_connection_error_msg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText("Нет интернет подключения,\nбудут использоваться устаревшие данные")
        msg.setWindowTitle("Нет подключения")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setModal(True)
        msg.exec()

    def curr_update_msg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Курс обновлён до актуального")
        msg.setWindowTitle("Курс обновлён")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setModal(True)
        msg.exec()

    def curr_error_test(self):
        if update_currency_rate_crypto():
            self.curr_update_msg()
        else:
            self.curr_update_error_msg()

    def curr_update_error_msg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Ошибка обновления курса криптовалют")
        msg.setWindowTitle("Ошибка")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def curr_fiat_update_error_msg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Ошибка обновления курса фиатных валют")
        msg.setWindowTitle("Ошибка")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setModal(True)
        msg.exec()

    def _refresh_fiat_rates(self):
        if not update_currency_rate():
            self.curr_fiat_update_error_msg()

    def execution(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setText("Вы уверены, что хотите выйти?")
        msg.setWindowTitle("Подтверждение выхода")
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        result = msg.exec()

        if result == QMessageBox.StandardButton.Yes:
            QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    flag = Converter()
    flag.show()
    sys.exit(app.exec())
