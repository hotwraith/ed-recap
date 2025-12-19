import json
import os
import glob
import datetime

class CMDRecap():
    global CMDR_logs

    def __init__(self, CMDR_logs) -> None:
        self.CMDR_logs = CMDR_logs


    def buildRecap(self) -> dict:
        CMDR_recap = {}

        return CMDR_recap
    
    def gatherStats(self, scrappedData:dict[str, dict[str, list[str]]]) -> dict:
        statsDict = {}
        years = list(scrappedData.keys())
        for year in years:
            loglist = list(scrappedData[year].keys())
            if(len(loglist) > 0):
                statsDict.update({year: {}})

                log_begin = json.loads(scrappedData[year][loglist[0]][-1])
                log_end = json.loads(scrappedData[year][loglist[-1]][-1])
                wealth_evo =  log_end["Bank_Account"]["Current_Wealth"]-log_begin["Bank_Account"]["Current_Wealth"]
                wealth_current = log_end["Bank_Account"]["Current_Wealth"]
                l = [log_begin, log_end]
                money_spent = 0
                for i in range(2): 
                    for key in list(l[i]["Bank_Account"].keys()):
                        if("Spent_On" in key):
                            if(i%2 == 1):
                                money_spent += l[i]["Bank_Account"][key]
                            elif(i%2 == 0):
                                money_spent -= l[i]["Bank_Account"][key]
                #print(wealth_evo, money_spent)
                new_ships = log_end["Bank_Account"]["Owned_Ship_Count"]-log_begin["Bank_Account"]["Owned_Ship_Count"]
                #print(new_ships)
                CRIME = "Crime"
                fines_count = log_end[CRIME]["Fines"]-log_begin[CRIME]["Fines"]
                fines_price = log_end[CRIME]["Total_Fines"]-log_begin[CRIME]["Total_Fines"]
                bounty_count = log_end[CRIME]["Bounties_Received"]-log_begin[CRIME]["Bounties_Received"]
                #print(fines_count, fines_price, bounty_count)
                



        return statsDict

    def scrapJournals(self, keywords:list) -> dict[str, dict[str, list[str]]]:
        years = list(self.CMDR_logs.keys())
        scrapped = {}
        for el in years:
            scrapped.update({el: {}})
            self.CMDR_logs[el].sort()
            for log in self.CMDR_logs[el]:
                with open(log, 'r') as f:
                    lines = f.readlines()
                    f.close()
                for l in lines:
                    for key in keywords:
                        if(key in l):
                            try:
                                scrapped[el][log].append(l)
                            except KeyError:
                                scrapped[el].update({log: [l]})
        return scrapped