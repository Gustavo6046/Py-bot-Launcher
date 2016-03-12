#-------------------------------------------------------------------------------
# Name:        PyBotLauncher
# Purpose:     Zero-player game where bots fights monsters
#
# Author:      Gustavo Ramos "Gustavo6046" Rehermann
#
# Created:     09/03/2016
# Copyright:   (c) Gustavo Ramos "Gustavo6046" Rehermann, 2016
# Licence:     CC-BY-SA
#-------------------------------------------------------------------------------

import Classes as C
C.logandprint("Finished importing Classes!")
from time import sleep
C.logandprint("Finished importing sleep from time!")
import Renderer as R
C.logandprint("Finished importing the VPython renderer!")

def main():
    GameStarter = StartGame()

class StartGame():

    def __init__(self):
        C.logandprint("Started initialization!")

        #defines what characters define comments
        commentchars = [";", "$", "#", "/", "!", "@"]

        #opens the config file about the maps
        firstmap = open("..\\config\\firstmap.txt", "r")

        #Filters comments from the first line and gets the map's name
        firstlvl = firstmap.readline()
        if commentchars.__contains__(firstlvl[1]):
            firstlvl = firstmap.readline()
        if firstlvl[len(firstlvl)-2:] == "\n":
            firstlvl = firstlvl[:-2]

        #Starts renderer
        self.renderer = R.GameRender()

        #Starts the new game
        Thegame = C.Game(firstlvl, self)

        #adds brushes and actors to it
        for x in Thegame.actorlist:
            renderer.addactor(x)
        for y in Thegame.brushlist:
            renderer.addbrush(y)

        #starts tickloop of renderer
        renderer.render()

        C.logandprint("Finished initialization!\n=========================\nStarted game tickloop")
        #Starts tickloop of new game
        Thegame.Tick()

if __name__ == "__main__":
    main()