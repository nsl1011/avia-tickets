import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from user_form import Ui_User




# наследуемся от класса QMainWindow
class User(QtWidgets.QMainWindow):
    """docstring for User"""

    # вызываем два конструктора (для User, и для наследования класса)
    def __init__(self):
        # возвращаем объект родителя класса User и вызываем его конструктор
        super(User, self).__init__()
        # создаем экземпляр класса Ui_User
        # инициализация
        self.ui = Ui_User()
        self.ui.setupUi(self)
        # создаем массив
        self.initial_arr = []
        # вызов функций
        self.create_row()
        self.print_table()
        self.ui.exit.clicked.connect(self.open_aug)
        self.ui.tableWidget.itemDoubleClicked.connect(self.on_cell_item_clicked)


    def on_cell_item_clicked(self):
        # берем и храним строку в массиве
        global start, finish, name
        if len(self.initial_arr) == 0:

            for x in range(0,self.ui.tableWidget.columnCount(),1):
                i = self.ui.tableWidget.item(self.ui.tableWidget.currentItem().row(), x).text()
                self.initial_arr.append(i)
            print(self.initial_arr)
            start = self.initial_arr[4]
            finish = self.initial_arr[5]
            name = self.initial_arr[0]
            self.initial_arr.clear()

        # преход на другую форму
        from User_by import User_by
        self.User_by = User_by()
        self.close()
        self.User_by.show()
        return self.User_by.info(start, finish, name)


    def open_aug(self):
        # создание приложения
        from Autor import Authorization
        self.Authorization = Authorization()
        self.close()
        self.Authorization.show()

    def create_row(self):
        # подключение к БД
        db = sqlite3.connect('tickets.db')
        # создаем курсор для работы с БД
        cursor = db.cursor()
        for value in cursor.execute("SELECT * FROM `route_data`"):
            Row_count = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.setRowCount(Row_count+1)

    def print_table(self):
        # подключение к БД
        db = sqlite3.connect('tickets.db')
        # создаем курсор для работы с БД
        cursor = db.cursor()
        r_count = 0
        for value in cursor.execute("SELECT * FROM `route_data`"):

            # заполняем tableWidget
            self.ui.tableWidget.setItem(r_count, 0, QTableWidgetItem(str(value[1])))
            self.ui.tableWidget.setItem(r_count, 1, QTableWidgetItem(str(value[2])))
            self.ui.tableWidget.setItem(r_count, 2, QTableWidgetItem(str(value[3])))
            self.ui.tableWidget.setItem(r_count, 6, QTableWidgetItem(str(value[4])))
            r_count +=1
        r_count = 0
        for value in cursor.execute("SELECT * FROM `timetable`"):
            # заполняем tableWidget
            self.ui.tableWidget.setItem(r_count, 3, QTableWidgetItem(str(value[1])))
            self.ui.tableWidget.setItem(r_count, 4, QTableWidgetItem(str(value[2])))
            self.ui.tableWidget.setItem(r_count, 5, QTableWidgetItem(str(value[3])))
            r_count +=1
        # отключаемся от БД
        db.close()
        self.ui.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)


    # стоимость билетов
    def count_ticket(self, count: int):
        self.ui.lineEdit_count.setText(str(count))