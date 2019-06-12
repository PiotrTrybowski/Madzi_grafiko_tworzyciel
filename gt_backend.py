import sys
import numpy as np
from PyQt5.QtWidgets import QApplication
import random
from gt_frontend import Table

class filler:
    def __init__(self,number_of_days,number_of_workers,_number_of_slaveowners,sunday_dates,number_of_hours):
        self.number_of_days = number_of_days
        self.number_of_workers = number_of_workers
        self.number_of_slaveowners = _number_of_slaveowners
        self.sunday_dates = sunday_dates
        self.tab_model = np.zeros((self.number_of_slaveowners+self.number_of_workers,self.number_of_days), dtype=object)
        self.numbers_of_persons_hours = []
        self.daily_workers = []
        self.repeating_workdays = []
        self.repeating_freedays = []

    def fill_sundays(self):
        for date in self.sunday_dates[:-1]:
            for i in range (len(self.tab_model)):
                self.tab_model[i][date-1]='x'


    def fill_with_elevens(self):
        number_of_rows = self.number_of_workers+self.number_of_slaveowners
        for i in range (number_of_rows):
            number_of_workdays = number_of_days
            for j in range (self.number_of_days):
                if self.tab_model[i,j] == 'x':
                    number_of_workdays -= 1
            for j in range(self.number_of_days):
                if self.tab_model[i,j] != 'x':
                    self.tab_model[i,j]=11.5

    def add_random_free_days(self):
        number_of_rows = self.number_of_workers+self.number_of_slaveowners
        for i in range(number_of_rows):
            rowsum = np.sum([elem for elem in self.tab_model[i] if type(elem)==float])
            j = 0
            while rowsum>self.number_of_hours+11.5:

                if random.randrange(100)<50 and self.tab_model[i,j]!='x':
                    self.tab_model[i,j]='x'
                    rowsum-=11.5
                j+=1
                if j>=self.number_of_days:
                    j=0

    def find_repetition(self):
        number_of_rows = self.number_of_workers + self.number_of_slaveowners

        for i in range(number_of_rows):
            for j in range(self.number_of_days-2):
                if self.tab_model[i, j] == self.tab_model[i, j+1] == self.tab_model[i, j+2] == 'x':
                    self.repeating_freedays.append((i,j+1))
                if self.tab_model[i, j] == self.tab_model[i, j+1] == self.tab_model[i, j+2] == 11.5:
                    self.tab_model[i,j+1] = 'y'
                    self.repeating_workdays.append((i,j+1))

    def naive_repetition_removal(self):
        for workday, freeday in zip(self.repeating_workdays, self.repeating_freedays):
            self.tab_model[workday] = 'x'
            self.tab_model[freeday] = 11.5

    def daily_worker_counter(self):

        for i in range(self.number_of_days):
            counter = 0
            for j in range(self.number_of_slaveowners+self.number_of_workers):
                if self.tab_model[j,i]!='x':
                    counter += 1
            self.daily_workers.append(counter)

    def count_hours(self):
        self.numbers_of_persons_hours = []
        for i in range (len(self.tab_model)):
            rowsum = np.sum([elem for elem in self.tab_model[i] if type(elem) == float])
            self.numbers_of_persons_hours.append(rowsum)

    def fill_days(self):
        for j in range(self.number_of_days):
            if self.tab_model[0, j] != 'x':
                today_working = list(range(0,self.number_of_slaveowners+self.number_of_workers))
            else:
                today_working = []
            i=0
            today_free = random.sample([0,1,2,3,4,5],3)
            today_working = [x for x in today_working if x not in today_free]
            while self.daily_workers[j]>3:
                if not( self.tab_model[today_free[i],j-2]=='x' and self.tab_model[today_free[i],j-1]=='x'):
                    self.tab_model[today_free[i],j]='x'
                    self.daily_workers[j]-=1
                    i+=1
                else:
                    buff = today_free[i]
                    today_free[i] = random.sample(today_working,1)[0]
                    today_working.remove(today_free[i])
                    today_working.append(buff)


    # def print_model(self, model):
    #     return model

app = QApplication(sys.argv)
front = Table()
number_of_days = front.number_of_days
number_of_workers = front.workers_number
number_of_slaveowners = front.slaveowners_number
sunday_dates = front.sunday_dates
number_of_hours = front.number_of_hours

back = filler(number_of_days,number_of_workers,number_of_slaveowners, sunday_dates, number_of_hours)
back.fill_sundays()
back.fill_with_elevens()
# back.add_random_free_days()
back.daily_worker_counter()
back.fill_days()
back.find_repetition()
model = back.tab_model
for rownumber,row in enumerate(model):
    for columnnumber,cell in enumerate(row):
        front.change_item(rownumber+1,columnnumber+1, cell)
front.count()
sys.exit(app.exec_())



