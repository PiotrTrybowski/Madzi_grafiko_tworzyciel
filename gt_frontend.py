import sys
import random
import numpy as np
import calendar
from PyQt5.QtWidgets import QMainWindow, QAbstractButton, QPushButton, QApplication, QWidget, QAction, QHBoxLayout, \
    QTableWidget, QTableWidgetItem, QVBoxLayout, QDateEdit, QLineEdit, QLabel
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot, QDate, pyqtSignal


class Table(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'grafiko_kreator'
        self.left = 20
        self.top = 50
        self.width = 2600
        self.height = 1000
        self.number_of_hours = 0
        self.number_of_days = QDate.daysInMonth(QDate.currentDate())
        self.workers_number = 3
        self.slaveowners_number = 3
        self.sunday_dates = []
        self.date_box = QDateEdit()
        self.date = QDate.currentDate()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()
        self.askfordate()
        self.number_of_wokers()
        self.number_of_slaveowners()
        self.update_table_button()
        self.workers_label()
        self.slaveowners_label()
        # Add box layout, add table to box layout and add box layout to widget
        self.Vlayout = QVBoxLayout()
        self.Hlayout = QHBoxLayout()

        self.Vlayout.addWidget(self.tableWidget)
        self.Vlayout.addLayout(self.Hlayout)
        self.Hlayout.addWidget(self.workers_box)
        self.Hlayout.addWidget(self.w_label)
        self.Hlayout.addWidget(self.slaveowners_box)
        self.Hlayout.addWidget(self.s_label)
        self.Hlayout.addWidget(self.update_button)
        self.Hlayout.addWidget(self.update_button)
        self.Vlayout.addWidget(self.date_box)
        self.setLayout(self.Vlayout)
        self.tableWidget.itemChanged.connect(self.isLast)
        # Show widget
        self.show()

    def createTable(self):
        # Create table
        number_of_rows = self.slaveowners_number + self.workers_number + 1
        number_of_columns = self.number_of_days + 2
        date = self.date
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(number_of_rows)
        self.tableWidget.setColumnCount(number_of_columns)
        horizontal_labels = []
        vertical_labels = []
        horizontal_labels.append('Pracownik/dzień')
        vertical_labels.append('')

        for i in range(number_of_columns - 2):
            horizontal_labels.append(str(i + 1))
        for i in range(number_of_columns):
            vertical_labels.append(str(i + 1))
        horizontal_labels.append('suma')
        self.tableWidget.setHorizontalHeaderLabels(horizontal_labels)
        self.tableWidget.setVerticalHeaderLabels(vertical_labels)
        for i in range(number_of_rows):
            self.tableWidget.setRowHeight(i, 20)
        for i in range(number_of_columns):
            self.tableWidget.setColumnWidth(i, 80)
        self.tableWidget.move(0, 0)

        # table selection change
        for i in range(1, self.number_of_days + 1):
            date.setDate(date.year(), date.month(), i)
            self.tableWidget.setItem(0, i, QTableWidgetItem(QDate.shortDayName(date.dayOfWeek())))
            # print(QDate.longDayName(date.dayOfWeek()))
        self.tableWidget.resizeColumnToContents(0)
        self.tableWidget.resizeRowsToContents()
        self.sundays()
        self.how_many_hours()
        self.count()

        self.show()

    def sundays(self):
        number_of_rows = self.slaveowners_number + self.workers_number + 1
        self.sunday_dates = []
        current_day_number = 0
        self.tableWidget.selectRow(0)
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            current_day_number += 1
            if currentQTableWidgetItem.text() == 'niedz.':
                self.sunday_dates.append(current_day_number)
        for j in range(len(self.sunday_dates) - 1):
            for i in range(number_of_rows):
                self.tableWidget.setItem(i + 1, self.sunday_dates[j], QTableWidgetItem("x"))

    def change_item(self, row,column,value):
        if value != 'y':
            self.tableWidget.setItem(row,column,QTableWidgetItem(str(value)))
        elif value == 'y':
            self.tableWidget.setItem(row,column,QTableWidgetItem(str(11.5)))
            self.tableWidget.item(row, column).setBackground(QtGui.QColor(255, 0, 0))

    def number_of_wokers(self):
        self.workers_box = QLineEdit()
        self.workers_box.setMaximumWidth(200)

    def number_of_slaveowners(self):
        self.slaveowners_box = QLineEdit()
        self.slaveowners_box.setMaximumWidth(200)

    def update_table_button(self):
        self.update_button = QPushButton('update')
        self.update_button.setMaximumWidth(200)

    def workers_label(self):
        self.w_label = QLabel('Ile pracowników')

    def slaveowners_label(self):
        self.s_label = QLabel('ile prowadzących zmiany')

    def askfordate(self):
        self.date_box.setDate(QDate.currentDate())
        self.date_box.setMaximumSize(200, 50)
        self.date_box.move(0, 300)
        self.date_box.show()
        self.date_box.setCalendarPopup(True)
        # self.date_box.dateChanged.connect(self.createTable)

    def how_many_hours(self):
        hours_count = 0
        working_date = self.date
        for i in range (working_date.daysInMonth()):
            working_date.setDate(working_date.year(), working_date.month(), i+1)
            if working_date.dayOfWeek()>0 and working_date.dayOfWeek()<6:
                hours_count+=8
        self.number_of_hours = hours_count
    @pyqtSlot()
    def isLast(self):
        try:
            self.tableWidget.currentItem().setBackground(QtGui.QColor(255,255,255))
            column = self.tableWidget.currentItem().column()
            if column == self.number_of_days+1:
                pass
            else:
                self.count()
        except:
            column = self.tableWidget.currentColumn()
            pass

    def count(self):
        for row in range(self.slaveowners_number+self.workers_number):
            suma = 0
            for column in range(self.number_of_days):
                try:
                    suma+=float(self.tableWidget.item(row+1,column+1).text())
                except:
                    pass
            self.tableWidget.selectColumn(column+2)
            self.tableWidget.setItem(row+1,column+2,QTableWidgetItem(str(suma)))





#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Table()
#     sys.exit(app.exec_())