# Types:
INVASION_TYPE_NORMAL = 0
INVASION_TYPE_MEGA = 1

# Flags:
IsSkelecog = 0
IsV2 = 1
IsWaiter = 2
IsVirtual = 3
isRental = 4
IFSkelecog = 0
IFWaiter = 2
IFV2 = 1

from toontown.toonbase.ToontownGlobals import IDES_OF_MARCH#Temp until I refactor source to HolidayGlobals
#Mega Invasion Dict
megaInvasionDict = {
    #Holiday ID   #Cog Index   #Flags    #Random flags?
    IDES_OF_MARCH: ((1, 4), [0, 0, 0, 0, 0], True)}
#Invasion Messages
SuitInvasionBegin = 0
SuitInvasionEnd = 1
SuitInvasionUpdate = 2
SuitInvasionBulletin = 3
SkelecogInvasionBegin = 4
SkelecogInvasionEnd = 5
SkelecogInvasionBulletin = 6
WaiterInvasionBegin = 7
WaiterInvasionEnd = 8
WaiterInvasionBulletin = 9
V2InvasionBegin = 10
V2InvasionEnd = 11
V2InvasionBulletin = 12
VirtualInvasionBegin = 13
VirtualInvasionEnd = 14
VirtualInvasionBulletin = 15
RentalInvasionBegin = 16
RentalInvasionEnd = 17
RentalInvasionBulletin = 18
