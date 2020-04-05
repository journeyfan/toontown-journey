from toontown.building.DistributedCFOElevator import DistributedCFOElevator
from toontown.toonbase import TTLocalizer


class DistributedBrutalCFOElevator(DistributedCFOElevator):
    notify = directNotify.newCategory('DistributedBrutalCFOElevator')

    def setupElevator(self):
        pass

    def getDestName(self):
        return TTLocalizer.ElevatorBrutalCashBotBoss