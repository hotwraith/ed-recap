import os
import re
import copy
import glob
import json
import datetime


class journalReader():
    global local

    def __init__(self) -> None:
        self.local = os.environ['USERPROFILE']
        pass


    def findLogs(self) -> list[str]:
        allJournals = glob.glob(os.path.join(self.local, 'Saved Games', 'Frontier Developments', 'Elite Dangerous', '*.log'))
        return allJournals
    
    def sortLogsYear(self, logs:list[str]) -> dict[int,list[str]]:
        sortedLogs = {}
        toBeSorted = logs.copy()
        for i in range(2014, int(datetime.datetime.now().year)+1):
            remainder = []
            sortedLogs.update({i:[]})
            for log in toBeSorted:
                if(len(re.findall('Journal.xxxx-[0-9]{2}-[0-9]{2}'.replace('xxxx', str(i)), log)) > 0):
                    sortedLogs[i].append(log)
                else:
                    remainder.append(log)
            toBeSorted = remainder.copy()
        return sortedLogs

    def sortLogsByCMDR(self, logs:list[str]) -> dict[str, list[str]]:
        keepPhrase = "FID"
        logsCMDR = {}
        for el in logs:
            with open(el, 'r') as f:
                f_lines = f.readlines()
                for line in f_lines:
                    ser = re.findall('"Name":"([A-z]{1,})', line)
                    if(keepPhrase in line and len(ser)>0):
                        CMDR = ser[0]
                        try:
                            logsCMDR[CMDR].append(el)
                        except KeyError:
                            logsCMDR.update({CMDR:[el]})
        return logsCMDR