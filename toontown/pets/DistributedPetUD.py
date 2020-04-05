from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectUD import DistributedObjectUD

class DistributedPetUD(DistributedObjectUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPetUD")
