from toontown.building.DistributedBossElevatorAI import DistributedBossElevatorAI
from toontown.building import ElevatorConstants


class DistributedVPElevatorAI(DistributedBossElevatorAI):
    def __init__(self, air, bldg, zone, antiShuffle = 0, minLaff = 0):
        DistributedBossElevatorAI.__init__(self, air, bldg, zone, antiShuffle=antiShuffle, minLaff=minLaff)

        self.type = ElevatorConstants.ELEVATOR_VP
        self.countdownTime = ElevatorConstants.ElevatorData[self.type]['countdown']
