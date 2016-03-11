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
print "Finished importing Classes!"
from visual import *
print "Finished importing VPython!"
from time import sleep
print "Finished importing sleep from time!"

def main():

    #lists for VPython objects
    brushes = [] #brushes
    actors  = [] #actors

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

    #Starts the new game
    Thegame = C.Game(firstlvl)

    #Starts tickloop of new game
    Thegame.Tick()

    #renders each brush in the window
    for w in Thegame.brushlist:
        brushes.append(box(pos=(w.x, w.z, w.y), length=(w.breadth), width=(w.width), height=(w.height), color=color.orange))

    #renders each actor in the window every tick
    while True:
        for w in Thegame.actorlist:
            actors.append(sphere(pos=(w.x, w.z, w,y)))
            sleep(1/30)

if __name__ == "__main__":
    main()