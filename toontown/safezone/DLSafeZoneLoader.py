from toontown.safezone import DLPlayground
from toontown.safezone import SafeZoneLoader


class DLSafeZoneLoader(SafeZoneLoader.SafeZoneLoader):
    def __init__(self, hood, parentFSM, doneEvent):
        SafeZoneLoader.SafeZoneLoader.__init__(self, hood, parentFSM, doneEvent)
        self.playgroundClass = DLPlayground.DLPlayground
        self.musicFile = 'phase_8/audio/bgm/DL_nbrhood.mp3'
        self.activityMusicFile = 'phase_8/audio/bgm/DL_SZ_activity.mp3'
        self.dnaFile = 'phase_8/dna/donalds_dreamland_sz.dna'
        self.safeZoneStorageDNAFile = 'phase_8/dna/storage_DL_sz.dna'
