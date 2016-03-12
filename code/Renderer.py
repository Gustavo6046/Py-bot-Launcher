from time import sleep
import Classes as C
from visual import *
C.logandprint("Finished importing VPython!")

class baseRendererClass(object):
    pass

class RendererBrush(baseRendererClass):
    def __init__(self, corrbrush, corrbox):
        self.brush = corrbrush
        self.box = corrbox

    def Tick(self):
        renderx, rendery, renderz = self.brush.x, self.brush.y, self.brush.z
        corrbox.pos = (renderx, renderz, rendery)
        corrbox.width, corrbox.lenght, corrbox.height = self.brush.breadth, self.brush.width, self.brush.height

class RendererActor(baseRendererClass):
    def __init__(self, corractor, corrsphere):
        self.actor = corractor
        self.sphere = corrsphere

    def Tick(self):
        renderx, rendery, renderz = self.actor.location.x, self.actor.location.y, self.actor.location.z
        corrsphere.pos = (renderx, renderz, rendery)

class GameRender(object):
    #VPython lists of RendererActors and RendererBrushes for rendering them
    renderedactors  = [] #actors
    renderedbrushes = [] #brushes

    #adds actor to render
    def addactor(self, actorname):
        self.renderedactors.append(RendererActor(actorname,\
        sphere(pos=(actorname.location.x, actorname.location.z, actorname.location.y), radius=24, color=color.blue)))

    #adds brush to render
    def addbrush(self, brushname):
        self.renderedbrushes.append (RendererBrush(brushname,\
        box(pos=(brushname.x + (brushname.width / 2.0), brushname.z + (brushname.height / 2.0), brushname.y + (brushname.breadth / 2.0)),\
        lenght=brushname.width, height=brushname.height, width=brushname.breadth, color=color.blue)))
        if isinstance(brushname, C.TriggerBrush):
            self.renderedbrushes[len(self.renderedbrushes) - 1].brush.color = color.orange

    #tick
    def render(self):
        for w in self.renderedactors:
            w.tick()
        for w in self.renderedbrushes:
            w.tick()