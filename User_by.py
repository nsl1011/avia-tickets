import sqlite3
from tkinter import messagebox
from PyQt5 import QtCore, QtGui, QtWidgets
from user_by_form import Ui_User_by




# наследуемся от класса QMainWindow
class User_by(QtWidgets.QMainWindow):
    """docstring for User"""

    # вызываем два конструктора (для User, и для наследования класса)
    def __init__(self):
        # возвращаем объект родителя класса User и вызываем его конструктор
        super(User_by, self).__init__()
        # создаем экземпляр класса Ui_User
        # инициализация
        self.ui = Ui_User_by()
        self.ui.setupUi(self)
        self.ui.user_flight_button_buy_ticket.clicked.connect(self.updates)
        self.ui.user_flight_button_back.clicked.connect(self.open_user)
        global status
        self.status = 0



    def info(self, start: str, finish: str, airbus: str):
        self.name = airbus
        self.ui.lineEdit_start.setText(start)
        self.ui.lineEdit_finish.setText(finish)
        print(self.name[0])


    def updates(self):
        global quantity, price, count
        count = self.ui.user_flight_text_number_tickets.toPlainText()
        db = sqlite3.connect('tickets.db')
        cursor = db.cursor()
        for q in cursor.execute("SELECT `price` FROM `route_data` WHERE `name` = ?", (self.name, )):
            price = q
        for q in cursor.execute("SELECT `quantity` FROM `route_data` WHERE `name` = ?", (self.name, )):
            quantity = q
        if int(quantity[0]) >= 0:
            quantity = int(quantity[0]) - int(count)
            if quantity >= 0:
                price = int(price[0]) * int(count)
                cursor.execute("UPDATE `route_data` SET `quantity` = ? WHERE `name` = ?", (quantity, self.name))
                db.commit()
                db.close()
                self.ui.user_flight_text_number_tickets.setText("")
                self.status = 1
                self.open_user()
            else:
                messagebox.showerror("Ошибка", "Нет столько билетов!!!")
        else:
            messagebox.showerror("Ошибка", "Билетов больше нет!!!")


    def open_user(self):
        from User import User
        self.user = User()
        self.close()
        self.user.show()
        if self.status==0:
            return self.user.count_ticket(0)
        else:
            return self.user.count_ticket(int(price))