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
        toBeSorted = copy.deepcopy(logs)
        for i in range(2014, int(datetime.datetime.now().year)+1):
            remainder = []
            sortedLogs.update({i:[]})
            for log in toBeSorted:
                if(len(re.findall('Journal.xxxx-[0-9]{2}-[0-9]{2}'.replace('xxxx', str(i)), log)) > 0):
                    sortedLogs[i].append(log)
                else:
                    remainder.append(log)
            toBeSorted = copy.deepcopy(remainder)
        #print(len(sortedLogs[2023]))
        return sortedLogs

    def sortLogsByCMDR(self, logs:list[str]) -> dict[str, list[str]]:
        keepPhrase = "LoadGame"
        logsCMDR = {}
        for el in logs:
            with open(el, 'r', encoding='utf-8') as f:
                try:
                    f_lines = f.readlines()
                    for line in f_lines:
                        if(keepPhrase in line):
                            loaded_line = json.loads(line)
                            CMDR = loaded_line['Commander']
                            try:
                                logsCMDR[CMDR].append(el)
                            except KeyError:
                                logsCMDR.update({CMDR:[el]})
                            break
                except UnicodeDecodeError as e:
                    #print(el, e)
                    pass
        return logsCMDR