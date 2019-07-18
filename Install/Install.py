import os

SourcePath = '../Source'
ModulesPath = '../Modules'

def Install ():
    Source = [Item for Item in os.listdir (SourcePath)]
    Modules = [Module for Module in os.listdir (ModulesPath)]

Install ()
