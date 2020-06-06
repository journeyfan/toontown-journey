from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from GroupTrackerGlobals import *
from itertools import izip
class GroupTracker(DistributedObjectGlobal):
    def __init__(self):
        self.group = {}
        self.doId = base.localAvatar.doId
    def announceGenerate(self):
        DistributedObjectGlobal.announceGenerate(self)
    
    def requestGroups(self):
        self.sendUpdate('requestGroups', [self.doId])

    def finishedRequesting(self):
        self.sendUpdate('finishedRequesting', [self.doId])

    def setInfo(self, leaderIds, groups):
        self.group = dict(izip(leaderIds, [list(i) for i in groups]))
        messenger.send('GroupTrackResponse')

    def getInfo(self):
        return self.group.values()

    def updateGroupInfo(self, leaderId, place, memberIds, memberNames, display):
        if leaderId not in self.group:
            return
        self.group[leaderId][PLACE] = place
        self.group[leaderId][MEMBER_IDS] = memberIds
        self.group[leaderId][MEMBER_NAMES] = memberNames
        self.group[leaderId][DISPLAY] = display
        messenger.send('GroupTrackResponse')

    def display(self, display):
        self.sendUpdate('display', [display])






