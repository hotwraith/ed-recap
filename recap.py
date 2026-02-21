import os
import copy
import glob
import json
import time
import datetime
from typeprinter import TypePrinter
from progressbar import ProgressBar
from fluffConstants import Constants


class CMDRecap():
    global CMDR_logs
    global CMDR_name
    global rank_dict
    global CTS
    global ODY
    global ODY_end

    def __init__(self, CMDR_logs, CMDR_name=None) -> None:
        CTGet = Constants() 
        self.CTS = CTGet.getter()
        self.CMDR_logs = CMDR_logs
        self.CMDR_name = CMDR_name
        self.rank_dict = {
            "Empire": ["None", "Outsider", "Serf", "Master", "Squire", "Knight", "Lord", "Baron", "Viscount", "Count", "Earl", "Marquis", "Duke", "Prince", "King"],
            "Federation": ["None", "Recruit", "Cadet", "Midshipman", "Petty Officer", "Chief Petty Officer", "Warrant Officer", "Ensign", "Lieutenant", "Lieutenant Commander", "Post Commander", "Post Captain", "Rear Admiral", "Vice Admiral", "Admiral"],
            "Combat": ["Harmless", "Mostly Harmless", "Novice", "Competent", "Expert", "Master", "Dangerous", "Deadly", "Elite", "Elite I", "Elite II", "Elite III", "Elite IV", "Elite V"],
            "Trade": ["Penniless", "Mostly Penniless", "Peddler", "Dealer", "Merchant", "Broker", "Entrepreneur", "Tycoon", "Elite", "Elite I", "Elite II", "Elite III", "Elite IV", "Elite V"],
            "Explore": ["Aimless", "Mostly Aimless", "Scout", "Surveyor", "Trailblazer", "Pathfinder", "Ranger", "Pioneer", "Elite", "Elite I", "Elite II", "Elite III", "Elite IV", "Elite V"],
            "Soldier": ["Defenceless",  "Mostly Defenceless",  "Rookie", "Soldier", "Gunslinger", "Warrior", "Gladiator", "Deadeye", "Elite", "Elite I", "Elite II", "Elite III", "Elite IV", "Elite V"],
            "Exobiologist": ["Directionless", "Mostly Directionless", "Compiler", "Collector", "Cataloguer", "Taxonomist", "Ecologist", "Geneticist", "Elite", "Elite I", "Elite II", "Elite III", "Elite IV", "Elite V"],
            "CQC": ["Helpless", "Mostly Helpless", "Amateur", "Semi Professional", "Professional", "Champion", "Hero", "Legend", "Elite", "Elite I", "Elite II", "Elite III", "Elite IV", "Elite V"]
            }
        CMDR_recap = self.buildRecap()
        self.printRecap(CMDR_recap)


    def buildRecap(self) -> dict:
        CMDR_recap = {}
        scrap_music = self.scrapJournals(["\"event\":\"Music\""])
        scrap_stats = self.scrapJournals(["\"event\":\"Statistics\""])
        scrap_rank = self.scrapJournals(["\"event\":\"Rank\"", "\"event\":\"Progress\""])
        scrap_mission = self.scrapJournals(["\"event\":\"MissionAccepted\"", "\"event\":\"MissionFailed\"", "\"event\":\"MissionCompleted\"", "\"event\":\"MissionAbandoned\""])
        scrap_jumps = self.scrapJournals(["\"event\":\"StartJump\", \"JumpType\":\"Hyperspace\""])
        #scrap_jumps = self.scrapJournals(["\"event\":\"FSDJump\""])
        #scrap_mission = self.scrapJournals(["\"event\":\"MissionAccepted\""])
        res_music = self.gatherMusic(scrap_music)
        res_stats = self.gatherStats(scrap_stats)
        res_rank = self.gatherRanks(scrap_rank)
        res_mission = self.gatherMissions(scrap_mission)
        res_jumps = self.gatherJumps(scrap_jumps)
        for year in list(self.CMDR_logs.keys()):
            if(year in list(res_music.keys()) or year in list(res_stats.keys()) or year in list(res_rank.keys())):
                CMDR_recap.update({year:{}})
                if(year in list(res_stats.keys())):
                    CMDR_recap[year].update(res_stats[year])
                if(year in list(res_music.keys())):
                    CMDR_recap[year].update(res_music[year])
                if(year in list(res_rank.keys())):
                    CMDR_recap[year].update(res_rank[year])
                if(year in list(res_mission.keys())):
                    CMDR_recap[year].update(res_mission[year])
                if(year in list(res_jumps.keys())):
                    CMDR_recap[year].update(res_jumps[year])

        #print(json.dumps(CMDR_recap, indent=4))
        return CMDR_recap

    def gatherStats(self, scrappedData:dict[str, dict[str, list[str]]]) -> dict[str,dict[str,dict[str,float]]]:
        statsDict = {}
        years = list(scrappedData.keys())
        for year in years:
            loglist = list(scrappedData[year].keys())
            if(len(loglist) > 0):
                statsDict.update({year: {"STATS":{}}})
                
                log_begin = json.loads(scrappedData[year][loglist[0]][-1])
                try:
                    log_end = json.loads(scrappedData[str(int(year)+1)][loglist[0]][-1])
                except KeyError:
                    log_end = json.loads(scrappedData[year][loglist[-1]][-1])

                BANK = 'Bank_Account'
                wealth_evo =  log_end[BANK]["Current_Wealth"]-log_begin[BANK]["Current_Wealth"]
                wealth_current = log_end[BANK]["Current_Wealth"]
                l = [log_begin, log_end]
                money_spent = 0
                for i in range(2): 
                    for key in list(l[i][BANK].keys()):
                        if("Spent_On" in key):
                            if(i%2 == 1):
                                money_spent += l[i][BANK][key]
                            elif(i%2 == 0):
                                money_spent -= l[i][BANK][key]
                #print(wealth_evo, money_spent)
                new_ships = log_end[BANK]["Owned_Ship_Count"]-log_begin[BANK]["Owned_Ship_Count"]
                statsDict[year]["STATS"].update({BANK: 
                                        {
                                        'MONEY_CHANGE':float(wealth_evo),
                                        'MONEY_NOW':float(wealth_current),
                                        'MONEY_SPENT':float(money_spent),
                                        'SHIPS_NEW':float(new_ships)
                                        }
                                        })
                #print(new_ships)
                CRIME = "Crime"
                fines_count = log_end[CRIME]["Fines"]-log_begin[CRIME]["Fines"]
                fines_price = log_end[CRIME]["Total_Fines"]-log_begin[CRIME]["Total_Fines"]
                bounty_count = log_end[CRIME]["Bounties_Received"]-log_begin[CRIME]["Bounties_Received"]
                #print(fines_count, fines_price, bounty_count)
                statsDict[year]["STATS"].update({CRIME: 
                                        {
                                        'FINE_COUNT':float(fines_count),
                                        'FINE_PRICE':float(fines_price),
                                        'BOUNTY_COUNT':float(bounty_count)
                                        }
                                        })                

                TRADE = 'Trading'
                market_profit = log_end[TRADE]["Market_Profits"]-log_begin[TRADE]["Market_Profits"]
                resources_traded = log_end[TRADE]["Resources_Traded"]-log_begin[TRADE]["Resources_Traded"]
                #resources_traded = log_end[TRADE]["Resources_Traded"]-log_begin[TRADE]["Resources_Traded"]

                statsDict[year]["STATS"].update({TRADE: 
                                        {
                                        'MARKET_PROFIT':float(market_profit),
                                        'RESOURCES_TRADED':float(resources_traded)
                                        }
                                        })    

                EXPLO = 'Exploration'
                new_visited_systems = log_end[EXPLO]["Systems_Visited"]-log_begin[EXPLO]["Systems_Visited"]
                explo_profit = log_end[EXPLO]["Exploration_Profits"]-log_begin[EXPLO]["Exploration_Profits"]
                total_distance = log_end[EXPLO]["Total_Hyperspace_Distance"]-log_begin[EXPLO]["Total_Hyperspace_Distance"]
                total_jumps = log_end[EXPLO]["Total_Hyperspace_Jumps"]-log_begin[EXPLO]["Total_Hyperspace_Jumps"]
                time_played = log_end[EXPLO]["Time_Played"]-log_begin[EXPLO]["Time_Played"]
                try:
                    get = log_begin[EXPLO]["OnFoot_Distance_Travelled"]
                    begin = True
                except KeyError:
                    begin = False
                try:
                    get = log_end[EXPLO]["OnFoot_Distance_Travelled"]
                    end = True
                except KeyError:
                    end = False
                if(begin and end):
                    onfoot_distance = log_end[EXPLO]["OnFoot_Distance_Travelled"]-log_begin[EXPLO]["OnFoot_Distance_Travelled"]
                    first_footfalls = log_end[EXPLO]["First_Footfalls"]-log_begin[EXPLO]["First_Footfalls"]
                    self.ODY =  True
                elif(end):
                    onfoot_distance = log_end[EXPLO]["OnFoot_Distance_Travelled"]
                    first_footfalls = log_end[EXPLO]["First_Footfalls"]
                    self.ODY =  True
                else:
                    self.ODY = False
                    onfoot_distance = 0
                    first_footfalls = 0         

                #print(total_distance, total_jumps, float(time_played)/3600, first_footfalls)

                statsDict[year]["STATS"].update({EXPLO: 
                                        {
                                        'SYSTEMS_NEW':float(new_visited_systems),
                                        'SYSTEMS_PROFIT':float(explo_profit),
                                        'TOTAL_DISTANCE':float(total_distance),
                                        'TOTAL_JUMPS':float(total_jumps),
                                        'TOTAL_TIME':float(time_played),
                                        'TOTAL_DISTANCE_FOOT':float(onfoot_distance),
                                        'TOTAL_FF':float(first_footfalls)
                                        }
                                        })    
                
                THARGOID = 'TG_ENCOUNTERS'
                try:
                    get = log_begin[THARGOID]["TG_ENCOUNTER_TOTAL"]   
                    begin = True
                except KeyError:
                    begin = False
                try:
                    get = log_end[THARGOID]["TG_ENCOUNTER_TOTAL"]
                    end = True
                except KeyError:
                    end = False
                if(begin and end):
                    tg_encounters = log_end[THARGOID]["TG_ENCOUNTER_TOTAL"]-log_begin[THARGOID]["TG_ENCOUNTER_TOTAL"]                
                #print(tg_encounters)
                elif(end):
                    tg_encounters = log_end[THARGOID]["TG_ENCOUNTER_TOTAL"]                
                else:
                    tg_encounters = 0

                statsDict[year]["STATS"].update({'Thargoid': 
                                        {
                                        'TG_ENCOUNTERS':float(tg_encounters)
                                        }
                                        })   

                ENGI = 'Crafting'
                engi_rolls = log_end[ENGI]["Recipes_Generated"]-log_begin[ENGI]["Recipes_Generated"]         
                new_engi = log_end[ENGI]["Count_Of_Used_Engineers"]-log_begin[ENGI]["Count_Of_Used_Engineers"]         
                #print(new_engi)

                statsDict[year]["STATS"].update({ENGI: 
                                        {
                                        'ENGI_ROLLS':float(engi_rolls),
                                        'ENGI_NEW':float(new_engi)
                                        }
                                        })

                CREW = 'Crew'
                crew_wages = log_end[CREW]["NpcCrew_TotalWages"]-log_begin[CREW]["NpcCrew_TotalWages"]
                crew_hired = log_end[CREW]["NpcCrew_Hired"]-log_begin[CREW]["NpcCrew_Hired"]
                crew_fired = log_end[CREW]["NpcCrew_Fired"]-log_begin[CREW]["NpcCrew_Fired"]
                crew_kia = log_end[CREW]["NpcCrew_Died"]-log_begin[CREW]["NpcCrew_Died"]
                #print(crew_wages, crew_hired, crew_fired, crew_kia)

                statsDict[year]["STATS"].update({CREW: 
                                        {
                                        'CREW_WAGES':float(crew_wages),
                                        'CREW_HIRED':float(crew_hired),
                                        'CREW_FIRED':float(crew_fired),
                                        'CREW_KIA':float(crew_kia)
                                        }
                                        })


                MATS = 'Material_Trader_Stats'
                mat_trades = log_end[MATS]["Trades_Completed"]-log_begin[MATS]["Trades_Completed"]
                mat_count = log_end[MATS]["Materials_Traded"]-log_begin[MATS]["Materials_Traded"]
                #print(mat_trades, mat_count)

                statsDict[year]["STATS"].update({'Materials': 
                                        {
                                        'MAT_TRADES':float(mat_trades),
                                        'MAT_COUNT':float(mat_count)
                                        }
                                        })

                CQC = 'CQC' #lol

                try:
                    get = log_begin[CQC]["CQC_Time_Played"]
                    begin = True
                except KeyError:
                    begin = False
                try:
                    get = log_end[CQC]["CQC_Time_Played"]
                    end = True
                except KeyError:
                    end = False
                if(begin and end):
                    CQC_time = log_end[CQC]["CQC_Time_Played"]-log_begin[CQC]["CQC_Time_Played"]
                elif(end):
                    CQC_time = log_end[CQC]["CQC_Time_Played"]
                else:
                    CQC_time = 0

                statsDict[year]["STATS"].update({CQC: 
                                        {
                                        'TIME_PLAYED':float(CQC_time)
                                        }
                                        })

                FC = 'FLEETCARRIER'
                try:
                    get = log_begin[FC]["FLEETCARRIER_EXPORT_TOTAL"]
                    begin = True
                except KeyError:
                    begin = False
                try:
                    get = log_end[FC]["FLEETCARRIER_EXPORT_TOTAL"]
                    end = True
                except KeyError:
                    end = False
                if(end and begin):
                    exported_commodities = log_end[FC]["FLEETCARRIER_EXPORT_TOTAL"]-log_begin[FC]["FLEETCARRIER_EXPORT_TOTAL"]
                    imported_commodities = log_end[FC]["FLEETCARRIER_IMPORT_TOTAL"]-log_begin[FC]["FLEETCARRIER_IMPORT_TOTAL"]
                    fc_distance = log_end[FC]["FLEETCARRIER_DISTANCE_TRAVELLED"]-log_begin[FC]["FLEETCARRIER_DISTANCE_TRAVELLED"]
                    fc_jumps = log_end[FC]["FLEETCARRIER_TOTAL_JUMPS"]-log_begin[FC]["FLEETCARRIER_TOTAL_JUMPS"]
                    #print(exported_commodities, imported_commodities)
                    #print(fc_distance, fc_jumps)
                    fc_rearm = log_end[FC]["FLEETCARRIER_REARM_TOTAL"]-log_begin[FC]["FLEETCARRIER_REARM_TOTAL"]
                    fc_refuel = log_end[FC]["FLEETCARRIER_REFUEL_TOTAL"]-log_begin[FC]["FLEETCARRIER_REFUEL_TOTAL"]
                    fc_repair = log_end[FC]["FLEETCARRIER_REPAIRS_TOTAL"]-log_begin[FC]["FLEETCARRIER_REPAIRS_TOTAL"]
                    #print(fc_rearm, fc_refuel, fc_repair)
                elif(end):
                    exported_commodities = log_end[FC]["FLEETCARRIER_EXPORT_TOTAL"]
                    imported_commodities = log_end[FC]["FLEETCARRIER_IMPORT_TOTAL"]
                    fc_distance = log_end[FC]["FLEETCARRIER_DISTANCE_TRAVELLED"]
                    fc_jumps = log_end[FC]["FLEETCARRIER_TOTAL_JUMPS"]
                    #print(exported_commodities, imported_commodities)
                    #print(fc_distance, fc_jumps)
                    fc_rearm = log_end[FC]["FLEETCARRIER_REARM_TOTAL"]
                    fc_refuel = log_end[FC]["FLEETCARRIER_REFUEL_TOTAL"]
                    fc_repair = log_end[FC]["FLEETCARRIER_REPAIRS_TOTAL"]
                else:
                    exported_commodities = 0
                    imported_commodities = 0
                    fc_distance = 0
                    fc_jumps = 0
                    fc_rearm = 0
                    fc_refuel = 0
                    fc_repair = 0

                statsDict[year]["STATS"].update({'FleetCarrier': 
                                        {
                                        'EXPORTED_COM':float(exported_commodities),
                                        'IMPORTED_COM':float(imported_commodities),
                                        'TOTAL_DISTANCE':float(fc_distance),
                                        'TOTAL_JUMPS':float(fc_jumps),
                                        'TOTAL_REARM':float(fc_rearm),
                                        'TOTAL_REFUEL':float(fc_refuel),
                                        'TOTAL_REPAIR':float(fc_repair)
                                        }
                                        })
                
                EXOBIO = 'Exobiology'
                try:
                    get = log_begin[EXOBIO]["Organic_Data_Profits"]
                    begin = True
                except KeyError:
                    begin = False
                try:
                    get = log_end[EXOBIO]["Organic_Data_Profits"]
                    end = True
                except KeyError:
                    end = False
                if(begin and end):
                    exobio_profit = log_end[EXOBIO]["Organic_Data_Profits"]-log_begin[EXOBIO]["Organic_Data_Profits"]
                    ff_profit = log_end[EXOBIO]["First_Logged_Profits"]-log_begin[EXOBIO]["First_Logged_Profits"]
                    ff_count = log_end[EXOBIO]["First_Logged"]-log_begin[EXOBIO]["First_Logged"]
                elif(end):
                    exobio_profit = log_end[EXOBIO]["Organic_Data_Profits"]
                    ff_profit = log_end[EXOBIO]["First_Logged_Profits"]
                    ff_count = log_end[EXOBIO]["First_Logged"]
                else:
                    exobio_profit = 0
                    ff_profit = 0
                    ff_count = 0

                statsDict[year]["STATS"].update({EXOBIO: 
                                        {
                                        'TOTAL_PROFIT':float(exobio_profit),
                                        'TOTAL_FF_PROFIT':float(ff_profit),
                                        'TOTAL_FF':float(ff_count)
                                        }
                                        })
        #print(json.dumps(statsDict, indent=4))
        return statsDict
    
    def gatherMusic(self, scrappedData:dict[str, dict[str, list[str]]]) -> dict:
        statsDict = {}
        years = list(scrappedData.keys())
        for year in years:
            loglist = list(scrappedData[year].keys())
            if(len(loglist) > 0):
                statsDict.update({year: {"MUSIC": {}}})
                for logs in loglist:
                    for music in scrappedData[year][logs]:
                        loaded_music = json.loads(music)['MusicTrack']
                        if (loaded_music != 'NoTrack' and loaded_music != 'NoInGameMusic'):
                            try:
                                statsDict[year]["MUSIC"][loaded_music] += 1
                            except KeyError:
                                statsDict[year]["MUSIC"].update({loaded_music:1})
        
        return statsDict
                 
    def gatherRanks(self, scrappedData:dict[str, dict[str, list[str]]]) -> dict:
        statsDict = {}
        years = list(scrappedData.keys())
        for year in years:
            loglist = list(scrappedData[year].keys())
            if(len(loglist) > 0):
                statsDict.update({year: {}})
                
                log_begin = scrappedData[year][loglist[0]]
                log_end = scrappedData[year][loglist[-1]]

                rank_begin = json.loads(log_begin[0])
                progress_begin = json.loads(log_begin[1])
                rank_end = json.loads(log_end[0])
                progress_end = json.loads(log_end[1])

                Empire = [rank_end['Empire']-rank_begin['Empire'], rank_end["Empire"], progress_end["Empire"]]
                Federation = [rank_end['Federation']-rank_begin['Federation'], rank_end["Federation"], progress_end["Federation"]]
                Combat = [rank_end['Combat']-rank_begin['Combat'], rank_end["Combat"], progress_end["Combat"]]
                Trade = [rank_end['Trade']-rank_begin['Trade'], rank_end["Trade"], progress_end["Trade"]]
                Explore = [rank_end['Explore']-rank_begin['Explore'], rank_end["Explore"], progress_end["Explore"]]
                #if(self.ODY):
                Soldier = [rank_end['Soldier']-rank_begin['Soldier'], rank_end["Soldier"], progress_end["Soldier"]]
                Exobiologist = [rank_end['Exobiologist']-rank_begin['Exobiologist'], rank_end["Exobiologist"], progress_end["Exobiologist"]]
                #else:
                    #Soldier = [0,0,0]
                    #Exobiologist = [0,0,0]
                CQC = [rank_end['CQC']-rank_begin['CQC'], rank_end["CQC"], progress_end["CQC"]]

                statsDict[year].update({"RANKS":
                                    {
                                    "Empire":Empire,
                                    "Federation":Federation,
                                    "Combat":Combat,
                                    "Trade":Trade,
                                    "Explore":Explore,
                                    "Soldier":Soldier,
                                    "Exobiologist":Exobiologist,
                                    "CQC":CQC
                                    }
                                       })
        return statsDict

        '''
        MissionAccepted     Mission_Mining_name (WMM) Mission_MassacreWing (massacre)
        MissionCompleted
        MissionAbandoned
        MissionFailed
        '''
    def gatherMissions(self, scrappedData:dict[str, dict[str, list[str]]]) -> dict:
        statsDict = {}
        years = list(scrappedData.keys())
        for year in years:
            loglist = list(scrappedData[year].keys())
            if(len(loglist) > 0):
                statsDict.update({year: {"MISSIONS":{"MissionAccepted":0, "MissionCompleted":0, "MissionAbandoned":0, "MissionFailed":0, "Mission_Mining_name":0, "Mission_MassacreWing":0}}})
                for logs in loglist:
                    for mission in scrappedData[year][logs]:
                        loaded_mission = json.loads(mission)['event']
                        type_mission = json.loads(mission)['Name']
                        try:
                            statsDict[year]["MISSIONS"][loaded_mission] += 1
                            if(type_mission == 'Mission_Mining_name' or type_mission == 'Mission_MassacreWing'):
                                try:
                                    statsDict[year]["MISSIONS"][type_mission] += 1
                                except KeyError:
                                    statsDict[year]["MISSIONS"].update({type_mission:1})
                        except KeyError:
                            statsDict[year]["MISSIONS"].update({loaded_mission:1})
        return statsDict
    
    def gatherJumps(self, scrappedData:dict[str, dict[str, list[str]]]) -> dict:
        statsDict = {}
        years = list(scrappedData.keys())
        for year in years:
            loglist = list(scrappedData[year].keys())
            if(len(loglist) > 0):
                statsDict.update({year: {"JUMPS":{}}})
                for logs in loglist:
                    for mission in scrappedData[year][logs]:
                        loaded_mission = json.loads(mission)['StarSystem']
                        #type_mission = json.loads(mission)['Name']
                        try:
                            statsDict[year]["JUMPS"][loaded_mission] += 1
                        except KeyError:
                            statsDict[year]["JUMPS"].update({loaded_mission:1})
        return statsDict


    def scrapJournals(self, keywords:list) -> dict[str, dict[str, list[str]]]:
        years = list(self.CMDR_logs.keys())
        scrapped = {}
        copied_logs = copy.deepcopy(self.CMDR_logs)
        for el in years:
            scrapped.update({el: {}})
            #print(el, len(copied_logs[el]))
            copied_logs[el].sort()
            for log in copied_logs[el]:
                with open(log, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    f.close()
                for i in range(len(lines)):
                    for key in keywords:
                        if(key in lines[i]):
                            try:
                                scrapped[el][log].append(lines[i])
                            except KeyError:
                                scrapped[el].update({log: [lines[i]]})
        return scrapped

    def numberStrBuilder(self, number:float, rounding:int=None) -> str: # type: ignore
        number = round(abs(number), ndigits=rounding)
        newNum = format(number, ',')
        newNum = newNum.replace(',', '\'')
        return newNum

    def printRecap(self, CMDR_recap) -> None:
        TYPE = TypePrinter(typeSpeed=0.025)
        allFluff = []
        phrase = "Welcome to your Elite: Dangerous yearly recap"
        if(self.CMDR_name != None):
            phrase += " for " + self.CMDR_name
        phrase += " !"
        allFluff.append(phrase)
        allFluff.append("Please select a year to view its recap:")
        TYPE.multipleSlowType(allFluff)
        years = list(CMDR_recap.keys())
        pickedYear = years[-1]
        running = True
        choice = ''
        while running:
            for i in range(len(years)):
                TYPE.slowType(f"{years[i]} ({i})")
            choice = input("::")
            try:
                choice = int(choice)
                if(0 <= choice < len(years)):
                    running = False
                else:
                    pass
            except Exception:
                #TYPE.clearConsole()
                TYPE.slowType("Please select a valid option!")
        if(type(choice) is int):
            pickedYear = years[choice]
        self.printYear(CMDR_recap[pickedYear], pickedYear)

    def sortMusic(self, CMDRC_music:dict[str, int]) -> list[tuple[str, int]]:
        sorted_music = []
        for key in list(CMDRC_music.keys()):
            sorted_music.append((CMDRC_music[key], key))
        sorted_music.sort(reverse=True)
        return sorted_music

    def printYear(self, CMDRC, year) -> None:
        musics = self.sortMusic(CMDRC["MUSIC"])
        if("JUMPS" in list(CMDRC.keys())):
            jumps = self.sortMusic(CMDRC["JUMPS"])
        PROGRESS = ProgressBar()
        TYPE = TypePrinter(typeSpeed=0.025)
        types = [
            f"This year of {year+1286} was a big year !",
            "You did a lot of things, let's review all of that shall we ?",
                ]
        TYPE.multipleSlowType(types)
        TYPE.hangingPoint(3)
        PROGRESS.fakeBar()
        print("")
        TYPE.clearConsole()
        words = []
        if(CMDRC["STATS"]["Bank_Account"]["MONEY_CHANGE"] > 0):
            words.append("gained")
        else:
            words.append("lost")
        if(CMDRC["STATS"]["Bank_Account"]["SHIPS_NEW"] > 0):
            words.append("acquired")
            words.append("what did you use them for ?")
        elif(CMDRC["STATS"]["Bank_Account"]["SHIPS_NEW"] == 0):
            words.append("have bought a grand total of")
            words.append("short on money CMDR ?")
        else:
            words.append("sold")
            words.append("were they collecting dust in a hangar ?")
        if(CMDRC["STATS"]["Crime"]["BOUNTY_COUNT"] +CMDRC["STATS"]["Crime"]["FINE_COUNT"] >= 10):
            words.append(" you criminal scum !")
        else:
            words.append(", what a lawful space citizen...")
        if(CMDRC["STATS"]["CQC"]["TIME_PLAYED"] > 0):
            words.append(", how did you manage to find a match ?")
        else:
            words.append(", like everyone else.")
        types = [
            f"This year you {words[0]} {self.numberStrBuilder(CMDRC["STATS"]["Bank_Account"]["MONEY_CHANGE"])} CR, that's about {self.numberStrBuilder(round(CMDRC["STATS"]["Bank_Account"]["MONEY_CHANGE"]*50/self.CTS["PIB"][0]*100, 2))}% of {self.CTS["PIB"][1]}'s nominal PIB",
            f"Across outfitting, ships, repairs and rebuys you've spent around {self.numberStrBuilder(CMDRC["STATS"]["Bank_Account"]["MONEY_SPENT"])} CR this year",
            f"You've {words[1]} {self.numberStrBuilder(CMDRC["STATS"]["Bank_Account"]["SHIPS_NEW"])} ships, {words[2]}",
            " ",
            f"You've been the target of {self.numberStrBuilder(CMDRC["STATS"]["Crime"]["FINE_COUNT"])} fines, {self.numberStrBuilder(CMDRC["STATS"]["Crime"]["BOUNTY_COUNT"])} bounties{words[3]}",
            " "
        ]
        if(CMDRC["STATS"]["Trading"]["RESOURCES_TRADED"] >0 ):
            types.extend([
                f"Across the year you've traded {self.numberStrBuilder(CMDRC["STATS"]["Trading"]["RESOURCES_TRADED"])} tons of commodities, totalizing a whooping {self.numberStrBuilder(CMDRC["STATS"]["Trading"]["MARKET_PROFIT"])} CR ! That's {self.numberStrBuilder(CMDRC["STATS"]["Trading"]["MARKET_PROFIT"]/CMDRC["STATS"]["Trading"]["RESOURCES_TRADED"])} CR/t on average.",
                " "
            ])

        types.extend([
            "Exploration is a key part of this universe, and you've done your part:",
            f"- By visiting {self.numberStrBuilder(CMDRC["STATS"]["Exploration"]["SYSTEMS_NEW"])} new systems"
        ])
        if(CMDRC["STATS"]["Exploration"]["SYSTEMS_PROFIT"] > 0):
            types.append(f"- Or selling {self.numberStrBuilder(CMDRC["STATS"]["Exploration"]["SYSTEMS_PROFIT"])} CR worth of cartographic data to Universal Cartographics !")
        
        types.append(f"- You've traveled {self.numberStrBuilder(CMDRC["STATS"]["Exploration"]["TOTAL_DISTANCE"])} lys across {self.numberStrBuilder(CMDRC["STATS"]["Exploration"]["TOTAL_JUMPS"])} jumps, that's {self.numberStrBuilder(CMDRC["STATS"]["Exploration"]["TOTAL_DISTANCE"]/CMDRC["STATS"]["Exploration"]["TOTAL_JUMPS"], 1)} lys/jump on average :eyes:")
        if(CMDRC["STATS"]["Exploration"]["TOTAL_DISTANCE_FOOT"] >0):
            types.append(f"- Finally you've ran, climbed or walked {self.numberStrBuilder(CMDRC["STATS"]["Exploration"]["TOTAL_DISTANCE_FOOT"])}m, that's {self.numberStrBuilder(CMDRC["STATS"]["Exploration"]["TOTAL_DISTANCE_FOOT"]/42000, 2)} marathon(s).")
        
        types.extend([
            " ",
            f"We might have won the war but they still hang around, sharing this galaxy with us, this year you've met {self.numberStrBuilder(CMDRC["STATS"]["Thargoid"]["TG_ENCOUNTERS"])} 'Goids !",
        ])

        if(CMDRC["STATS"]["Crafting"]["ENGI_ROLLS"]):
            types.extend([
            " ",
            f"A good ship is one that you made yours, and this year you've clicked {self.numberStrBuilder(CMDRC["STATS"]["Crafting"]["ENGI_ROLLS"])} times on the button \"Generate modification\" to upgrade your fleet.",
            ])
        if(CMDRC["STATS"]["Materials"]["MAT_COUNT"]):
            types.extend([
            f"Engineering doesn't happen without materials, this year you've traded {self.numberStrBuilder(CMDRC["STATS"]["Materials"]["MAT_COUNT"])} materials across {self.numberStrBuilder(CMDRC["STATS"]["Materials"]["MAT_TRADES"])} trades.",
            ])

        types.extend([
            " ",
            f"This year you've hired {self.numberStrBuilder(CMDRC["STATS"]["Crew"]["CREW_HIRED"])} NPC crew, fired {self.numberStrBuilder(CMDRC["STATS"]["Crew"]["CREW_FIRED"])} and lost {self.numberStrBuilder(CMDRC["STATS"]["Crew"]["CREW_KIA"])} in the darkness of space...",
        ])
        if(CMDRC["STATS"]["Crew"]["CREW_WAGES"] > 0):
            types.append(f"Despite your best efforts during contract negotatiation you've paid them {self.numberStrBuilder(CMDRC["STATS"]["Crew"]["CREW_WAGES"])} CR across the year.")
        types.extend([
            f"This year you've played {self.numberStrBuilder(CMDRC["STATS"]["CQC"]["TIME_PLAYED"]/3600)} hours of CQC{words[4]}",
            " "
        ])
        if(CMDRC["STATS"]["FleetCarrier"]["TOTAL_DISTANCE"] > 0 or CMDRC["STATS"]["FleetCarrier"]["TOTAL_REARM"] > 0 or CMDRC["STATS"]["FleetCarrier"]["TOTAL_REFUEL"] > 0 or CMDRC["STATS"]["FleetCarrier"]["TOTAL_REPAIR"] > 0):
            types.append("A fleet carrier is a CMDR's pride, and most valuable asset (trit crew set aside), here's yours in numbers:")
            if(CMDRC["STATS"]["FleetCarrier"]["TOTAL_DISTANCE"] > 0):
                types.append(f"- It jumped across {self.numberStrBuilder(CMDRC["STATS"]["FleetCarrier"]["TOTAL_DISTANCE"])} lys in about {self.numberStrBuilder(CMDRC["STATS"]["FleetCarrier"]["TOTAL_JUMPS"]*20/60)} hours (you could've used a ship ya know).")
            if(CMDRC["STATS"]["FleetCarrier"]["TOTAL_REARM"] > 0 or CMDRC["STATS"]["FleetCarrier"]["TOTAL_REFUEL"] > 0 or CMDRC["STATS"]["FleetCarrier"]["TOTAL_REPAIR"] > 0):
                types.append(f"- You've rearmed, refueled, and repaired CMDRs {self.numberStrBuilder(CMDRC["STATS"]["FleetCarrier"]["TOTAL_REARM"])}, {self.numberStrBuilder(CMDRC["STATS"]["FleetCarrier"]["TOTAL_REFUEL"])}, {self.numberStrBuilder(CMDRC["STATS"]["FleetCarrier"]["TOTAL_REPAIR"])} times respectively ! Thank you for your service o7")
        types.extend([
            " ",
            "A game is also its music... You've listened, we took note, here are the three themes you've listened to the most:",
            f"- {musics[2][1]}, {musics[2][0]} times",
            f"- {musics[3][1]}, {musics[3][0]} times",
            f"- {musics[4][1]}, {musics[4][0]} times",
            " "])
        TYPE.multipleSlowType(types)

        if("MISSIONS" in list(CMDRC.keys())):
            if(CMDRC["MISSIONS"]["MissionAccepted"] > 0):
                TYPE.slowType('You\'ve spent some time doing missions, here\'s how that breaks down in numbers:')
                slines = [
                        f'- {CMDRC["MISSIONS"]["MissionAccepted"]} accepted', 
                        f'- {CMDRC["MISSIONS"]["MissionCompleted"]} completed', 
                        f'- {CMDRC["MISSIONS"]["MissionAbandoned"]} abandoned', 
                        f'- {CMDRC["MISSIONS"]["MissionFailed"]} failed',
                        f'- Among those, {CMDRC["MISSIONS"]["Mission_Mining_name"]} were Wing Mining Missions and {CMDRC["MISSIONS"]["Mission_MassacreWing"]} were Wing Massacre Missions.'
                        ]
                TYPE.multipleSlowType(slines)
        if("JUMPS" in list(CMDRC.keys())):
            jump_text = [
                " ",
                "You've jumped, jumped, and jumped... here are your three favourite destinations of the year:",
                f"- {jumps[0][1]}, {jumps[0][0]} times",
                f"- {jumps[1][1]}, {jumps[1][0]} times",
                f"- {jumps[2][1]}, {jumps[2][0]} times",
                " "]
            TYPE.multipleSlowType(jump_text)
        
        '''
        tot = 0
        for el in jumps:
            tot += int(el[0])
        print(f"Total number of jumps: {tot}")
        '''
        
        for key in list(CMDRC['RANKS'].keys()):
            if(CMDRC['RANKS'][key][0] > 0):
                types = [
                    "All of this made you progress through this galaxy, getting closer to the legends, let's see...",
                    " "
                ]
                TYPE.multipleSlowType(types)
                break
        if(CMDRC['RANKS']['Empire'][0] > 0):
            TYPE.slowType(f"You've gained {CMDRC['RANKS']['Empire'][0]} ranks to the Empire this year, reaching the valued rank of {self.rank_dict["Empire"][CMDRC['RANKS']['Empire'][1]]} !")
        if(CMDRC['RANKS']['Federation'][0] > 0):
            TYPE.slowType(f"You've gained {CMDRC['RANKS']['Federation'][0]} ranks with the Feds this year, reaching the valued rank of {self.rank_dict["Federation"][CMDRC['RANKS']['Federation'][1]]} !")
        if(CMDRC['RANKS']['Combat'][0] > 0):
            TYPE.slowType(f"You've reached the rank of {self.rank_dict["Combat"][CMDRC['RANKS']['Combat'][1]]} in Combat, blasting your way through {CMDRC['RANKS']['Combat'][0]} rank(s) !")
        if(CMDRC['RANKS']['Trade'][0] > 0):
            TYPE.slowType(f"You've reached the monetary status of {self.rank_dict["Trade"][CMDRC['RANKS']['Trade'][1]]}, hauling your Type-9, Cutter or Plipper through {CMDRC['RANKS']['Trade'][0]} rank(s) !")
        if(CMDRC['RANKS']['Explore'][0] > 0):
            TYPE.slowType(f"You've become a(n) {self.rank_dict["Explore"][CMDRC['RANKS']['Explore'][1]]} among the explorers, uncovering the mysteries of the Black across {CMDRC['RANKS']['Explore'][0]} rank(s) !")
        if(CMDRC['RANKS']['Soldier'][0] > 0):
            TYPE.slowType(f"Dropped on the surface, you made yourself a respected {self.rank_dict["Soldier"][CMDRC['RANKS']['Soldier'][1]]} on the battlefields, silencing your doubters with guns and grenades as you made your way across {CMDRC['RANKS']['Soldier'][0]} rank(s)...")
        if(CMDRC['RANKS']['Exobiologist'][0] > 0):
            TYPE.slowType(f"Some say you've spent your time licking plants and rocks on foreign bodies, but we know (and Vista's payout show it) you've truly worked out there, reaching the rank of {self.rank_dict["Exobiologist"][CMDRC['RANKS']['Exobiologist'][1]]} in exobiology, coming from {CMDRC['RANKS']['Exobiologist'][0]} rank(s) under.")
        if(CMDRC['RANKS']['CQC'][0] > 0):
            TYPE.slowType(f"You've.. somehow found enough matches of CQC to climb through {CMDRC['RANKS']['CQC'][0]} rank(s), reaching {self.rank_dict["CQC"][CMDRC['RANKS']['CQC'][1]]} in this unloved category. I can only say: Bravo!")
        print(" ")
        lines = [
            "There are still wonders to uncover, and questions to solve, so we'll stop stealing your time here,",
            "and wish you nothing but the best in your future endeavours CMDR !",
            "We hope you'll keep playing next year and, in the meantime, fly dangerously o7",
            " ",
            "Before going, the stat you've been waiting for, this year you played: ",
            f"\033[1m{self.numberStrBuilder(CMDRC['STATS']['Exploration']['TOTAL_TIME']/3600)} hours\033[0m, that's \033[1m{self.numberStrBuilder(CMDRC['STATS']['Exploration']['TOTAL_TIME']/(3600*24))} days\033[0m !"
        ]
        TYPE.multipleSlowType(lines)
        TYPE.slowType("Press enter to continue...")
        input()
