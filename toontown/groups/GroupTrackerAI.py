from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI

class GroupTrackerAI(DistributedObjectGlobalAI):
    def __init__(self):
        self.avId = self.air.getAvatarIdFromSender()

    def announceGenerate(self):
        DistributedObjectGlobalAI.announceGenerate(self)

    def createGroupAI(self, leaderId, leaderName, district, place, memberIds, memberNames, display):
        self.sendUpdate('createGroup', [leaderId, [leaderName, district, place, memberIds, memberNames, display]])

    def updateGroupAI(self, leaderId, place, memberIds, memberNames, display):
        self.sendUpdate('updateGroup', [leaderId, place, memberIds, memberNames, display])

    def display(self, display):
        
        self.sendUpdate('displayGroup', [self.avId, display])
    
