import sqlite3
import bcrypt
import sys
from PyQt5 import QtWidgets
from Reg import Registration
from enter_form import Ui_Enter

# наследуемся от класса QMainWindow
class Authorization(QtWidgets.QMainWindow):
    """docstring for Authorization"""

    # вызываем два конструктора (для Authorization, и для наследования класса)
    def __init__(self):
        # возвращаем объект родителя класса Autor и вызываем его конструктор
        super(Authorization, self).__init__()

        # создаем экземпляр класса Ui_Registration
        # инициализация
        self.ui = Ui_Enter()
        self.ui.setupUi(self)
        self.ui.enter_button_enter.clicked.connect(self.aut_function)
        self.ui.enter_button_registration.clicked.connect(self.open_reg)

    def open_reg(self):
        # создание приложения
        self.Registration = Registration()
        self.close()
        self.Registration.show()


    def test_select(self, login: str, password: str, cursor: sqlite3):
        # проходим по БД и проверяем, есть ли пользователь с таким именем
        for value in cursor.execute("SELECT * FROM `author` WHERE `user` = ?", (login, )):
            if bcrypt.hashpw(password, value[2]) == value[2]:
                return True
            break
        return False

    def aut_function(self):
        # получаем значения с текстовых полей
        global level
        login = self.ui.enter_text_login.toPlainText()
        password = self.ui.enter_text_password.text()

        # подключение к БД
        db = sqlite3.connect('tickets.db')
        # начинаем работу с БД, создаем курсор
        cursor = db.cursor()

        # расшифруем пароль (оброзно говоря)
        password = password.encode('utf-8')

        if self.test_select(login, password, cursor):
            # чистим поля ввода
            self.ui.enter_text_login.setText("")
            self.ui.enter_text_password.setText("")
            # результат авторизации
            print("Вы авторизовались!")

            for i in cursor.execute("SELECT * FROM `author` WHERE `user` = ? ", (login, )):
                level = i[3]
            if level == 1:
                # создание приложения
                from User import User
                self.User = User()
                self.close()
                self.User.show()
            elif level == 2:
                # создание приложения
                from Admin import Administrator
                self.Administrator = Administrator()
                self.close()
                self.Administrator.show()
        else:
            print("Не правильный логин или пароль!!!")
            # чистим поля ввода
            self.ui.enter_text_login.setText("")
            self.ui.enter_text_password.setText("")
        # завершаем работу с БД
        db.close()