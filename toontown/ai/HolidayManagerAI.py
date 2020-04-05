from toontown.toonbase import ToontownGlobals

class HolidayManagerAI:

    def __init__(self, air):
        self.air = air
        self.currentHolidays = []
        self.xpMultiplier = 1
        self.setup()

    def setup(self):
        holidays = config.GetString('active-holidays','')
        if holidays != '':
            for holiday in holidays.split(","):
                holiday = int(holiday)
                self.currentHolidays.append(holiday)
            simbase.air.newsManager.setHolidayIdList([self.currentHolidays])

    def isHolidayRunning(self, holidayId):
        if holidayId in self.currentHolidays:
            return True

    def isMoreXpHolidayRunning(self):
        if ToontownGlobals.MORE_XP_HOLIDAY in self.currentHolidays:
            self.xpMultiplier = 2
            return True
        return False

    def getXpMultiplier(self):
        return self.xpMultiplier

    def appendHoliday(self, holidayId):
        if holidayId not in self.currentHolidays:
            self.currentHolidays.append(holidayId)
            self.air.newsManager.setHolidayIdList([self.currentHolidays])
            return True

    def removeHoliday(self, holidayId):
        if holidayId in self.currentHolidays:
            self. currentHolidays.remove(holidayId)
            self.air.newsManager.setHolidayIdList([self.currentHolidays])
            return True

from otp.ai.MagicWordGlobal import *

@magicWord(category=CATEGORY_PROGRAMMER, types=[int])
def startHoliday(holidayId):
    if simbase.air.holidayManager.appendHoliday(holidayId) == True:
        return 'Started Holiday %s' % holidayId
    return 'Holiday %s is already running' % holidayId

@magicWord(category=CATEGORY_PROGRAMMER, types=[int])
def endHoliday(holidayId):
    if simbase.air.holidayManager.removeHoliday(holidayId) == True:
        return 'Ended Holiday %s' % holidayId
    return 'Holiday %s already ended' % holidayId