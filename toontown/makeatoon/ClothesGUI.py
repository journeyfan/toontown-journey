from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData
from direct.gui.DirectGui import *
from toontown.toon import ToonDNA
from toontown.toonbase import TTLocalizer
from . import ShuffleButton
from .FrameGUI import ChoiceFrame
from .MakeAToonGlobals import *

CLOTHES_MAKETOON = 0
CLOTHES_TAILOR = 1
CLOTHES_CLOSET = 2


class ClothesGUI(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('ClothesGUI')

    def __init__(self, type, doneEvent, swapEvent=None):
        StateData.StateData.__init__(self, doneEvent)
        self.type = type
        self.toon = None
        self.swapEvent = swapEvent
        self.gender = '?'
        self.girlInShorts = 0
        self.swappedTorso = 0
        return

    def load(self):
        self.gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui')
        shuffleFrame = self.gui.find('**/tt_t_gui_mat_shuffleFrame')
        shuffleArrowUp = self.gui.find('**/tt_t_gui_mat_shuffleArrowUp')
        shuffleArrowDown = self.gui.find('**/tt_t_gui_mat_shuffleArrowDown')
        shuffleArrowRollover = self.gui.find('**/tt_t_gui_mat_shuffleArrowUp')
        shuffleArrowDisabled = self.gui.find('**/tt_t_gui_mat_shuffleArrowDisabled')
        # only MakeClothesGUI has the code for SwapTopStyle currently
        if self.type == CLOTHES_MAKETOON:
            self.parentFrame = DirectFrame(relief=DGG.RAISED, pos=(1.418, 0, .50), frameColor=(1, 0, 0, 0))
            # Shirt Style
            self.shirtStyle = ChoiceFrame(parent=self.parentFrame, image_scale=halfButtonInvertScale, images=(
                shuffleFrame, (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled)),
                                          pos=(0, 0, -0.06), hpr=(0, 0, 5), scale=1.2,
                                          text=TTLocalizer.ClothesShopShirtStyle, text_scale=0.057,
                                          text_pos=(-0.001, -0.015), button_command=self.swapTopStyle)

            # Shirt Color
            self.shirtFrame = ChoiceFrame(parent=self.parentFrame, image_scale=halfButtonScale, images=(
                shuffleFrame, (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled)),
                                          pos=(0, 0, -0.3), hpr=(0, 0, 3), scale=1,
                                          text=TTLocalizer.ClothesShopShirtColor, text_scale=0.05,
                                          text_pos=(-0.001, -0.015), button_command=self.swapTopColor)

            # Bottoms Style
            self.botStyle = ChoiceFrame(parent=self.parentFrame, image_scale=halfButtonInvertScale, images=(
                shuffleFrame, (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled)),
                                        pos=(0, 0, -0.55), hpr=(0, 0, -2), scale=1.2,
                                        text=TTLocalizer.ClothesShopBottomsStyle, text_scale=0.057,
                                        text_pos=(-0.001, -0.015), button_command=self.swapBottomStyle)
            # Bottoms Color
            self.bottomFrame = ChoiceFrame(parent=self.parentFrame, image_scale=halfButtonScale,
                                           images=(shuffleFrame, (shuffleArrowUp, shuffleArrowDown,
                                                               shuffleArrowRollover,
                                                               shuffleArrowDisabled)),
                                           pos=(0, 0, -0.8), hpr=(0, 0, -4), scale=1,
                                           text=TTLocalizer.ClothesShopBottomsColor, text_scale=0.05,
                                           text_pos=(-0.001, -0.015), button_command=self.swapBottomColor)
        else:  # Default to the two button style
            self.parentFrame = DirectFrame(relief=DGG.RAISED, pos=(0.98, 0, 0.416), frameColor=(1, 0, 0, 0))
            self.shirtFrame = ChoiceFrame(parent=self.parentFrame, image_scale=halfButtonInvertScale, images=(
                shuffleFrame, (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled)),
                                          pos=(0, 0, -0.4), hpr=(0, 0, 5), scale=1.2,
                                          text=TTLocalizer.ClothesShopShirt, text_scale=0.057,
                                          text_pos=(-0.001, -0.015), button_command=self.swapTop)
            self.bottomFrame = ChoiceFrame(parent=self.parentFrame, image_scale=halfButtonInvertScale, images=(
                shuffleFrame, (shuffleArrowUp, shuffleArrowDown, shuffleArrowRollover, shuffleArrowDisabled)),
                                        pos=(0, 0, -0.65), hpr=(0, 0, -2), scale=1.2,
                                        text=TTLocalizer.ClothesShopBottoms, text_scale=0.057,
                                        text_pos=(-0.001, -0.015), button_command=self.swapBottom)
        self.parentFrame.hide()
        self.shuffleFetchMsg = 'ClothesShopShuffle'
        self.shuffleButton = ShuffleButton.ShuffleButton(self, self.shuffleFetchMsg)
        return

    def unload(self):
        self.gui.removeNode()
        del self.gui
        self.parentFrame.destroy()
        if hasattr(self, "shirtStyle"):
            self.shirtStyle.destroy()
            del self.shirtStyle
            self.botStyle.destroy()
            del self.botStyle
        self.shirtFrame.destroy()
        self.bottomFrame.destroy()
        del self.parentFrame
        del self.shirtFrame
        del self.bottomFrame
        self.shuffleButton.unload()
        self.ignore('MAT-newToonCreated')

    def showButtons(self):
        self.parentFrame.show()

    def hideButtons(self):
        self.parentFrame.hide()

    def enter(self, toon):
        self.notify.debug('enter')
        base.disableMouse()
        self.toon = toon
        self.setupScrollInterface()
        if not self.type == CLOTHES_TAILOR:
            currTop = (self.toon.style.topTex,
                       self.toon.style.topTexColor,
                       self.toon.style.sleeveTex,
                       self.toon.style.sleeveTexColor)
            currTopIndex = self.tops.index(currTop)
            self.swapTop(currTopIndex - self.topChoice)
            currBottom = (self.toon.style.botTex, self.toon.style.botTexColor)
            currBottomIndex = self.bottoms.index(currBottom)
            self.swapBottom(currBottomIndex - self.bottomChoice)
        choicePool = [self.tops, self.bottoms]
        self.shuffleButton.setChoicePool(choicePool)
        self.accept(self.shuffleFetchMsg, self.changeClothes)
        self.acceptOnce('MAT-newToonCreated', self.shuffleButton.cleanHistory)

    def exit(self):
        try:
            del self.toon
        except:
            self.notify.warning('ClothesGUI: toon not found')

        self.hideButtons()
        self.ignore('enter')
        self.ignore('next')
        self.ignore('last')
        self.ignore(self.shuffleFetchMsg)

    def setupButtons(self):
        self.girlInShorts = 0
        if self.gender == 'f':
            if self.type != CLOTHES_MAKETOON:
                if self.bottomChoice == -1:
                    botTex = self.bottoms[0][0]
                else:
                    botTex = self.bottoms[self.bottomChoice][0]
                if ToonDNA.GirlBottoms[botTex][1] == ToonDNA.SHORTS:
                    self.girlInShorts = 1
            else:
                if self.botStyleChoice == -1:
                    botTex = self.bottoms[0][0]
                else:
                    botTex = self.bottoms[self.bottomChoice][0]
                if ToonDNA.GirlBottoms[botTex][1] == ToonDNA.SHORTS:
                    self.girlInShorts = 1
        if self.toon.style.getGender() == 'm':
            if self.type != CLOTHES_MAKETOON:
                self.bottomFrame.choice_box['text'] = TTLocalizer.ClothesShopShorts
            else:
                self.botStyle.choice_box['text'] = TTLocalizer.ClothesShopShortStyles
                self.bottomFrame.choice_box['text'] = TTLocalizer.ClothesShopShortColors
        elif self.type != CLOTHES_MAKETOON:
            self.bottomFrame.choice_box['text'] = TTLocalizer.ClothesShopBottoms
        else:
            self.botStyle.choice_box['text'] = TTLocalizer.ClothesShopBottomsStyle
            self.bottomFrame.choice_box['text'] = TTLocalizer.ClothesShopBottomsColor
        self.acceptOnce('last', self.__handleBackward)
        self.acceptOnce('next', self.__handleForward)
        return None

    def swapTop(self, offset):
        length = len(self.tops)
        self.topChoice += offset
        if self.topChoice <= 0:
            self.topChoice = 0
        self.updateFrame(self.topChoice, length, self.shirtFrame)
        if self.topChoice < 0 or self.topChoice >= len(self.tops) or len(self.tops[self.topChoice]) != 4:
            self.notify.warning('topChoice index is out of range!')
            return None
        self.toon.style.topTex = self.tops[self.topChoice][0]
        self.toon.style.topTexColor = self.tops[self.topChoice][1]
        self.toon.style.sleeveTex = self.tops[self.topChoice][2]
        self.toon.style.sleeveTexColor = self.tops[self.topChoice][3]
        self.toon.generateToonClothes()
        if self.swapEvent != None:
            messenger.send(self.swapEvent)
        messenger.send('wakeup')

    def swapTopStyle(self, offset):
        length = len(self.topStyles)
        self.topStyleChoice += offset
        if self.topStyleChoice <= 0:
            self.topStyleChoice = 0
        colors = ToonDNA.getTopColors(self.gender, self.topStyles[self.topStyleChoice], tailorId=ToonDNA.MAKE_A_TOON)
        if self.topColorChoice < 0 or self.topColorChoice >= len(colors):
            self.topColorChoice = 0
        self.updateFrame(self.topStyleChoice, length, self.shirtStyle)
        self.updateFrame(self.topColorChoice, len(colors), self.shirtFrame)
        self.updateToon("TOP")

    def swapTopColor(self, offset):
        colors = ToonDNA.getTopColors(self.gender, self.topStyles[self.topStyleChoice], tailorId=ToonDNA.MAKE_A_TOON)
        length = len(colors)
        self.topColorChoice += offset
        if self.topColorChoice <= 0:
            self.topColorChoice = 0
        self.updateFrame(self.topColorChoice, length, self.shirtFrame)
        if self.topColorChoice < 0 or self.topColorChoice >= length:
            self.notify.warning('TopStyle choice out of range!')
            return
        self.updateToon("TOP")

    def swapBottom(self, offset):
        length = len(self.bottoms)
        self.bottomChoice += offset
        if self.bottomChoice <= 0:
            self.bottomChoice = 0
        self.updateFrame(self.bottomChoice, length, self.bottomFrame)
        if self.bottomChoice < 0 or self.bottomChoice >= len(self.bottoms) or len(self.bottoms[self.bottomChoice]) != 2:
            self.notify.warning('bottomChoice index is out of range!')
            return None
        self.toon.style.botTex = self.bottoms[self.bottomChoice][0]
        self.toon.style.botTexColor = self.bottoms[self.bottomChoice][1]
        if self.toon.generateToonClothes() == 1:
            self.toon.loop('neutral', 0)
            self.swappedTorso = 1
        if self.swapEvent != None:
            messenger.send(self.swapEvent)
        messenger.send('wakeup')

    def swapBottomStyle(self, offset):
        length = len(self.botStyles)
        self.botStyleChoice += offset
        if self.botStyleChoice <= 0:
            self.botStyleChoice = 0
        colors = ToonDNA.getBotColors(self.gender, self.botStyles[self.botStyleChoice], tailorId=ToonDNA.MAKE_A_TOON)
        if self.botColorChoice < 0 or self.botColorChoice >= len(colors):
            self.botColorChoice = 0
        self.updateFrame(self.botStyleChoice, length, self.botStyle)
        self.updateFrame(self.botColorChoice, len(colors), self.bottomFrame)
        self.updateToon('BOT')

    def swapBottomColor(self, offset):
        colors = ToonDNA.getBotColors(self.gender, self.botStyles[self.botStyleChoice], tailorId=ToonDNA.MAKE_A_TOON)
        length = len(colors)
        self.botColorChoice += offset
        if self.botColorChoice <= 0:
            self.botColorChoice = 0
        self.updateFrame(self.botColorChoice, length, self.bottomFrame)
        if self.botColorChoice < 0 or self.botColorChoice >= length:
            self.notify.warning('botStyle choice out of range!')
            return
        self.updateToon("BOT")

    def __handleForward(self):
        self.doneStatus = 'next'
        messenger.send(self.doneEvent)

    def __handleBackward(self):
        self.doneStatus = 'last'
        messenger.send(self.doneEvent)

    def resetClothes(self, style):
        if self.toon:
            self.toon.style.makeFromNetString(style.makeNetString())
            if self.swapEvent != None and self.swappedTorso == 1:
                self.toon.swapToonTorso(self.toon.style.torso, genClothes=0)
                self.toon.generateToonClothes()
                self.toon.loop('neutral', 0)
        return

    def changeClothes(self):
        self.notify.debug('Entering changeClothes')
        newChoice = self.shuffleButton.getCurrChoice()
        if newChoice[0] in self.tops:
            newTopIndex = self.tops.index(newChoice[0])
        else:
            newTopIndex = self.topChoice
        if newChoice[1] in self.bottoms:
            newBottomIndex = self.bottoms.index(newChoice[1])
        else:
            newBottomIndex = self.bottomChoice
        oldTopIndex = self.topChoice
        oldBottomIndex = self.bottomChoice
        self.swapTop(newTopIndex - oldTopIndex)
        self.swapBottom(newBottomIndex - oldBottomIndex)

    def updateFrame(self, choice, length, frame):
        if choice >= length - 1:
            frame.right_arrow['state'] = DGG.DISABLED
        else:
            frame.right_arrow['state'] = DGG.NORMAL
        if choice <= 0:
            frame.left_arrow['state'] = DGG.DISABLED
        else:
            frame.left_arrow['state'] = DGG.NORMAL

    def updateToon(self, section):
        if section == "TOP":
            colors = ToonDNA.getTopColors(self.gender, self.topStyles[self.topStyleChoice],
                                          tailorId=ToonDNA.MAKE_A_TOON)
            self.toon.style.topTex = self.topStyles[self.topStyleChoice][0]
            self.toon.style.sleeveTex = self.topStyles[self.topStyleChoice][1]
            self.toon.style.topTexColor = colors[self.topColorChoice][0]
            self.toon.style.sleeveTexColor = colors[self.topColorChoice][1]
        elif section == "BOT":
            colors = ToonDNA.getBotColors(self.gender, self.botStyles[self.botStyleChoice],
                                          tailorId=ToonDNA.MAKE_A_TOON)
            self.toon.style.botTex = self.botStyles[self.botStyleChoice][0]
            self.toon.style.botTexColor = colors[self.botColorChoice]
        if self.toon.generateToonClothes() == 1:
            self.toon.loop('neutral', 0)
            self.swappedTorso = 1
        if self.swapEvent != None:
            messenger.send(self.swapEvent)
        messenger.send('wakeup')

    def getCurrToonSetting(self):
        return [self.tops[self.topChoice], self.bottoms[self.bottomChoice]]
