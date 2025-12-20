import os
import sys
import time
import shutil

class TypePrinter():
    global speed

    def __init__(self, typeSpeed:float=0.05) -> None:
        self.speed = typeSpeed

    def slowType(self, sentence:str) -> None:
        width = shutil.get_terminal_size().columns
        col = 0
        slow = ""
        for char in sentence:
            if(col == width-1):
                print("")
                slow = ""
                col = 0
            slow += char
            print(slow, end='\r')
            time.sleep(self.speed)
            col +=1
        print("")

    def multipleSlowType(self, sentences:list[str]) -> None:
        width = shutil.get_terminal_size().columns
        for sentence in sentences:
            col = 0
            slow = ""
            for char in sentence:
                if(col == width-1):
                    print("")
                    slow = ""   
                    col = 0
                slow += char
                print(slow, end='\r')
                time.sleep(self.speed)
                col += 1
            print("")

    def hangingPoint(self, delay:float) -> None:
        blank = " "
        point = "."
        start = time.time()
        i = 0
        while time.time()-start < delay:
            if(i%2 == 0):
                print(point, end='\r')
            else:
                print(blank, end='\r')
            time.sleep(0.25)
            i+=1

    def clearConsole(self) -> None:
        os.system('cls')
    