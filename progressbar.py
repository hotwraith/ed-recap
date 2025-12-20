import time
import random

class ProgressBar():

    def __init__(self) -> None:
        self.task = ''
        self.progress = 0

    def printPercentBar(self) -> None:
        percentage = "["
        for j in range(1, round(self.progress)+1):
            if(j%10 == 0):
                percentage += "█"
        for j in range(len(percentage), 11):
            percentage += "▒"
        percentage += f'] {round(self.progress, 1)}%'
        percentage = self.task +': ' +percentage
        print(percentage, end='\r')
    
    def updateProgress(self, update:float) -> None:
        self.progress += update
        self.printPercentBar()

    def setProgress(self, update:float) -> None:
        self.progress = update
        self.printPercentBar()

    def resetProgress(self) -> None:
        self.progress = 0
        #self.printPercentBar()

    def setTask(self, taskName:str) -> None:
        self.task = taskName
        print('')
    
    def setTaskNoReset(self, taskName:str) -> None:
        self.task = taskName

    def fakeBar(self) -> None:
        self.setTaskNoReset('Loading')
        for i in range(91):
            self.setProgress(i)
            if(i == 14):
                self.setTaskNoReset("Reading journals...")
            if(i == 29):
                self.setTaskNoReset("Discovering systems")
            if(i == 58):
                self.setTaskNoReset("Bridging to Colonia")
            if(i == 79):
                self.setTaskNoReset("Searching for Raxxla")
            time.sleep(0.05)
        for i in range(91, 101):
            self.setProgress(i)
            wait = random.randint(1, 4)
            time.sleep(wait/10)
            
