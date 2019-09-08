import inspect
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
    frameinfo = inspect.currentframe()
    tabs = '\t'*nFolders
    eq = delim*20
    print(f'{tabs}{eq} {fname}: {frameinfo.f_back.f_lineno} {eq}')
    return frameinfo.f_back.f_lineno

debug_print(__file__)
