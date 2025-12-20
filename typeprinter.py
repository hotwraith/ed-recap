import os
import time

class TypePrinter():

    def __init__(self) -> None:
        pass

    def slowType(self, sentence:str) -> None:
        slow = ""
        for char in sentence:
            slow += char
            print(slow, end='\r')
            time.sleep(0.05)
        print("")

    def multipleSlowType(self, sentences:list[str]) -> None:
        for sentence in sentences:
            slow = ""
            for char in sentence:
                slow += char
                print(slow, end='\r')
                time.sleep(0.05)
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

    