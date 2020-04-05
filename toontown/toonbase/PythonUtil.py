from direct.showbase.PythonUtil import *
from direct.showbase import DConfig

# __dev__ is not defined at import time, call this after it's defined
def recordFunctorCreationStacks():
    global Functor
    config = DConfig
    # off by default, very slow
    if __dev__ and config.GetBool('record-functor-creation-stacks', 0):
        if not hasattr(Functor, '_functorCreationStacksRecorded'):
            Functor = recordCreationStackStr(Functor)
            Functor._functorCreationStacksRecorded = True
            Functor.__call__ = Functor._exceptionLoggedCreationStack__call__

# like recordCreationStack but stores the stack as a compact stack list-of-strings
# scales well for memory usage
def recordCreationStackStr(cls):
    if not hasattr(cls, '__init__'):
        raise 'recordCreationStackStr: class \'%s\' must define __init__' % cls.__name__
    cls.__moved_init__ = cls.__init__
    def __recordCreationStackStr_init__(self, *args, **kArgs):
        # store as list of strings to conserve memory
        self._creationStackTraceStrLst = StackTrace(start=1).compact().split(',')
        return self.__moved_init__(*args, **kArgs)
    def getCreationStackTraceCompactStr(self):
        return ','.join(self._creationStackTraceStrLst)
    def printCreationStackTrace(self):
        print ','.join(self._creationStackTraceStrLst)
    cls.__init__ = __recordCreationStackStr_init__
    cls.getCreationStackTraceCompactStr = getCreationStackTraceCompactStr
    cls.printCreationStackTrace = printCreationStackTrace
    return cls