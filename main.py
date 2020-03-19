import sys, sqlite3
from design import Ui_Form as Design
from PyQt5.QtWidgets import QWidget, QApplication, QTableWidgetItem


class Widget(QWidget, Design):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("films.db")
        self.update_result()
        cur = self.con.cursor()
        result = cur.execute("Select * from genres").fetchall()
        self.genres = {}
        for i in result:
            self.genres[i[1]] = i[0]
            self.comboBox.addItem(i[1])
        self.pushButton.clicked.connect(self.request)


    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("Select * from films").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def request(self):
        cur = self.con.cursor()
        print(self.genres[self.comboBox.currentText()])
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("""Select * from films
                                WHERE genre = ?""", (str(self.genres[self.comboBox.currentText()]))).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


app = QApplication(sys.argv)
ex = Widget()
ex.show()
sys.exit(app.exec_())