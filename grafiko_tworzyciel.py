import sys
import random
import numpy as np
import calendar
from PyQt5.QtWidgets import QMainWindow,QAbstractButton, QPushButton, QApplication, QWidget, QAction,QHBoxLayout, QTableWidget, QTableWidgetItem, QVBoxLayout, QDateEdit, QLineEdit, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QDate, pyqtSignal

class App(QWidget):

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

        # Show widget
        self.show()

    def createTable(self):
        # Create table
        number_of_rows = self.slaveowners_number + self.workers_number+1
        number_of_columns = self.number_of_days+2
        date = self.date
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(number_of_rows)
        self.tableWidget.setColumnCount(number_of_columns)
        horizontal_labels = []
        vertical_labels = []
        horizontal_labels.append('Pracownik/dzień')
        vertical_labels.append('')
        sunday_dates = []
        current_day_number = 0
        for i in range (number_of_columns-2):
            horizontal_labels.append(str(i+1))
        for i in range (number_of_columns):
            vertical_labels.append(str(i+1))
        horizontal_labels.append('suma')
        self.tableWidget.setHorizontalHeaderLabels(horizontal_labels)
        self.tableWidget.setVerticalHeaderLabels(vertical_labels)
        for i in range (number_of_rows):
            self.tableWidget.setRowHeight(i,20)
        for i in range (number_of_columns):
            self.tableWidget.setColumnWidth(i,80)
        self.tableWidget.move(0, 0)

        # table selection change
        for i in range(1,self.number_of_days+1):
            date.setDate(date.year(),date.month(),i)
            self.tableWidget.setItem(0,i,QTableWidgetItem(QDate.shortDayName(date.dayOfWeek())))
            #print(QDate.longDayName(date.dayOfWeek()))
        self.tableWidget.doubleClicked.connect(self.on_click)
        self.tableWidget.resizeColumnToContents(0)
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.selectRow(0)
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            current_day_number +=1
            if currentQTableWidgetItem.text() == 'niedz.':
                sunday_dates.append(current_day_number)
        for j in range (len(sunday_dates)-1):
            for i in range (number_of_rows):
                self.tableWidget.setItem(i+1,sunday_dates[j],QTableWidgetItem("x"))

        self.tableWidget.itemChanged.connect(self.isLast)
        self.how_many_hours()
        self.give_full_hours()
        self.show()

    def number_of_wokers(self):
        self.workers_box = QLineEdit()
        self.workers_box.setMaximumWidth(200)


    def number_of_slaveowners(self):
        self.slaveowners_box = QLineEdit()
        self.slaveowners_box.setMaximumWidth(200)

    def update_table_button(self):
        self.update_button = QPushButton('update')
        self.update_button.setMaximumWidth(200)
        self.update_button.clicked.connect(self.update_rows)

    def workers_label(self):
        self.w_label = QLabel('Ile pracowników')

    def slaveowners_label(self):
        self.s_label = QLabel('ile prowadzących zmiany')

    def askfordate(self):
        self.date_box.setDate(QDate.currentDate())
        self.date_box.setMaximumSize(200,50)
        self.date_box.move(0,300)
        self.date_box.show()
        self.date_box.setCalendarPopup(True)
        self.date_box.dateChanged.connect(self.update_date)
        #self.date_box.dateChanged.connect(self.createTable)

    def how_many_hours(self):
        hours_count = 0
        working_date = self.date
        for i in range (working_date.daysInMonth()):
            working_date.setDate(working_date.year(), working_date.month(), i+1)
            if working_date.dayOfWeek()>0 and working_date.dayOfWeek()<6:
                hours_count+=8
        print(hours_count)
        self.number_of_hours = hours_count

    def give_free_days(self):
        propability_table = []
        for i in range(self.number_of_days):
            for j in range(self.slaveowners_number+self.workers_number):
                try:
                    if self.tableWidget.item(i,j).text()=='x':
                        propability_table.append(1)
                except:
                    pass
        


    def give_full_hours(self):
        for i in range(self.workers_number+self.slaveowners_number):
            hours_for_person = self.number_of_hours
            number_of_free_days = self.number_of_days-int(round(hours_for_person/11.5,0))
            assigned_free_days = 0
            j=0
            # for j in range(self.number_of_days):
            while hours_for_person > 0:
                three_of_the_same = (self.tableWidget.item(i+1,j-1)==self.tableWidget.item(i+1,j)==self.tableWidget.item(i+1,j+1))
                try:
                    if (self.tableWidget.item(i+1,j+1).text())=='x' and assigned_free_days-number_of_free_days!=0:
                        assigned_free_days+=1
                        j+=1
                    else:
                        j+=1
                except:
                    is_ramdomly_free = random.random() < (number_of_free_days-assigned_free_days)/((self.number_of_days-j)+np.power(10.0,-100))
                    if is_ramdomly_free and assigned_free_days-number_of_free_days!=0:
                        self.tableWidget.setItem(i+1,j+1,QTableWidgetItem(str('x')))
                        j+=1
                        assigned_free_days+=1
                    elif self.is_enough_today(j+1) and assigned_free_days-number_of_free_days!=0:
                        self.tableWidget.setItem(i + 1, j + 1, QTableWidgetItem(str('x')))
                        j+=1
                        assigned_free_days+=1
                    else:
                        self.tableWidget.setItem(i+1,j+1,QTableWidgetItem(str(11.5)))
                        hours_for_person-=11.5
                        j+=1
            
            hours_for_person+=11.5
            self.tableWidget.setItem(i+1,j+1,QTableWidgetItem(str(hours_for_person)))

    def is_enough_today(self,day):
        number_of_todays_workers = 0
        for i in range (self.slaveowners_number+self.workers_number):
            try:
                if self.tableWidget.item(i,day).text()=='11.5':
                    number_of_todays_workers+=1
            except:
                pass
        return number_of_todays_workers > 2

    @pyqtSlot()
    def isLast(self):
        try:
            column = self.tableWidget.currentItem().column()
            if column == self.number_of_days+1:
                pass
            else:
                self.count()
        except:
            pass
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    def update_rows(self):
        self.slaveowners_number = int(self.slaveowners_box.text())
        self.workers_number = int(self.workers_box.text())
        rows = self.slaveowners_number+self.workers_number
        difference = self.tableWidget.rowCount()-(rows+2)
        for i in range(abs(difference+1)):
            if (difference<0):
                self.tableWidget.insertRow(i+1)
            if (difference>0):
                self.tableWidget.removeRow(self.tableWidget.rowCount()-1)
        vertical_labels = []
        vertical_labels.append('')
        for i in range(rows):
            vertical_labels.append(str(i + 1))
        self.tableWidget.setVerticalHeaderLabels(vertical_labels)
        self.tableWidget.resizeRowsToContents()

    def count(self):
        suma = 0
        row = self.tableWidget.currentItem().row()
        #print(type(int(self.tableWidget.currentItem().text())))
        for i in range(self.number_of_days+1):
            try:
                 suma+=float(self.tableWidget.item(row,i).text())

            except:
                pass
        try:
            self.tableWidget.selectColumn(self.number_of_days+1)
            self.tableWidget.setItem(row,self.number_of_days+1,QTableWidgetItem(str(suma)))
        except:
            pass
        # self.tableWidget.setItem(row,self.number_of_days,QTableWidgetItem(suma))

    def update_date(self):
        current_day_number = 0
        sunday_dates = []
        days = QDate.daysInMonth(self.date_box.date())
        columns = days+1
        number_of_rows = self.workers_number+self.slaveowners_number
        self.date=self.date_box.date()
        date = self.date
        difference = self.number_of_days-(days)
        for i in range(abs(difference)):
            if (difference<0):
                print(difference)
                self.tableWidget.insertColumn(i)
            if (difference>0):
                print(difference)
                self.tableWidget.removeColumn(days-i)
        self.number_of_days = days
        self.tableWidget.clear()

        horizontal_labels = []
        horizontal_labels.append('Pracownik/dzień')
        for i in range(days):
            horizontal_labels.append(str(i + 1))
        horizontal_labels.append('suma')
        self.tableWidget.setHorizontalHeaderLabels(horizontal_labels)
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHeight(i, 20)
        for i in range(days+1):
            self.tableWidget.setColumnWidth(i, 80)
        for i in range(1, days+1):
           date.setDate(date.year(), date.month(), i)
           self.tableWidget.setItem(0, i, QTableWidgetItem(QDate.shortDayName(date.dayOfWeek())))

        self.tableWidget.selectRow(0)
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            current_day_number += 1
            if currentQTableWidgetItem.text() == 'niedz.':
                sunday_dates.append(current_day_number)
        for j in range(len(sunday_dates) - 1):
            for i in range(number_of_rows):
                self.tableWidget.setItem(i + 1, sunday_dates[j], QTableWidgetItem("x"))
        self.tableWidget.resizeColumnToContents(0)
        self.tableWidget.resizeRowsToContents()
        self.how_many_hours()
        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())