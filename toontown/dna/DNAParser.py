from direct.stdpy import threading

import libpandadna

class DNABulkLoader:
    def __init__(self, storage, files):
        self.dnaStorage = storage
        self.dnaFiles = files

    def loadDNAFiles(self):
        for file in self.dnaFiles:
            print('Reading DNA file...', file)
            loadDNABulk(self.dnaStorage, file)
        del self.dnaStorage
        del self.dnaFiles

def loadDNABulk(dnaStorage, file):
    if __debug__:
        file = '../resources/' + file
    else:
        file = '/' + file
    libpandadna.loadDNAFile(dnaStorage, file)

def loadDNAFile(dnaStorage, file):
    print('Reading DNA file...', file)
    if __debug__:
        file = '../resources/' + file
    else:
        file = '/' + file
    node = libpandadna.loadDNAFile(dnaStorage, file)
    return node

def loadDNAFileAI(dnaStorage, file):
    if __debug__:
        file = '../resources/' + file
    else:
        file = '/' + file
    data = libpandadna.loadDNAFileAI(dnaStorage, file)
    return data
