from . import ClothesGUI
from toontown.toon import ToonDNA

class MakeClothesGUI(ClothesGUI.ClothesGUI):
    notify = directNotify.newCategory('MakeClothesGUI')

    def __init__(self, doneEvent):
        ClothesGUI.ClothesGUI.__init__(self, ClothesGUI.CLOTHES_MAKETOON, doneEvent)

    def setupScrollInterface(self):
        self.dna = self.toon.getStyle()
        gender = self.dna.getGender()
        if gender != self.gender:
            # Tops still needed for shuffle
            self.tops = ToonDNA.getRandomizedTops(gender, tailorId=ToonDNA.MAKE_A_TOON)
            self.bottoms = ToonDNA.getRandomizedBottoms(gender, tailorId=ToonDNA.MAKE_A_TOON)

            self.topStyles = ToonDNA.getTopStyles(gender, tailorId=ToonDNA.MAKE_A_TOON)
            self.botStyles = ToonDNA.getBotStyles(gender, tailorId=ToonDNA.MAKE_A_TOON)

            self.gender = gender
            self.topChoice = 0
            self.topStyleChoice = 0
            self.topColorChoice = 0
            self.bottomChoice = 0
            self.botStyleChoice = -1
            self.botColorChoice = 0
        self.setupButtons()

    def setupButtons(self):
        ClothesGUI.ClothesGUI.setupButtons(self)
        if len(self.dna.torso) == 1:
            if self.gender == 'm':
                torsoStyle = 's'
            elif self.girlInShorts == 1:
                torsoStyle = 's'
            else:
                torsoStyle = 'd'
            self.toon.swapToonTorso(self.dna.torso[0] + torsoStyle)
            self.toon.loop('neutral', 0)
            self.toon.swapToonColor(self.dna)
            self.swapTop(0)
            self.swapBottom(0)
        return None
