from otp.uberdog.GlobalOtpObjectUD import GlobalOtpObjectUD
from GroupTrackerGlobals import *

class GroupTrackerUD(GlobalOtpObjectUD):
    
    def __init__(self):
        self.group = {}
        self.listeners = {}

    def announceGenerate(self):
        GlobalOtpObjectUD.announceGenerate(self)

    def createGroup(self, leaderId, groupStructure):
        self.group[leaderId] = list(groupStructure)
        place = self.group[leaderId][PLACE]
        memberIds = self.group[leaderId][MEMBER_IDS]
        memberNames = self.group[leaderId][MEMBER_NAMES]
        display = self.group[leaderId][DISPLAY]
        for listener in self.listeners:
            self.sendToAvatar(listener, 'updateGroupInfo', [leaderId, place, memberIds, memberNames, display] )
        
    def requestGroups(self, avId):
        self.requestGroupsResponse(avId)
        if avId not in self.listeners:
             self.accept('distObjDelete-{}'.format(avId), self.finishedRequesting, extraArgs=[avId])
             self.listeners.append(avId)
    
    def requestGroupsResponse(self, avId):
        if not self.group:
            return 
        self.sendToAvatar(avId, 'requestGroupsResponse', [self.group.keys(), self.groups.values()])

    def finishedRequesting(self, avId):
         self.ignore('distObjDelete-{}'.format(avId))
         if avId in self.listeners:
             self.listeners.remove(avId)

    def displayGroup(self, leaderId, display):
        if leaderId not in group:
            return
        place = self.group[leaderId][place]
        memberIds = self.group[leaderId][MEMBER_IDS]
        memberNames = self.group[leaderId][MEMBER_NAMES]
        display = self.group[leaderId][DISPLAY]

        for avId in self.listeners:
            self.sendToAvatar(avId, 'updateGroupInfo', [leaderId, place, memberIds, memberNames, display])

    