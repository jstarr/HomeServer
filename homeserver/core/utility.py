from inspect import currentframe
# import os

topDir = 'HomeServer'


def debug_print(callingFile, delim='='):
    tabs = 0
    fname = callingFile
    nFolders = 0
    if (callingFile):
        homeLoc = callingFile.find(topDir) + len(topDir) + 1
        fname = callingFile[homeLoc:]
        nFolders = fname.count('/')
    frameinfo = currentframe()
    tabs = '\t'*nFolders
    eq = delim*20
    print(f'{tabs}{eq} {fname}: {frameinfo.f_back.f_lineno} {eq}')


debug_print(__file__)
