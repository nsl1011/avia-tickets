import sqlite3
from tkinter import messagebox
import bcrypt
from PyQt5 import QtWidgets

from registration_form import Ui_Registration

# наследуемся от класса QMainWindow
class Registration(QtWidgets.QMainWindow):
    """docstring for Registration"""

    # вызываем два конструктора (для Registration, и для наследования класса)
    def __init__(self):
        # возвращаем объект родителя класса Registration и вызываем его конструктор
        super(Registration, self).__init__()
        # создаем экземпляр класса Ui_Registration
        # инициализация
        self.ui = Ui_Registration()
        self.ui.setupUi(self)
        self.ui.registration_button_registration.clicked.connect(self.reg_function)
        self.ui.registration_button_enter.clicked.connect(self.open_aut)

    def open_aut(self):
        # создание приложения
        from Autor import Authorization
        self.Authorization = Authorization()
        self.close()
        self.Authorization.show()

    def test_select(self, login: str, cursor: sqlite3):
        # проходим по БД и проверяем, есть ли пользователь с таким именем
        for value in cursor.execute("SELECT * FROM `author` WHERE `user` = ?", (login, )):
            if login == value[1]:
                return False
        return True

    def clear_text(self):
        self.ui.registration_text_login.setText("")
        self.ui.registration_text_password.setText("")
        self.ui.registration_text_password_repeat.setText("")

    def reg_function(self):
        # получаем значения с текстовых полей
        login = self.ui.registration_text_login.toPlainText()
        password = self.ui.registration_text_password.text().encode('utf-8')
        password_repeat = self.ui.registration_text_password_repeat.text().encode('utf-8')
        if password == password_repeat:
            # подключение к БД
            db = sqlite3.connect('tickets.db')
            # начинаем работу с БД, создаем курсор
            cursor = db.cursor()


            if self.test_select(login, cursor):
                # шифруем пароль (необратимая шифровка)
                password_hesh = bcrypt.hashpw(password, bcrypt.gensalt())
                # отправляем запрос на добавление нового пользователя
                cursor.execute("INSERT INTO `author` (`user`, `password`, `lev`) VALUES(?, ?, ?)", (login, password_hesh, 1))
                # сохраняем изменения
                db.commit()
                # messagebox.showinfo("Статус", "Ваш аккаунт зарегестрирован!!!")
                print("Ваш аккаунт зарегестрирован!!!")
                # чистим поля ввода
                self.clear_text()
            else:
                # messagebox.showinfo("Статус", "Пользователь с таким именем уже существует!!!")
                print("Пользователь с таким именем уже существует!!!")
                self.clear_text()
            # завершаем работу с БД
            db.close()
        else:
            messagebox.showerror("Ошибка", "Пароль не совпадает!!!")
            self.clear_text()