from pandac.PandaModules import NodePath

from toontown.shtiker.CogMenuBar import CogMenuBar


class CogMenu(NodePath):
    def __init__(self):
        NodePath.__init__(self, 'CogMenu')

        self.sellbotBar = CogMenuBar(self, 's')
        self.cashbotBar = CogMenuBar(self, 'm')
        self.lawbotBar = CogMenuBar(self, 'l')
        self.bossbotBar = CogMenuBar(self, 'c')
        self.secbotBar = CogMenuBar(self, 'y')

        self.sellbotBar.setX(-0.502)
        self.lawbotBar.setX(0.502)
        self.bossbotBar.setX(1)
        self.secbotBar.setX(1.502)

    def update(self):
        self.sellbotBar.update()
        self.cashbotBar.update()
        self.lawbotBar.update()
        self.bossbotBar.update()
        self.secbotBar.update()

    def cleanup(self):
        self.sellbotBar.cleanup()
        self.cashbotBar.cleanup()
        self.lawbotBar.cleanup()
        self.bossbotBar.cleanup()
        self.secbotBar.cleanup()
        self.removeNode()
