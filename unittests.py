import os
import re
import json
import glob
import time
import unittest
from reader import journalReader
from recap import CMDRecap
from typeprinter import TypePrinter


class Test(unittest.TestCase):

    '''
    def test_blow_type(self):
        sentence = "I would like to see this thing typed slowly like a type printer ?"
        type = TypePrinter()
        type.slowType(sentence)
        print("Test")
        type.clearConsole()

    def test_reader_findLogs(self):
        reader = journalReader()
        allLogs = reader.findLogs()
        empirLogs = glob.glob('C:\\Users\\coqua\\Saved Games\\Frontier Developments\\Elite Dangerous\\*.log')
        self.assertEqual(allLogs, empirLogs, allLogs)

    def test_reader_sortLogsYear_empty(self):
        reader = journalReader()
        allLogs = reader.findLogs()
        sortedLogs = reader.sortLogsYear(allLogs)
        error = (True, 0)
        for el in list(sortedLogs.keys()):
            if(el != 2025 and len(sortedLogs[el]) == 0):
                pass
            elif(el != 2025 and len(sortedLogs[el]) == 0):
                error = (False, el)

        self.assertTrue(error[0], error[1])

    def test_reader_sortLogsYear_full(self):
        reader = journalReader()
        allLogs = reader.findLogs()
        sortedLogs = reader.sortLogsYear(allLogs)
        self.assertEqual(813, len(sortedLogs[2025]), len(sortedLogs[2025]))

    def test_regex_sortLogsByCMDR(self):
        line = '{ "timestamp":"2025-11-13T09:14:23Z", "event":"Commander", "FID":"F6103330", "Name":"Hotwraith" }'
        self.assertEqual('Hotwraith', re.findall('"Name":"([A-z]{1,})', line)[0], re.findall('"Name":"([A-z]{1,})', line)[0])

    def test_recap_scrapJournals(self):
        reader = journalReader()
        allLogs = reader.findLogs()
        sortedLogs = reader.sortLogsByCMDR(allLogs)
        hotwraith_year = reader.sortLogsYear(sortedLogs['Hotwraith'])
        recap_hot = CMDRecap(hotwraith_year)
        json.dumps(recap_hot.scrapJournals(["\"event\":\"Statistics\""]), indent=4)
    
    def test_recap_gatherStats(self):
        reader = journalReader()
        allLogs = reader.findLogs()
        sortedLogs = reader.sortLogsByCMDR(allLogs)
        hotwraith_year = reader.sortLogsYear(sortedLogs['Hotwraith'])
        recap_hot = CMDRecap(hotwraith_year)
        re = recap_hot.scrapJournals(["\"event\":\"Statistics\""])
        recap_hot.gatherStats(re)
    
    def test_recap_gatherMusic(self):
        reader = journalReader()
        allLogFiles = reader.findLogs()
        sortedLogs = reader.sortLogsByCMDR(allLogFiles)
        hotwraith_year = reader.sortLogsYear(sortedLogs['Hotwraith'])
        recap_for_hotw = CMDRecap(hotwraith_year)
        re = recap_for_hotw.scrapJournals(["\"event\":\"Music\""])
        recap_for_hotw.gatherMusic(re)
    
    def test_recap_gatherRanks(self):
        reader = journalReader()
        allLogFiles = reader.findLogs()
        sortedLogs = reader.sortLogsByCMDR(allLogFiles)
        hotwraith_year = reader.sortLogsYear(sortedLogs['Hotwraith'])
        recap_for_hotw = CMDRecap(hotwraith_year)
        re = recap_for_hotw.scrapJournals(["\"event\":\"Rank\"", "\"event\":\"Progress\""])
        recap_for_hotw.gatherRanks(re)
    '''

    def test_complete(self):
        reader = journalReader()
        allLogs = reader.findLogs()
        sortedByCMDR = reader.sortLogsByCMDR(allLogs)
        hotwraith_logs = reader.sortLogsYear(sortedByCMDR['Hotwraith'])
        hotwrcp = CMDRecap(hotwraith_logs)

if __name__ == '__main__':
    unittest.main()