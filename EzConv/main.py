import PyQt6.QtCore
from PyQt6.QtWidgets import (
    QWidget,
    QMainWindow,
    QApplication,
    QLabel,
    QComboBox,
    QDialog,
    QDialogButtonBox,
)
from PyQt6 import uic
from PyQt6.QtGui import QIcon, QPixmap
from rate_update import update_currency_rate
import PyQt6
import sys

currency_list = {
    "USD": "img/USD20.png",
    "RUB": "img/RUB20.png",
    "BTC": "img/BTC20.png",
    "USDT": "img/USDT20.png",
    "EUR": "img/EUR20.png",
    "AED": "img/AED20.png",
    "CNY": "img/CNY20.png",
    "JPY": "img/JPY20.png",
    "KZT": "img/KZT20.png",
}

#TODO сделать наконец конвертацию по актуальному курсу
#TODO//сделать обновление курса
# TODO// сделать изменение картинки в зависимости от валюты
# TODO// диалоговое окно для выхода

class Converter(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("EzConv.ui", self)
        self.setFixedSize(270, 370)

        icon = QIcon("img/Bitcoin.svg.png")
        self.setWindowIcon(icon)
        
        with open("bin/last_values.txt") as file:
            values = file.read().split()
            self.currency1.setCurrentText(values[0])
            self.currency2.setCurrentText(values[1])
            self.currency3.setCurrentText(values[2])
            self.currency4.setCurrentText(values[3])
            self.currency5.setCurrentText(values[4])
            
        update_currency_rate()
            
        self.reset_curr.triggered.connect(self.reset)   #сброс валют

        self.exit_btn.triggered.connect(self.execution) # выход через menu bar
        
        self.refresh_rate.triggered.connect(update_currency_rate)

        self.pushButton.clicked.connect(
            self.convert
        )  # кнопка перевода  #! сейчас не используется


        self.action()

        # self.currency1 = QComboBox

        self.currency1.activated.connect(self.action)
        self.currency2.activated.connect(self.action)
        self.currency3.activated.connect(self.action)
        self.currency4.activated.connect(self.action)
        self.currency5.activated.connect(self.action)

    def action(self):
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
        with open("bin/last_values.txt", mode="w") as file:
            file.write(" ".join(values))
            
    def convert(self):
        pass 
    
    def reset(self):
        self.currency1.setCurrentText("BTC")
        self.currency2.setCurrentText("USDT")
        self.currency3.setCurrentText("USD")
        self.currency4.setCurrentText("EUR")
        self.currency5.setCurrentText("RUB")
        self.action()

    def execution(self):
        dialog = Exit()
        dialog.show()
        dialog.exec()



class Exit(QDialog):
    def __init__(self, parent=Converter):
        super().__init__()
        uic.loadUi("exit_dialog.ui", self)
        self.setWindowTitle("Выход")
        self.exit_accept.accepted.connect(self.ex)

    def ex(sefl):
        sys.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    flag = Converter()
    flag.show()
    sys.exit(app.exec())
