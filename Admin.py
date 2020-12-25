import sqlite3
from tkinter import messagebox

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from admin_form import Ui_Adm




# наследуемся от класса QMainWindow
class Administrator(QtWidgets.QMainWindow):
    """docstring for Administrator"""

    # вызываем два конструктора (для Administrator, и для наследования класса)
    def __init__(self):
        # возвращаем объект родителя класса Administrator и вызываем его конструктор
        super(Administrator, self).__init__()
        # создаем экземпляр класса Ui_Registration
        # инициализация
        self.ui = Ui_Adm()
        self.ui.setupUi(self)
        # вызов функций
        self.create_row()
        self.print_table()
        self.ui.pushButton_row_plu.clicked.connect(self.row_plu)
        self.ui.pushButton_row_min.clicked.connect(self.row_del)
        self.initial_arr = []
        self.update_arr = []
        self.ui.tableWidget.itemDoubleClicked.connect(self.on_cell_item_clicked)
        self.ui.exit.clicked.connect(self.open_aug)

    def open_aug(self):
        # создание приложения
        from Autor import Authorization
        self.Authorization = Authorization()
        self.close()
        self.Authorization.show()

    def test_signal(self):
        print((self.ui.tableWidget.currentItem().text()))

    def row_plu(self):
        Row_count = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.setRowCount(Row_count+1)
        self.insert()

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

    # override keyPressEvent
    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key_Enter:
            self.update()
        elif e.key() == Qt.Key_Return:
            self.update()


    def update(self):
        # получаем измененные данные с  tableWidget
        for x in range(0,self.ui.tableWidget.columnCount(),1):
            i = self.ui.tableWidget.item(self.ui.tableWidget.currentItem().row(), x).text()
            self.update_arr.append(i)
            # подключение к БД
            db = sqlite3.connect('tickets.db')
            # создаем курсор для работы с БД
            cursor = db.cursor()
            # отправляем запрос на изменение данных в БД
            cursor.execute("UPDATE `route_data` SET `name` = ?, `distance` = ?, `price` = ?, `quantity` = ? WHERE `name` = ? and `distance` = ? and `price` = ? and `quantity` = ?",
                           (self.update_arr[0], self.update_arr[1], self.update_arr[2], self.update_arr[6], self.initial_arr[0], self.initial_arr[1], self.initial_arr[2], self.initial_arr[6]))
            cursor.execute("UPDATE `timetable` SET `days_week` = ?, `start_point` = ?, `final_point` = ? WHERE `days_week` = ? and `start_point` = ? and `final_point` = ?",
                           (self.update_arr[3], self.update_arr[4], self.update_arr[5], self.initial_arr[3], self.initial_arr[4], self.initial_arr[5]))
            # сохраняем изменения в БД
            db.commit()
            # отключаемся от БД
            db.close()
        # чистим массивы
        self.initial_arr.clear()
        self.update_arr.clear()
        # обновляем tableWidget
        self.print_table()

    def clear_text(self):
        self.ui.lineEdit_name.setText(""), self.ui.lineEdit_distance.setText(""), self.ui.lineEdit_price.setText(""),
        self.ui.lineEdit_dw.setText(""), self.ui.lineEdit_sp.setText(""), self.ui.lineEdit_fp.setText(""), self.ui.lineEdit_qt.setText("")

    def insert(self):
        t_e_1 = len(self.ui.lineEdit_name.text().encode('utf-8'))
        t_e_2 = len(self.ui.lineEdit_distance.text().encode('utf-8'))
        t_e_3 = len(self.ui.lineEdit_price.text().encode('utf-8'))
        t_e_4 = len(self.ui.lineEdit_dw.text().encode('utf-8'))
        t_e_5 = len(self.ui.lineEdit_sp.text().encode('utf-8'))
        t_e_6 = len(self.ui.lineEdit_fp.text().encode('utf-8'))
        t_e_7 = len(self.ui.lineEdit_qt.text().encode('utf-8'))
        if t_e_1>0 and t_e_2>0 and t_e_3>0 and t_e_4>0 and t_e_5>0 and t_e_6>0 and t_e_7>0:
            # подключение к БД
            db = sqlite3.connect('tickets.db')
            # создаем курсор для работы с БД
            cursor = db.cursor()
            cursor.execute("INSERT INTO `route_data` (`name`, `distance`, `price`, `quantity`) VALUES (?, ?, ?, ?)", (self.ui.lineEdit_name.text(), self.ui.lineEdit_distance.text(), self.ui.lineEdit_price.text(), self.ui.lineEdit_qt.text()))
            cursor.execute("INSERT INTO `timetable` (`days_week`, `start_point`, `final_point`) VALUES (?, ?, ?)", (self.ui.lineEdit_dw.text(), self.ui.lineEdit_sp.text(), self.ui.lineEdit_fp.text()))
            # сохраняем изменения в БД
            db.commit()
            # отключаемся от БД
            db.close()
            # чистим поля ввода
            self.clear_text()
        else:
            messagebox.showerror("Ошибка", "Поля пустые!!!")
        # чистим массив
        self.initial_arr.clear()
        # обновляем tableWidget
        self.print_table()

    def on_cell_item_clicked(self):
        # берем и храним строку в массиве
        if len(self.initial_arr) == 0:
            for x in range(0,self.ui.tableWidget.columnCount(),1):
                i = self.ui.tableWidget.item(self.ui.tableWidget.currentItem().row(), x).text()
                self.initial_arr.append(i)
            print(self.initial_arr)


    def row_del(self):
        for x in range(0,self.ui.tableWidget.columnCount(),1):
                i = self.ui.tableWidget.item(self.ui.tableWidget.currentItem().row(), x).text()
                self.initial_arr.append(i)
        print(self.initial_arr)

        # подключение к БД
        db = sqlite3.connect('tickets.db')
        # создаем курсор для работы с БД
        cursor = db.cursor()

        cursor.execute("DELETE FROM `route_data` WHERE `name` = ? and `distance` = ? and `price` = ? and `quantity` = ?", (self.initial_arr[0], self.initial_arr[1], self.initial_arr[2], self.initial_arr[6]))
        cursor.execute("DELETE FROM `timetable` WHERE `days_week` = ? and `start_point` = ? and `final_point` = ?", (self.initial_arr[3], self.initial_arr[4], self.initial_arr[5]))
        # сохраняем изменения в БД
        db.commit()
        # отключаемся от БД
        db.close()
        # чистим массивы
        self.initial_arr.clear()

        Row_count = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.removeRow(Row_count-1)

        # обновляем tableWidget
        self.print_table()