from pandac.PandaModules import *
from toontown.battle import BattleProps
from toontown.toonbase import ToontownGlobals
from toontown.toonbase.ToontownBattleGlobals import *
from direct.directnotify import DirectNotifyGlobal
import string
from toontown.suit import Suit
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from direct.task.Task import Task

class TownBattleCogPanel(DirectFrame):
    notify = DirectNotifyGlobal.directNotify.newCategory('TownBattleCogPanel')
    healthColors = (Vec4(0, 1, 0, 1),# 0 Green
     Vec4(0.5, 1, 0, 1),#1 Green-Yellow
     Vec4(0.75, 1, 0, 1),#2 Yellow-Green
     Vec4(1, 1, 0, 1),#3 Yellow
     Vec4(1, 0.866, 0, 1),#4 Yellow-Orange
     Vec4(1, 0.6, 0, 1),#5 Orange-Yellow
     Vec4(1, 0.5, 0, 1),#6 Orange
     Vec4(1, 0.25, 0, 1.0),#7 Red-Orange
     Vec4(1, 0, 0, 1),#8 Red
     Vec4(0.3, 0.3, 0.3, 1))#9 Grey
    healthGlowColors = (Vec4(0.25, 1, 0.25, 0.5),#Green
     Vec4(0.5, 1, 0.25, .5),#1 Green-Yellow
     Vec4(0.75, 1, 0.25, .5),#2 Yellow-Green
     Vec4(1, 1, 0.25, 0.5),#Yellow 
     Vec4(1, 0.866, 0.25, .5),#4 Yellow-Orange
     Vec4(1, 0.6, 0.25, .5),#5 Orange-Yellow
     Vec4(1, 0.5, 0.25, 0.5),#6 Orange
     Vec4(1, 0.25, 0.25, 0.5),#7 Red-Orange    
     Vec4(1, 0.25, 0.25, 0.5),#8 Red     
     Vec4(0.3, 0.3, 0.3, 0))#9 Grey
    
    def __init__(self, id):
        gui = loader.loadModel('phase_3.5/models/gui/battle_gui')
        DirectFrame.__init__(self, relief=None, image=gui.find('**/ToonBtl_Status_BG'), image_color=Vec4(0.5, 0.5, 0.5, 0.7))
        self.hpText = DirectLabel(parent=self, text='', pos=(-0.05, 0, -0.0356), text_scale=0.055)
        self.setScale(0.8)
        self.initialiseoptions(TownBattleCogPanel)
        self.levelText = DirectLabel(parent=self, text='', pos=(-0.06, 0, -0.075), text_scale=0.055)
        self.healthText = DirectLabel(parent=self, text='', pos=(0, 0, -0.075), text_scale=0.055)
        healthGUI = loader.loadModel('phase_3.5/models/gui/matching_game_gui')
        button = healthGUI.find('**/minnieCircle')
        button.setScale(0.5)
        button.setColor(Vec4(0, 1, 0, 1))
        button.setH(180)    
        self.healthNode = self.attachNewNode('health')
        self.healthNode.setPos(-0.065,0,0.055)
        glow = BattleProps.globalPropPool.getProp('glow')
        glow.reparentTo(button)
        glow.setScale(0.28)
        glow.setPos(-0.005, 0.01, 0.015)
        glow.setColor(Vec4(0.25, 1, 0.25, 0.5))
        self.button = button
        self.glow = glow
        self.head = None
        self.blinkTask = None
        button.reparentTo(self.healthNode)
        self.healthBar = None
        self.healthBarGlow = None
        self.hpChangeEvent = None
        self.blinkTask = None
        self.suit = None
        self.head = None
        self.maxHP = None
        self.currHP = None
        self.cog = None
        self.hpChangeEvent = None
        self.generateHealthBar()
        self.hide()
        healthGUI.removeNode()
        gui.removeNode()
        return
        
    def setSuit(self, suit):
        if self.suit == suit:
            messenger.send(self.suit.uniqueName('hpChange'))
            return
        self.suit = suit
        self.setLevelText(self.suit.getActualLevel())
        if self.head:
            self.head.removeNode()
        self.setSuitHead(self.suit.getStyleName())
        self.setMaxHp(self.suit.getMaxHP())
        self.setHp(self.suit.getHP())
        self.hpChangeEvent = self.suit.uniqueName('hpChange')
        if self.blinkTask:
            taskMgr.remove(self.blinkTask)
            self.blinkTask = None
        self.accept(self.hpChangeEvent, self.updateHealthBar)
        self.updateHealthBar()
        self.healthBar.show()
        
    def getSuit(self, suit):
        return self.suit

    def setCogInfo(self, cog):
        self.cog = cog
        self.updateHealthBar()
        if self.head:
            self.head.removeNode()
        
        self.head = self.attachNewNode('head')
        for part in cog.headParts:
            copyPart = part.copyTo(self.head)
            copyPart.setDepthTest(1)
            copyPart.setDepthWrite(1)

        p1, p2 = Point3(), Point3()
        self.head.calcTightBounds(p1, p2)
        d = p2 - p1
        biggest = max(d[0], d[1], d[2])
        s = 0.1 / biggest
        self.head.setPosHprScale(0.1, 0, 0.01, 180, 0, 0, s, s, s)
        self.setLevelText(cog.getActualLevel(), cog.getSkeleRevives())

    def setLevelText(self,health, revives = 0):
        if revives <= 0:
            self.healthText['text'] = TTLocalizer.DisguisePageCogLevel % str(hp)
        else:
            self.healthText['text'] = TTLocalizer.DisguisePageCogLevel % str(hp) + TTLocalizer.SkeleRevivePostFix


    def setSuitHead(self, suitName):
        self.head = Suit.attachSuitHead(self, suitName)
        self.head.setX(0.1)
        self.head.setZ(0.01)

    def generateHealthBar(self):
        model = loader.loadModel('phase_3.5/models/gui/matching_game_gui')
        button = model.find('**/minnieCircle')
        model.removeNode()
        button.setScale(0.5)
        button.setH(180.0)
        button.setColor(self.healthColors[0])
        button.reparentTo(self)
        button.setX(-0.08)
        button.setZ(0.02)
        self.healthBar = button
        glow = BattleProps.globalPropPool.getProp('glow')
        glow.reparentTo(self.healthBar)
        glow.setScale(0.28)
        glow.setPos(-0.005, 0.01, 0.015)
        glow.setColor(self.healthGlowColors[0])
        button.flattenLight()
        self.healthBarGlow = glow
        self.healthBar.hide()
        self.healthCondition = 0 

    def updateHealthBar(self):
        condition = self.cog.healthCondition
        if condition == 9:
            self.blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.75), Task.pause(0.1))
            taskMgr.add(self.blinkTask, self.uniqueName('blink-task'))
        elif condition == 10:
            taskMgr.remove(self.uniqueName('blink-task'))
            blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.25), Task(self.__blinkGray), Task.pause(0.1))
            taskMgr.add(blinkTask, self.uniqueName('blink-task'))
        else:
            taskMgr.remove(self.uniqueName('blink-task'))
            if not self.button.isEmpty():
                self.button.setColor(self.healthColors[condition], 1)
            
            if not self.glow.isEmpty():
                self.glow.setColor(self.healthGlowColors[condition], 1)
        self.hp = self.cog.getHP()
        self.maxHp = self.cog.getMaxHP()
        self.hpText['text'] = str(self.hp) + '/' + str(self.maxHp)

    def __blinkRed(self, task):
        if not self.blinkTask or not self.healthBar:
            return Task.done  
        self.healthBar.setColor(self.healthColors[8], 1)
        self.healthBarGlow.setColor(self.healthGlowColors[8], 1)
        if self.healthCondition == 7:
            self.healthBar.setScale(1.17)
        return Task.done

    def __blinkGray(self, task):
        if not self.blinkTask or not self.healthBar:
            return Task.done
        self.healthBar.setColor(self.healthColors[9], 1)
        self.healthBarGlow.setColor(self.healthGlowColors[9], 1)
        if self.healthCondition == 10:
            self.healthBar.setScale(1.0)
        return Task.done

    def removeHealthBar(self):
        if self.healthCondition == 9 or self.healthCondition == 10:
            if self.blinkTask:
                taskMgr.remove(self.blinkTask)
                self.blinkTask = None    
        if self.healthBar:
            self.healthBar.removeNode()
            self.healthBar = None
        self.healthCondition = 0
        return
        
    def getDisplayedCurrHp(self):
        return self.currHP
        
    def getDisplayedMaxHp(self):
        return self.maxHP   

    def setMaxHp(self, hp):
        self.maxHP = hp

    def setHp(self, hp):
        self.currHP = hp

    def show(self):
        if self.cog:
            self.updateHealthBar()
        self['image_color'] = Vec4(0.7, 0.7, 0.7, 0.7)
        self.hidden = False
        self.healthNode.show()
        self.button.show()
        self.glow.show()
        DirectFrame.show(self)

    def unload(self):
        self.exit()
        del self.hpText
        del self.cog
        del self.glow
        del self.button
        del self.blinkTask
        DirectFrame.destroy(self)

        
    def cleanup(self):
        self.ignoreAll()
        self.removeHealthBar()
        if self.head is not None:
            self.head.removeNode()
        del self.head
        self.levelText.destroy()
        del self.levelText
        del self.healthBar
        if self.healthBarGlow is not None:
            self.healthBarGlow.removeNode()
        del self.healthBarGlow
        del self.suit
        del self.maxHP
        del self.currHP
       
        if self.blinkTask:
            taskMgr.remove(self.blinkTask)
            self.blinkTask = None
        
        del self.blinkTask
        self.healthNode.removeNode()
        self.button.removeNode()
        self.glow.removeNode()
        DirectFrame.destroy(self)
