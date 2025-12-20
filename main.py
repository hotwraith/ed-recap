import os
import glob
import json
from recap import CMDRecap
from reader import journalReader
from typeprinter import TypePrinter

def main():
    TYPE = TypePrinter(typeSpeed=0.01)
    reader = journalReader()
    allLogs = reader.findLogs()
    sortedByCMDR = reader.sortLogsByCMDR(allLogs)
    allCMDRS = list(sortedByCMDR.keys())
    running = True
    choice = -1
    while running:
        for i in range(len(allCMDRS)):
            TYPE.slowType(f"{allCMDRS[i]} ({i})")
        choice = input("::")
        try:
            choice = int(choice)
            if(0 <= choice < len(allCMDRS)):
                running = False
            else:
                pass
        except Exception:
            #TYPE.clearConsole()
            TYPE.slowType("Please select a valid option!")
    hotwraith_logs = reader.sortLogsYear(sortedByCMDR[allCMDRS[choice]])
    TYPE.clearConsole()
    hotwrcp = CMDRecap(hotwraith_logs, CMDR_name=allCMDRS[choice])



if __name__ == '__main__':
    main()