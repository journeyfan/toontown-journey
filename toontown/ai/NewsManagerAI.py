from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectAI import DistributedObjectAI


class NewsManagerAI(DistributedObjectAI):
    notify = directNotify.newCategory('NewsManagerAI')

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        self.accept('avatarEntered', self.__handleAvatarEntered)

    def __handleAvatarEntered(self, avatar):
        if self.air.suitInvasionManager.getInvading():
            self.air.suitInvasionManager.notifyInvasionBulletin(avatar.getDoId())
        self.holidayNotify()    

    def setPopulation(self, todo0):
        pass

    def setBingoWin(self, zoneId):
        pass
        #self.sendUpdate('setBingoWin', zoneId)

    def setBingoStart(self):
        pass
        #self.sendUpdateToAvatarId('setBingoStart')

    def setBingoEnd(self):
        pass
        #self.sendUpdate('setBingoEnd')

    def setCircuitRaceStart(self):
        pass

    def setCircuitRaceEnd(self):
        pass

    def setTrolleyHolidayStart(self):
        pass
        #self.sendUpdate('setTrolleyHolidayStart')

    def setTrolleyHolidayEnd(self):
        pass
        #self.sendUpdate('SetTrolleyHolidayEnd')

    def setTrolleyWeekendStart(self):
        pass

    def setTrolleyWeekendEnd(self):
        pass

    def setRoamingTrialerWeekendStart(self):
        pass

    def setRoamingTrialerWeekendEnd(self):
        pass

    def setInvasionStatus(self, msgType, cogType, numRemaining, flags):
        self.sendUpdate('setInvasionStatus', args=[msgType, cogType, numRemaining, flags])

    def setHolidayIdList(self, holidays):
        self.sendUpdate('setHolidayIdList', holidays)

    def holidayNotify(self):
        self.sendUpdate('holidayNotify')

    def setWeeklyCalendarHolidays(self, todo0):
        pass

    def getWeeklyCalendarHolidays(self):
        return [(19, 0)]

    def setYearlyCalendarHolidays(self, todo0):
        pass

    def getYearlyCalendarHolidays(self):
        return []

    def setOncelyCalendarHolidays(self, todo0):
        pass

    def getOncelyCalendarHolidays(self):
        return []

    def setRelativelyCalendarHolidays(self, todo0):
        pass

    def getRelativelyCalendarHolidays(self):
        return []

    def setMultipleStartHolidays(self, todo0):
        pass

    def getMultipleStartHolidays(self):
        return []

    def sendSystemMessage(self, todo0, todo1):
        pass

