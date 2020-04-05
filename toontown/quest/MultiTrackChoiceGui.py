from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import ToontownTimer
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import ToontownBattleGlobals
from toontown.toonbase import TTLocalizer

class TrackPoster(DirectFrame):
    normalTextColor = (0.3, 0.25, 0.2, 1)

    def __init__(self, trackId, callback):
        DirectFrame.__init__(self, relief=None)
        self.initialiseoptions(TrackPoster)
        bookModel = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        trackName = ToontownBattleGlobals.Tracks[trackId].capitalize()
        self.poster = DirectFrame(parent=self, relief=None, image=bookModel.find('**/questCard'), image_scale=(0.4, 0.29, 0.29))
        invModel = loader.loadModel('phase_3.5/models/gui/inventory_icons')
        iconGeom = invModel.find('**/' + ToontownBattleGlobals.AvPropsNew[trackId][5])
        invModel.removeNode()
        self.pictureFrame = DirectFrame(parent=self.poster, relief=None, image=bookModel.find('**/questPictureFrame'), image_scale=0.125,
            image_color=(0.45, 0.8, 0.45, 1), text=trackName, text_font=ToontownGlobals.getInterfaceFont(), text_pos=(0, -0.14), 
            text_fg=self.normalTextColor, text_scale=0.05, text_align=TextNode.ACenter, text_wordwrap=8.0, textMayChange=0, geom=iconGeom, geom_scale=(0.8, 0.8, 0.8), pos=(0.0, 0, 0.05))
        bookModel.removeNode()
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        self.chooseButton = DirectButton(parent=self.poster, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), 
            image_scale=(0.7, 1, 1), text=TTLocalizer.TrackChoiceGuiChoose, text_scale=0.06, text_pos=(0, -0.02), command=callback, extraArgs=[trackId], pos=(0, 0, -0.20), scale=0.8)
        guiButton.removeNode()
        return


class MultiTrackChoiceGui(DirectFrame):
    TrackPosterPos = [
        (-0.5, 0, 0.5),
        (0, 0, 0.5),
        (0.5, 0, 0.5),
        (-0.5, 0, 0.1),
        (0, 0, 0.1),
        (0.5, 0, 0.1),
        (0, 0, -0.3)    
    ]

    def __init__(self, tracks, timeout):
        DirectFrame.__init__(self, relief=None, geom=DGG.getDefaultDialogGeom(), geom_color=Vec4(0.8, 0.6, 0.4, 1), geom_scale=(1.5, 1, 1.5), geom_hpr=(0, 0, -90), pos=(0, 0, 0))
        self.initialiseoptions(MultiTrackChoiceGui)
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        self.cancelButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(0.7, 1, 1), text=TTLocalizer.TrackChoiceGuiCancel, pos=(0.15, 0, -0.625), text_scale=0.06, text_pos=(0, -0.02), command=self.chooseTrack, extraArgs=[-1])
        guiButton.removeNode()
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(self)
        self.timer.setScale(0.35)
        self.timer.setPos(-0.2, 0, -0.6)
        self.timer.countdown(timeout, self.timeout)
        self.trackChoicePosters = []
        i = 0
        for trackId in tracks:
            print 'at track '+str(trackId)
            tp = TrackPoster(trackId, self.chooseTrack)
            tp.reparentTo(self)
            self.trackChoicePosters.append(tp)
            tp.setPos(self.TrackPosterPos[i])
            i+=1
        return

    def chooseTrack(self, trackId):
        self.timer.stop()
        messenger.send('chooseTrack', [trackId])

    def timeout(self):
        messenger.send('chooseTrack', [-1])
