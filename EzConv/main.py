import os
import csv
import sys
import requests
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
    "CNY": os.path.join(script_path, "img", "CNY20.png"),
    "JPY": os.path.join(script_path, "img", "JPY20.png"),
    "KZT": os.path.join(script_path, "img", "KZT20.png"),
    "SOL": os.path.join(script_path, "img", "SOL20.png"),
    "BNB": os.path.join(script_path, "img", "BNB20.png"),
    "DOGE": os.path.join(script_path, "img", "DOGE20.png"),
    "TRX": os.path.join(script_path, "img", "TRX20.png"),
    "XRP": os.path.join(script_path, "img", "XRP20.png"),
    "TON": os.path.join(script_path, "img", "TON20.png"),
}

# TODO// проверка интернет соединения
# TODO// сделать, чтобы при смене валюты менялось значение
# TODO// сделать наконец конвертацию по актуальному курсу
# TODO//сделать обновление курса
# TODO// сделать изменение картинки в зависимости от валюты
# TODO// диалоговое окно для выхода


class Converter(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(GUI_path, self)
        self.setFixedSize(270, 344)

        icon = QIcon(icon_path)
        self.setWindowIcon(icon)

        with open(last_values_path) as file:
            values = file.read().split()
            self.currency1.setCurrentText(values[0])
            self.currency2.setCurrentText(values[1])
            self.currency3.setCurrentText(values[2])
            self.currency4.setCurrentText(values[3])
            self.currency5.setCurrentText(values[4])
            
        if self.check_internet():
            update_currency_rate()  # обновление курса
        else:
            self.internet_connection_error_msg()

        self.read_currency()

        self.reset_curr.triggered.connect(self.reset)  # сброс валют

        self.reset_values_btn.clicked.connect(self.reset_values)

        self.reset_values_menu.triggered.connect(self.reset_values)

        self.exit_btn.triggered.connect(self.execution)  # выход через menu bar

        self.refresh_rate.triggered.connect(update_currency_rate)  # обновление валют
        
        self.refresh_rate.triggered.connect(
            self.curr_error_test
        )  # проверка ошибок обновления крипты
        self.refresh_rate.triggered.connect(self.read_currency)

        self.last_changed = 6

        self.img_change()

        # self.currency1 = QComboBox
        # self.lineEdit_1 = QLineEdit

        self.currency1.activated.connect(lambda: self.img_change())
        self.currency1.activated.connect(lambda: self.local_covert(0))
        self.currency2.activated.connect(lambda: self.img_change())
        self.currency2.activated.connect(lambda: self.local_covert(1))
        self.currency3.activated.connect(lambda: self.img_change())
        self.currency3.activated.connect(lambda: self.local_covert(2))
        self.currency4.activated.connect(lambda: self.img_change())
        self.currency4.activated.connect(lambda: self.local_covert(3))
        self.currency5.activated.connect(lambda: self.img_change())
        self.currency5.activated.connect(lambda: self.local_covert(4))

        self.lineEdit_1.textChanged.connect(lambda: self.convert(0))
        self.lineEdit_2.textChanged.connect(lambda: self.convert(1))
        self.lineEdit_3.textChanged.connect(lambda: self.convert(2))
        self.lineEdit_4.textChanged.connect(lambda: self.convert(3))
        self.lineEdit_5.textChanged.connect(lambda: self.convert(4))
        
        self.lines = [
            "self.lineEdit_1",
            "self.lineEdit_2",
            "self.lineEdit_3",
            "self.lineEdit_4",
            "self.lineEdit_5",
        ]
        self.currencies = [
            "self.currency1",
            "self.currency2",
            "self.currency3",
            "self.currency4",
            "self.currency5",
        ]

    def read_currency(self):
        with open(currency_path, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";", quotechar='"')
            self.curr_rows = [[value[0], value[1], value[2]] for value in reader]

        with open(crypto_currency_path, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";", quotechar='"')
            self.crypto_rows = [[value[0], value[1], value[2]] for value in reader]

    def convert(self, line):  # конвертирование
        self.lineEdit_1.blockSignals(True)
        self.lineEdit_2.blockSignals(True)
        self.lineEdit_3.blockSignals(True)
        self.lineEdit_4.blockSignals(True)
        self.lineEdit_5.blockSignals(True)
        changing_line_text = eval(self.lines[line]).text()
        if changing_line_text == "":
            self.reset_values()
        elif (
            not changing_line_text[-1].isnumeric() and changing_line_text[-1] != "."
        ) or changing_line_text.count(".") > 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Введите корректное значение")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.setModal(True)
            msg.exec()
            self.lineEdit_1.blockSignals(False)
            self.lineEdit_2.blockSignals(False)
            self.lineEdit_3.blockSignals(False)
            self.lineEdit_4.blockSignals(False)
            self.lineEdit_5.blockSignals(False)
            eval(self.lines[line]).setText(changing_line_text[:-1])
            return ValueError
        else:
            changing_currency = eval(self.currencies[line]).currentText()
            lines = self.lines.copy()
            currencies = self.currencies.copy()
            del lines[line]
            del currencies[line]
            if changing_currency in crypto_list:
                for row in self.crypto_rows:
                    if row[0] == changing_currency:
                        changing_currency, changing_rate, changing_multiplicator = row
                        break
            else:
                for row in self.curr_rows:
                    if row[0] == changing_currency:
                        changing_currency, changing_rate, changing_multiplicator = row
                        break

            for x in range(4):
                making_line = lines[x]
                making_currency = eval(currencies[x]).currentText()
                if making_currency in crypto_list:
                    for row in self.crypto_rows:
                        if row[0] == making_currency:
                            making_currency, making_rate, making_multiplicator = row
                            break
                else:
                    for row in self.curr_rows:
                        if row[0] == making_currency:
                            making_currency, making_rate, making_multiplicator = row
                            break
                eval(making_line).setText(
                    str(
                        round(
                            float(changing_line_text)
                            * (
                                (float(changing_rate) / (float(changing_multiplicator)))
                                / (float(making_rate) / (float(making_multiplicator)))
                            ),
                            4,
                        )
                    )
                )
        self.lineEdit_1.blockSignals(False)
        self.lineEdit_2.blockSignals(False)
        self.lineEdit_3.blockSignals(False)
        self.lineEdit_4.blockSignals(False)
        self.lineEdit_5.blockSignals(False)
        self.last_changed = line
        print(self.last_changed)

    def img_change(
        self,
    ):  # обновление картинок + сохранение последних выбранных валют
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
        with open(last_values_path, mode="w") as file:
            file.write(" ".join(values))
        
    def local_covert(self, line):  # конвертирование еденичной строки
        self.lineEdit_1.blockSignals(True)
        self.lineEdit_2.blockSignals(True)
        self.lineEdit_3.blockSignals(True)
        self.lineEdit_4.blockSignals(True)
        self.lineEdit_5.blockSignals(True)
        if self.last_changed != 6 and eval(self.lines[0]).text() != "":
            if self.last_changed == line:
                self.convert(line)
            else:
                changing_line_text = eval(self.lines[self.last_changed]).text()
                changing_currency = eval(
                    self.currencies[self.last_changed]
                ).currentText()
                print(changing_line_text)
                print(changing_currency)
                if changing_currency in crypto_list:
                    for row in self.crypto_rows:
                        if row[0] == changing_currency:
                            changing_currency, changing_rate, changing_multiplicator = (
                                row
                            )
                            break
                else:
                    for row in self.curr_rows:
                        if row[0] == changing_currency:
                            changing_currency, changing_rate, changing_multiplicator = (
                                row
                            )
                            break
                making_line = self.lines[line]
                making_currency = eval(self.currencies[line]).currentText()
                if making_currency in crypto_list:
                    for row in self.crypto_rows:
                        if row[0] == making_currency:
                            making_currency, making_rate, making_multiplicator = row
                            break
                else:
                    for row in self.curr_rows:
                        if row[0] == making_currency:
                            making_currency, making_rate, making_multiplicator = row
                            break
                eval(making_line).setText(
                    str(
                        round(
                            float(changing_line_text)
                            * (
                                (float(changing_rate) / (float(changing_multiplicator)))
                                / (float(making_rate) / (float(making_multiplicator)))
                            ),
                            4,
                        )
                    )
                )
        self.lineEdit_1.blockSignals(False)
        self.lineEdit_2.blockSignals(False)
        self.lineEdit_3.blockSignals(False)
        self.lineEdit_4.blockSignals(False)
        self.lineEdit_5.blockSignals(False)

    def reset(self):  # сброс валют
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

    def check_internet(x):
        try:
            response = requests.get('https://www.google.com', timeout=5)
            return response.status_code == 200
        except requests.ConnectionError:
            return False
    
    def internet_connection_error_msg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText("Нет интернет подключения,\nбудут использоваться устаревшие данные")
        msg.setWindowTitle("Нет подключения")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setModal(True)
        msg.exec()
    
    def curr_update_msg(self):  # окно успешного обновления
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Курс обновлён до актуального")
        msg.setWindowTitle("Курс обновлён")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.setModal(True)
        msg.exec()

    def curr_error_test(self):  # проверка на наличие ошибок обновления курса
        if update_currency_rate_crypto():
            self.curr_update_error_msg()
        else:
            self.curr_update_msg()

    def curr_update_error_msg(self):  # ошибка обновления курса крипты
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Ошибка обновления курса криптовалют")
        msg.setWindowTitle("Ошибка")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def execution(self):  # выход
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
