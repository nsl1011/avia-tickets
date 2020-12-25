import sys
from PyQt5 import QtWidgets
from Autor import Authorization

if __name__ == "__main__":

    # создание приложения
    app = QtWidgets.QApplication(sys.argv)

    # инициализация
    Authorization = Authorization()
    Authorization.show()


    sys.exit(app.exec_())