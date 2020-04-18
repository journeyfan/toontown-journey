from toontown.toonbase import ToontownGlobals
from . import SellbotLegFactorySpec
from . import SellbotLegFactoryCogs
from . import LawbotLegFactorySpec
from . import LawbotLegFactoryCogs

def getFactorySpecModule(factoryId):
    return FactorySpecModules[factoryId]


def getCogSpecModule(factoryId):
    return CogSpecModules[factoryId]


FactorySpecModules = {ToontownGlobals.SellbotFactoryInt: SellbotLegFactorySpec,
 ToontownGlobals.LawbotOfficeInt: LawbotLegFactorySpec}
CogSpecModules = {ToontownGlobals.SellbotFactoryInt: SellbotLegFactoryCogs,
 ToontownGlobals.LawbotOfficeInt: LawbotLegFactoryCogs}

if config.GetBool('want-brutal-factory', True):
    from . import SellbotBrutalLegFactorySpec
    from . import SellbotBrutalLegFactoryCogs
    FactorySpecModules[ToontownGlobals.SellbotBrutalFactoryInt] = SellbotBrutalLegFactorySpec
    CogSpecModules[ToontownGlobals.SellbotBrutalFactoryInt] = SellbotBrutalLegFactoryCogs
 
if __dev__:
    from . import FactoryMockupSpec
    FactorySpecModules[ToontownGlobals.MockupFactoryId] = FactoryMockupSpec
    from . import FactoryMockupCogs
    CogSpecModules[ToontownGlobals.MockupFactoryId] = FactoryMockupCogs
