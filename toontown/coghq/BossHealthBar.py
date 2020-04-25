from toontown.toonbase import TTLocalizer
from toontown.toonbase.ToontownGlobals import *
from direct.gui.DirectGui import *
from panda3d.core import *
from toontown.suit.Suit import *
from direct.task.Task import Task
import math
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *

class BossHealthBar:
    def __init__(self):

        notify = DirectNotifyGlobal.directNotify.newCategory('BossHealthBar')
        #self.bossBarStartPosZ = 1.5 #for the frame when we implement it
       # self.bossBarEndPosZ = 0.88
        self.bossBar = DirectWaitBar(relief=DGG.SUNKEN, scale=(0.197, 0, 0.135), value = 100, pos=(0.0, 0, 0.94), frameSize=(-2.0,2.0, -0.2, 0.2), borderWidth=(0.02, 0.02), range=100, sortOrder=50, frameColor=(0.5, 0.5, 0.5, 0.6), barColor=(0.75, 0.75, 1.0, 0.7), text='0 / 0',text_scale=(0.35, 0.4), text_fg=(1,1,1,1), text_align=TextNode.ACenter, text_pos=(0, -0.13), text_shadow=(0, 0, 0, 1))
        self.bossBar.hide()
        self.healthCondition = 0
        self.currentHealth = 0
        self.newHealth = 0
        self.maxHealth = 0
        self.healthRatio = 0
        self.isUpdating = False
        self.isBlinking = False
        self.bossBarColors = (Vec4(0, 1, 0, 0.8),
                              Vec4(1, 1, 0, 0.8),
                              Vec4(1, 0.5, 0, 0.8),
                              Vec4(1, 0, 0, 0.8),
                              Vec4(0.3, 0.3, 0.3, 0.8))
        
        self.colorThresholds = (0.65, 0.4, 0.2, 0.1, 0.5)
        return
    
    def start(self, health, maxHealth):
        self.maxHealth = maxHealth
        self.newHealth = health
        self.currentHealth = health 
        self.bossBar['text'] = ('{0} / {1}'.format(str(health), str(maxHealth)))
        self.bossBar['range'] = maxHealth
        self.bossBar['value'] = health
        self.__checkUpdateColor(health, maxHealth)
        self.bossBar.show()

    def update(self, health, maxHealth):
        if self.isUpdating:
            taskMgr.remove('bar-smooth-update-task')
            self.isUpdating = False
        self.newHealth = health
        if self.newhealth < 0:
            self.newhealth = 0
        if self.maxHealth != 0:
            if self.currentHealth != self.newHealth:
                smoothUpdateTask = Task.loop(Task(self.__smoothUpdate), Task.pause(0.01))
                taskMgr.add(smoothUpdateTask, 'bar-smooth-update-task')
                self.isUpdating = True

    def __checkUpdateColor(self, health, maxHealth):
        if self.bossBar:
            self.healthRatio = float(health) / float(maxHealth)
        if self.healthRatio > self.colorThresholds[0]:
            condition = 0
        elif self.healthRatio > self.colorThresholds[1]:
            condition = 1
        elif self.healthRatio > self.colorThresholds[2]:
            condition = 2
        elif self.healthRatio > self.colorThresholds[3]:
            condition = 3
        elif self.healthRatio > self.colorThresholds[4]:
            condition = 4
        else:
            condition = 5
        self.__applyNewColor(condition)
        if self.healthCondition != condition:
            if condition == 4:
                if self.healthCondition == 5:
                    taskMgr.remove('bar-blink-task')
                    self.isBlinking = False
                blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.75), Task(self.__blinkGray), Task.pause(0.1))
                taskMgr.add(blinkTask, 'bar-blink-task')
                self.isBlinking = True 
            elif condition == 5:
                if self.healthCondition == 4:
                    taskMgr.remove('bar-blink-task')
                    self.isBlinking =False
                blinkTask = Task.loop(Task(self.__blinkRed), Task.pause(0.25), Task(self.__blinkGray), Task.pause(0.1))
                taskMgr.add(blinkTask, 'bar-blink-task')
                self.isBlinking = True

            else:
                if self.isBlinking:
                    taskMgr.remove('bar-blink-task')
                    self.isBlinking = False
            self.healthCondition = condition

    def __blinkRed(self, task):
        if self.bossBar:
            self.bossBar['barColor'] = self.bossBarColors[3]
            return Task.done
        else:
            taskMgr.remove('bar-blink-task')
    
    def __applyNewColor(self, currentColor):
        if self.bossBar:
            if currentColor != 3 and currentColor !=4 and currentColor !=5:
                if self.healthRatio > self.colorThresholds[0]:
                    condition = 0
                elif self.healthRatio > self.colorThresholds[1]:
                    condition = 1
                elif self.healthRatio > self.colorThresholds[2]:
                    condition = 2
                if condition > 0:
                    numeratorRatioAmount = self.colorThresholds[condition - 1]
                else:
                    numeratorRatioAmount = 1
                denominatorRatioAmount = self.colorThresholds[condition]
                numeratorColorAmount = self.bossBarColors[condition]
                denominatorColorAmount = self.bossBarColors[condition + 1]
                currentRatioAmount =numeratorRatioAmount - self.healthRatio
                totalRatioAmount = numeratorRatioAmount - denominatorRatioAmount
                ratioRatio = currentRatioAmount / totalRatioAmount
                differenceColorAmount = denominatorColorAmount - numeratorColorAmount
                ratioColorToAdd = differenceColorAmount * ratioRatio
                totalColorAmount = self.bossBarColors[condition] + ratioColorToAdd
                self.bossBar['barColor'] = totalColorAmount 

    def __blinkGray(self, task):
        if self.bossBar:
            self.bossBar['barColor'] = self.bossBarColors[4]
            return Task.done
        else:
            taskMgr.remove('bar-blink-task')

    def cleanup(self):
        if self.bossBar:
            if self.isUpdating:
                taskMgr.remove('bar-smooth-update-task')

            self.bossBar.destroy()
            self.bossBar = None
            taskMgr.remove('blink-task')
            if self.isBlinking:
                taskMgr.remove('bar-blink-task')
            self.healthCondition = 0 

    def __smoothUpdate(self, task):
        if self.bossBar:
            if self.currentHealth != self.newHealth:
                posOrNeg = self.currentHealth = self.newHealth
                if posOrNeg > 0:
                    if posOrNeg == 1:

                        self.currentHealth -= 1
                    else:
                        self.currentHealth -= 2
                elif posOrNeg < 0:
                    if posOrNeg == -1:

                        self.currentHealth += 1
                    else:
                        self.currentHealth += 2
                
                self.bossBar['text'] = ('{0} / {1}'.format(str(self.currentHealth), str(self.maxHealth)))
                self.bossBar['value'] = self.currentHealth
                self.__checkUpdateColor(self.currentHealth, self.maxHealth)
            elif self.currentHealth == newHealth:
                self.isUpdating = False
                taskMgr.remove('bar-smooth-update-task')
            return Task.done