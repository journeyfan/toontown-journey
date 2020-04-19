import time
from random import random, randint, choice
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from toontown.battle import SuitBattleGlobals
from toontown.toonbase.ToontownGlobals import IDES_OF_MARCH
from . import SuitDNA
from .SuitInvasionGlobals import *
from otp.ai.MagicWordGlobal import *


class SuitInvasionManagerAI:
    notify = directNotify.newCategory('SuitInvasionManagerAI')

    def __init__(self, air):
        self.air = air

        self.invading = False
        self.start = 0
        self.remaining = 0
        self.total = 0
        self.suitDeptIndex = None
        self.suitTypeIndex = None
        self.megaInvasion = None
        self.megaInvasionCog = None
        self.megaInvasionFlags = None
        self.flags = 0
        self.isSkelecog = 0
        self.isV2 = 0
        self.isWaiter = 0
        self.isVirtual = 0
        self.isRental = 0
        self.flags = [0, 0, 0, 0, 0]

        self.air.netMessenger.accept(
            'startInvasion', self, self.handleStartInvasion)
        self.air.netMessenger.accept(
            'stopInvasion', self, self.handleStopInvasion)

        # We want to handle shard status queries so that a ShardStatusReceiver
        # being created after we're created will know where we're at:
        self.air.netMessenger.accept('queryShardStatus', self, self.sendInvasionStatus)

        self.safeHarbours = []
        tempSafeHarbours = config.GetString('safe-harbours','')
        if tempSafeHarbours != '':
            for safeHarbour in tempSafeHarbours.split(","):
                safeHarbour = safeHarbour.strip()
                self.safeHarbours.append(safeHarbour)
        
        if config.GetBool('want-mega-invasions', False):
            self.randomInvasionProbability = config.GetFloat('mega-invasion-probability', 0.65)
            if self.air.distributedDistrict.name in self.safeHarbours:
                self.notify.debug("Can't summon mega invasion in safe harbour!")
            elif self.air.holidayManager.isHolidayRunning(IDES_OF_MARCH):#Temp
                self.megaInvasion = IDES_OF_MARCH
                #if self.megaInvasion:
                # self.megaInvasionCog = megaInvasionDict[self.megaInvasion][0]
                taskMgr.doMethodLater(randint(1800, 5400), self.__randomInvasionTick, 'random-invasion-tick')
                
        self.sendInvasionStatus()

    def getInvading(self):
        return self.invading

    def getInvadingCog(self):
        return (self.suitDeptIndex, self.suitTypeIndex, self.flags)

    def startInvasion(self, suitDeptIndex=None, suitTypeIndex=None, flags=[0, 0, 0, 0, 0],
                      type=INVASION_TYPE_NORMAL):
        if self.invading:
            # An invasion is currently in progress; ignore this request.
            return False

        if (suitDeptIndex is None) and (suitTypeIndex is None) and (not flags):
            # This invasion is no-op.
            return False
            
        if((flags[2] == 1) and (flags[0] == 1 or flags[4] == 1)):
            return False

        if((flags[0] == 1) and (flags[1] == 1 or flags[2] == 1 or flags[4] == 1)):
            return False             
        

        if (suitDeptIndex is None) and (suitTypeIndex is not None):
            # It's impossible to determine the invading Cog.
            return False

        if (suitDeptIndex is not None) and (suitDeptIndex >= len(SuitDNA.suitDepts)):
            # Invalid suit department.
            return False

        if (suitTypeIndex is not None) and (suitTypeIndex >= SuitDNA.suitsPerDept):
            # Invalid suit type.
            return False

        if type not in (INVASION_TYPE_NORMAL, INVASION_TYPE_MEGA):
            # Invalid invasion type.
            return False

        # Looks like we're all good. Begin the invasion:
        self.invading = True
        self.start = int(time.time())
        self.suitDeptIndex = suitDeptIndex
        self.suitTypeIndex = suitTypeIndex
        self.flags = flags
        self.isSkelecog = flags[0]
        self.isV2 = flags[1]
        self.isWaiter = flags[2] 
        self.isVirtual = flags[3]
        self.isRental = flags[4]

        # How many suits do we want?
        if type == INVASION_TYPE_NORMAL:
            self.total = 1000
        elif type == INVASION_TYPE_MEGA:
            self.total = randint(1800, 5400)
        self.remaining = self.total

        self.flySuits()
        self.notifyInvasionStarted()

        # Update the invasion tracker on the districts page in the Shticker Book:
        if self.suitDeptIndex is not None:
            self.air.districtStats.b_setInvasionStatus(self.suitDeptIndex + 1)
        else:
            self.air.districtStats.b_setInvasionStatus(5)

        # If this is a normal invasion, and the players take too long to defeat
        # all of the Cogs, we'll want the invasion to timeout:
        if type == INVASION_TYPE_NORMAL:
            timeout = config.GetInt('invasion-timeout', 1800)
            taskMgr.doMethodLater(timeout, self.stopInvasion, 'invasionTimeout')

        self.sendInvasionStatus()
        return True

    def stopInvasion(self, task=None):
        if not self.invading:
            # We are not currently invading.
            return False

        # Stop the invasion timeout task:
        taskMgr.remove('invasionTimeout')

        # Update the invasion tracker on the districts page in the Shticker Book:
        self.air.districtStats.b_setInvasionStatus(0)

        # Revert what was done when the invasion started:
        self.notifyInvasionEnded()
        self.invading = False
        self.start = 0
        self.suitDeptIndex = None
        self.suitTypeIndex = None
        self.flags = None
        self.total = 0
        self.remaining = 0
        self.flySuits()

        self.sendInvasionStatus()
        return True

    def getSuitName(self):
        if self.suitDeptIndex is not None:
            if self.suitTypeIndex is not None:
                return SuitDNA.getSuitName(self.suitDeptIndex, self.suitTypeIndex)
            else:
                return SuitDNA.suitDepts[self.suitDeptIndex]
        else:
            return SuitDNA.suitHeadTypes[0]

    def notifyInvasionStarted(self):
        msgType = SuitInvasionBegin
        if self.isSkelecog:
            msgType = SkelecogInvasionBegin
        elif self.isV2:
            msgType = V2InvasionBegin
        elif self.isWaiter:
            msgType = WaiterInvasionBegin
        elif self.isVirtual:
            msgType = VirtualInvasionBegin
        elif self.isRental:
            msgType = RentalInvasionBegin
        self.air.newsManager.sendUpdate(
            'setInvasionStatus',
            [msgType, self.getSuitName(), self.total, self.flags])

    def notifyInvasionEnded(self):
        msgType = SuitInvasionEnd
        if self.isSkelecog:
            msgType = SkelecogInvasionEnd
        elif self.isV2:
            msgType = V2InvasionEnd
        elif self.isWaiter:
            msgType = WaiterInvasionEnd
        elif self.isVirtual:
            msgType = VirtualInvasionEnd 
        elif self.isRental:
            msgType = RentalInvasionEnd            
        self.air.newsManager.sendUpdate(
            'setInvasionStatus', [msgType, self.getSuitName(), 0, self.flags])

    def notifyInvasionUpdate(self):
        self.air.newsManager.sendUpdate(
            'setInvasionStatus',
            [SuitInvasionUpdate, self.getSuitName(),
             self.remaining, self.flags])

    def notifyInvasionBulletin(self, avId):
        msgType = SuitInvasionBulletin
        if self.isSkelecog:
            msgType = SkelecogInvasionBulletin
        elif self.isV2:
            msgType = V2InvasionBulletin
        elif self.isWaiter:
            msgType = WaiterInvasionBulletin
        elif self.isVirtual:
            msgType = VirtualInvasionBulletin     
        elif self.isRental:
            msgType = RentalInvasionBulletin            
        self.air.newsManager.sendUpdateToAvatarId(
            avId, 'setInvasionStatus',
            [msgType, self.getSuitName(), self.remaining, self.flags])

    def flySuits(self):
        for suitPlanner in list(self.air.suitPlanners.values()):
            suitPlanner.flySuits()

    def handleSuitDefeated(self):
        self.remaining -= 1
        if self.remaining == 0:
            self.stopInvasion()
        elif self.remaining == (self.total/2):
            self.notifyInvasionUpdate()
        self.sendInvasionStatus()

    def handleStartInvasion(self, shardId, *args):
        if shardId == self.air.ourChannel:
            self.startInvasion(*args)

    def handleStopInvasion(self, shardId):
        if shardId == self.air.ourChannel:
            self.stopInvasion()

    def sendInvasionStatus(self):
        if self.invading:
            if self.suitDeptIndex is not None:
                if self.suitTypeIndex is not None:
                    type = SuitBattleGlobals.SuitAttributes[self.getSuitName()]['name']
                else:
                    type = SuitDNA.getDeptFullname(self.getSuitName())
            else:
                type = None
            status = {
                'invasion': {
                    'type': type,
                    'flags': [self.isSkelecog, self.isV2, self.isWaiter, self.isVirtual, self.isRental],
                    'remaining': self.remaining,
                    'total': self.total,
                    'start': self.start
                }
            }
        else:
            status = {'invasion': None}
        self.air.netMessenger.send('shardStatus', [self.air.ourChannel, status])
        
    def __randomInvasionTick(self, task=None):
        """
        Each hour, have a tick to check if we want to start an invasion in
        the current district. This works by having a random invasion
        probability, and each tick it will generate a random float between
        0 and 1, and then if it's less than or equal to the probablity, it
        will spawn the invasion.
        An invasion will not be started if there is an invasion already
        on-going.
        """
        # Generate a new tick delay.
        task.delayTime = randint(1800, 5400)
        if self.getInvading():
            # We're already running an invasion. Don't start a new one.
            self.notify.debug('Invasion tested but already running invasion!')
            return task.again
        if random() <= self.randomInvasionProbability:
            # We want an invasion!
            self.notify.debug('Invasion probability hit! Starting invasion.')
            if config.GetBool('want-mega-invasions', False):
                suitDept = megaInvasionDict[self.megaInvasion][0][0]
                suitIndex = megaInvasionDict[self.megaInvasion][0][1]
                if megaInvasionDict[self.megaInvasion][2]:
                    rngFlag = randint(0, 4)
                    flags = [0, 0, 0, 0, 0]
                    flags[rngFlag] = 1
                else:
                    flags = megaInvasionDict[self.megaInvasion][1]
                self.startInvasion(suitDept, suitIndex, flags, INVASION_TYPE_MEGA)
        return task.again
    
@magicWord(category=CATEGORY_COMMUNITY_MANAGER, types=[str, int, int, int])
def invasion(cmd='start', dept=0, suit=0, flag=0):
    """
    Starts/stops an invasion.
    """
    if cmd == 'start':
        if dept < 0 or dept > 4:
            return 'Invalid suit department. Must be 0-4.'
        elif suit < 0 or suit > 7:
            return 'Invalid suit. Must be 0-7.'
        elif flag < 0 or flag > 4:
            return 'Invalid flags. Valid flags:\n0-Normal suit\n1-Skelecog\n2-Waiter\n4-V2'
        if not simbase.air.suitInvasionManager.getInvading():
            flags = [0, 0, 0, 0, 0]
            flags[flag] = 1
            simbase.air.suitInvasionManager.startInvasion(dept, suit, flags)
            return 'Started invasion!'
        else:
            if simbase.air.suitInvasionManager.getInvading():
                return 'There is already an invasion in progress.'
    elif cmd == 'end':
        if simbase.air.suitInvasionManager.getInvading():
            simbase.air.suitInvasionManager.stopInvasion()
            return 'Stopped invasion!'
        return 'There is no invasion in progress.'
    else:
        return 'Invalid command %s.' % cmd
