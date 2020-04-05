from direct.directnotify import DirectNotifyGlobal
import DistributedFactoryAI
from toontown.toon import NPCToons
import random

class DistributedBrutalFactoryAI(DistributedFactoryAI.DistributedFactoryAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBrutalFactoryAI')

    def __init__(self, air, factoryId, zoneId, entranceId, avIds):
        DistributedFactoryAI.DistributedFactoryAI.__init__(self, air, factoryId, zoneId, entranceId, avIds)

    def setVictors(self, victorIds):
        DistributedFactoryAI.DistributedFactoryAI.setVictors(self, victorIds)

        activeVictors = []
        for victorId in victorIds:
            toon = self.air.doId2do.get(victorId)
            if toon is not None:
                activeVictors.append(toon)
        npcId = random.choice(NPCToons.npcFriendsMinMaxStars(3, 3))
        for toon in activeVictors:
            toon.attemptAddNPCFriend(npcId)
            toon.d_setSystemMessage(0, 'You got a %s SOS card.' % (NPCToons.getNPCName(npcId)))

