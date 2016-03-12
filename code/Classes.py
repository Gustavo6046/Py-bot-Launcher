from time import sleep, strftime
from random import choice
from math import sqrt
from datetime import datetime

if __name__ == "__main__":
    clearfile = open("..\\log.txt", "w")
    clearfile.write("")
    clearfile.close()

def logandprint(logging):
    if not isinstance(logging, str):
        return False

    print logging
    return logtext(logging)

def logtext(logging):
    dt = datetime.now()
    logging = "[" + strftime("%H:%M:%S.") + str(dt.microsecond) + "] " + logging
    if not isinstance(logging, str):
        return False
    logtxt = open("..\log.txt", "a")
    logtxt.write(logging + "\n")
    logtxt.close()
    return True

logandprint("Finished importing sqrt from math!")

#=================#
# Project Classes #
#=================#

# Brush class (just because)
class NormalBrush(object):

    disttotarget = 0

    def __init__(self, x, y, z, width, height, breadth, tag, owner):
        self.position, self.x, self.y, self.z, self.width, self.height, self.breadth, self.owner = Vector(x, y, z), float(x), float(y), float(z), float(width), float(height), float(breadth), owner
        self.targetpos, self.initpos = self.position, self.position

    def tick(self):
        self.x, self.y, self.z = self.position.x, self.position.y, self.position.z
        if self.position.unwrap() == self.targetpos.unwrap():
            disttotarget = 0
            self.initpos = self.position
        else:
            disttotarget += 1
            self.position = self.position.move_towards(self.targetpos, self.position.distance_to(self.targetpos) / disttotarget)

    def HasCoordinate(self, x, y, z):
        return x > self.x and x < self.width + self.x and y < self.y and\
     y > self.y + self.breadth and z > self.z and z < self.z + self.height

    def Touch(self, Other):
        pass

    def trigger(self, instigator):
        pass

class TriggerBrush(NormalBrush):

    tickwait = -1

    def __init__(self, x, y, z, width, height, breadth, tag, target, event, callevent, owner):
        super(TriggerBrush, self).__init__(x, y, z, width, height, breadth, tag, owner)
        self.target, self.event, self.callevent = target, event, callevent
        if not isinstance(target, Vector):
            logandprint("Warning: Invalid type for target!")
            target = self.position
        if not isinstance(callevent, bool):
            raise TypeError
        self.target2 = self.position

    def Touch(self, Other):
        self.targetpos = self.target
        self.toucher = Other

    def trigger(self, instigator):
        self.Touch(self, instigator)

    def tick(self):
        super(TriggerBrush, self)
        if self.position.unwrap() == self.target.unwrap():
            if tickwait == -1:
                tickwait = 121
                if self.Toucher != None:
                    self.owner.Event(self, self.toucher)
                self.toucher = None
            tickwait -= 1
            if tickwait < 1:
                tickwait = -1
                self.targetpos = self.target2



#==========================
# Math Classes

class Vector(object):
    def __init__(self, x, y, z):
        self.x, self.y, self.z = float(x), float(y), float(z)

    def unwrap(self):
        return [self.x, self.y, self.z]

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other, self.z * other)

    def __div__(self, other):
        return Vector(self.x / other, self.y / other, self.z / other)

    def __pow__(self, other):
        return Vector(self.x ** other, self.y ** other, self.z ** other)

    def move_towards(self, other, fraction):
        return self + ((other - self) / float(fraction))

    def __float__(self):
        return (self.x + self.y + self.z) / 3

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def distance_to(self, other):
        return sqrt(self.dot_product(other))

#==========================
# Main Classes

class Game(object):

    brushlist = []
    actorlist = []
    commentchars = ["#", ";", "/", "$"]

    def Event(self, event, instigator, triggerer):
        for x in brushlist:
            if x.tag == event:
                x.trigger(instigator, triggerer)

        for xx in actorlist:
            if x.tag == event:
                x.trigger()

    def Touching(self, x, y, z):
        for w in self.brushlist:
            if w.HasCoordinate(x, y, z):
                return True
        return False

    def __init__(self, mapname, owner):

        self.owner = owner

        mapfile = open("..\\maps\\" + mapname + ".blm", "r")

        for mapparseline in mapfile:
            mapparseline = mapparseline.rstrip()
            mapparsecode = mapparseline.split(" ")

            if not mapparsecode[0][:1] in self.commentchars:
                logandprint("Parsing map line: \"" + mapparseline + "\"")

            if mapparsecode[0] == "brush":
                if mapparsecode[1] == "normal":

                    #next line TL;DR: grab all values from the map's line
                    bx, by, bz, bwidth, bbreadth, bheight, tag = float(mapparsecode[2]), float(mapparsecode[3]), float(mapparsecode[4]), float(mapparsecode[5]), float(mapparsecode[6]), float(mapparsecode[7]), mapparsecode[8]

                    self.brushlist.append(NormalBrush(bx, by, bz, bwidth, bheight, bbreadth, tag, self))

                elif mapparsecode[1] == "moving":
                    bx, by, bz, bwidth, bbreadth,  bheight, tag, targetx, targety, targetz, event, callevent = float(mapparsecode[2]), float(mapparsecode[3]), float(mapparsecode[4]), float(mapparsecode[5]), float(mapparsecode[6]), float(mapparsecode[7]), mapparsecode[8], float(mapparsecode[9]), float(mapparsecode[10]), float(mapparsecode[11]), mapparsecode[12], bool(mapparsecode[13])

                    self.brushlist.append(TriggerBrush(bx, by, bz, bwidth, bheight, bbreadth, tag, Vector(targetx, targety, targetz),\
                    event, callevent, self))

            elif mapparsecode[0] == "gravity":
                self.gravity = float(mapparsecode[1])

            elif mapparsecode[0] == "actor":
                if mapparsecode[1] == "endmap":
                    x, y, z, name, tag, lvlname, radius, height = float(mapparsecode[2]), float(mapparsecode[3]), float(mapparsecode[4]), mapparsecode[5], mapparsecode[6], mapparsecode[7], float(mapparsecode[8]), float(mapparsecode[9])

                    self.actorlist.append(LevelTransition(x, y, z, name, tag, lvlname, radius, height, self))
                elif mapparsecode[1] == "monster":
                    x. y. z. health, name, armor, tag, pitch, yaw, roll, event, projdmg, projradius, projspeed= float(mapparsecode[2]), float(mapparsecode[3]), float(mapparsecode[4]), float(mapparsecode[5]), mapparsecode[6], float(mapparsecode[7]), mapparsecode[8], float(mapparsecode[9]), float(mapparsecode[10]), float(mapparsecode[11]), float(mapparsecode[12]), float(mapparsecode[12]), float(mapparsecode[13])

                    self.actorlist.append(Monster(x, y, z, health, name, armor, tag, self, event, pitch, yaw, roll, projdmg, projradius, projspeed) )
                elif mapparsecode[1] == "botnode":
                    if mapparsecode[2] == "startpoint":
                        x, y, z, name, pitch, yaw, roll = float(mapparsecode[3]), float(mapparsecode[4]), float(mapparsecode[5]), mapparsecode[6], float(mapparsecode[7]), float(mapparsecode[8]), float(mapparsecode[9])

                        self.actorlist.append(StartPoint(x, y, z, name, self, pitch, yaw, roll))

                    elif mapparsecode[2] == "normal":
                        x, y, z, name = float(mapparsecode[3]), float(mapparsecode[4]), float(mapparsecode[5]), mapparsecode[6]

                        self.actorlist.append(NavigationPoint(x, y, z, name, self))

                    elif mapparsecode[2] == "target":
                        x, y, z, name = float(mapparsecode[3]), float(mapparsecode[4]), float(mapparsecode[5]), mapparsecode[6]

                        self.actorlist.append(TargetPoint(x, y, z, name. self))

                elif mapparsecode[1] == "health":

                    x, y, z, name, amount = float(mapparsecode[2]), float(mapparsecode[3]), float(mapparsecode[4]),mapparsecode[5], float(mapparsecode[6])

                    self.actorlist.append(HealthInventory(x, y, z, name, amount, self))

                elif mapparsecode[1] == "weapon":

                    x, y, z, name, rating, firerate, projspeed, projdamage, projradius = float(mapparsecode[2]), float(mapparsecode[3]), float(mapparsecode[4]), mapparsecode[5], float(mapparsecode[6]), float(mapparsecode[7]), float(mapparsecode[8]), float(mapparsecode[9]), float(mapparsecode[10])

                    self.actorlist.append(WeaponInventory(x, y, z, name, rating, firerate, projspeed, projdamage, projradius, self))

                elif mapparsecode[1] == "bot":

                    x, y, z, health, name, armor, tag = float(mapparsecode[2]), float(mapparsecode[3]), float(mapparsecode[4]), float(mapparsecode[5]), mapparsecode[6], float(mapparsecode[7]), mapparsecode[8]

                    self.actorlist.append(Bot(x, y, z, health, name, armor, tag, self))

            elif not mapparsecode[0][:1] in self.commentchars:
                logandprint("Invalid map statement: " + mapparsecode[0])

        if not hasattr(self, 'gravity'):
            logandprint("Map missing gravity! Setting to default (80)...")
            self.gravity = 80

        logandprint("Calculating NavigationPoint reachspecs...")

        for x in self.actorlist:
            if issubclass(type(x), NavigationPoint) or isinstance(x, NavigationPoint):
                x.PostInitialization()

        logandprint("Adding brushes to renderer....")
        for x in self.brushlist:
            self.owner.renderer.addbrush(x)

    def Tick(self):
        logandprint("Started tickloop!")
        while True:
            sleep(1/30)
            self.owner.renderer.render()
            for x in self.actorlist:
                x.tick()
            for x in self.brushlist:
                x.tick()
            for y in self.actorlist:
                hasactor = False
                for x in self.owner.renderer.renderedactors:
                    if x.actor == y:
                        hasactor = True
                if not hasactor:
                    self.owner.renderer.addactor(y)
            for x in self.owner.renderer.renderedactors:
                if not x.actor in self.actorlist:
                    del x


class Actor(object):

    def LineOfSightTo(self, Actor2):
            if not ( isinstance(Actor2, Actor) or issubclass(Type(Actor2), Actor) ):
                raise TypeError("Invalid types for execution of line of sight check!")

            currentpos = self.location

            if Actor2 is self:
                logtext("Warning: " + self.name + " tried to check line of sight to self!")
                return False

            if self.location == Actor2.location:
                return True

            logtext("   :" + self.name + " is detecting line of sight to " + Actor2.name)

            portion = 0

            while not self.owner.Touching(currentpos.x, currentpos.y, currentpos.z):

                portion += 1

                logtext("       -checked x=" + str(currentpos.x) + " y=" + str(currentpos.y) + " z=" + str(currentpos.z))
                currentpos = currentpos.move_towards(Actor2.location, self.location.distance_to(Actor2.location) / (portion * 1.5))

                if currentpos.unwrap() == Actor2.location.unwrap():
                    return True

                sleep(1/500)

            return False

    def __init__(self, x, y, z, name, owner, pitch = 0, yaw = 0, roll = 0):
        self.x, self.y, self.z, self.name, self.owner,self.pitch, self.yaw, self.roll =\
        x, y, z, name, owner, pitch, yaw, roll
        self.location = Vector(x, y, z)

    def DistanceToActor(self, actor2):
        assert isinstance(actor2, Actor) or issubclass(type(actor2, Actor))

        return self.location.distance_to(actor2.location)

    def tick(self):
        self.x, self.y, self.z = self.location.unwrap()[0], self.location.unwrap()[1], self.location.unwrap()[2]

    def Trigger(self, eventinstigator, eventcaller):
        pass

class LevelTransition(Actor):

    def __init__(self, x, y, z, name, tag, lvlname, radius, height, owner):
        self.x, self.y, self.z, self.name, self.tag, self.lvlname, self.radius, self.height, self.owner = x, y, z, name, tag, lvlname, radius, height, owner

    def triggered():
        del self.owner
        owner = Game(self.lvlname)


#================
# Navigation Points
#
# Common Function Descriptions:
#
# 1. SpecialHandling: Returns the next node the bot should
#    navigate to after finding this one.
#
# 2. PostInitialization: Called after the actor list's navigation nodes
#    have been constructed.

class NavigationPoint(Actor):
    ConnectedNodes = []

    def GetPathToActor(TheActor, MaxDist = 256, PreviousNodes = []):
        path = []

        if not isinstance(TheActor, Actor) or issubclass(type(TheActor, Actor)):
            return []

        for w in ConnectedNodes:
            if w in PreviousNodes:
                continue
            PreviousNodes.append(w)
            if w.DistanceToActor(TheActor) < MaxDist:
                return PreviousNodes
            else:
                path = w.GetPathToActor(TheActor, MaxDist, PreviousNodes)
        if path != None and path != []:
            return path
        return None

    def GetPathToTarget(PreviousNodes = []):
        path = []

        for w in ConnectedNodes:
            if w in PreviousNodes:
                continue
            PreviousNodes.append(w)
            if isinstance(w, TargetPoint):
                return PreviousNodes
            else:
                curpath = w.GetPathToTarget(PreviousNodes)
                if curpath != None and len(curpath) < len(path):
                    path = curpath
        if path != []:
            return path
        return None

    def SpecialHandling(self, Navigator):
        return Navigator.GetNextNavigationPoint(self)

    def PostInitialization(self):
        for x in self.owner.actorlist:
            if not ( isinstance(x, NavigationPoint) and issubclass(type(x), NavigationPoint) ):
                continue
            if self.LineOfSightTo(x) and x.z - self.z < 70 and not x is self:
                self.ConnectedNodes.append(x)

class TargetPoint(NavigationPoint):
    def SpecialHandling(self, Navigator):
        return self

class StartPoint(NavigationPoint):

    def SpecialHandling(self, Navigator):
        return choice(self.ConnectedNodes)
#================
# Projectiles

class Projectile(Actor):
    def __init__(self, x, y, z, name, owner, targetloc, speed, damage, radius, shooter):
        self.location, self.x, self.y, self.z, self.name, self.owner, self.targetloc, self.speed, self.damage, self.explradius, self.shooter = Vector(x, y, z), x, y, z, name, owner, targetloc, pitch, yaw, roll, speed, damage, radius

        self.initlocation = self.location

    def tick(self):
        self.location.move_toward(self.targetloc, self.initlocation.distance_to(self.targetloc) / self.speed)
        touched = False

        for w in self.owner.brushlist:
            if w.HasCoordinate(self.location.x, self.location.y, self.location.z):
                touched = True

        if self.location == self.targetloc or touched:
            for w in self.owner.actorlist:
                if DistanceToActor(w) < self.explradius and isinstance(w, Pawn) or issubclass(type(w), Pawn):
                    w.TakeDamage()

#================
# Inventory classes

class Inventory(Actor):
    collected = None

    def __init__(self, x, y, z, name, amount, owner, pitch=0, yaw=0, roll=0):
        self.x, self.y, self.z, self.name, self.amount, self.owner, self.pitch, self.yaw, self.roll = x, y, z, name, amount, owner, pitch, yaw, roll
        self.location = Vector(x, y, z)

    def Collected(self, owner):
        if isinstance(owner, Pawn) or issubclass(type(owner, Pawn)):
            self.collected = owner

    def tick(self):
        if self.collected != None:
            self.x, self.y, self.z = self.collected.x, self.collected.y, self.collected.z

class HealthInventory(Inventory):
    def Collected(self, owner):
        if isinstance(owner, Pawn) or issubclass(type(owner, Pawn)):
            owner.GiveHealth(amount, self)

class WeaponInventory(Inventory):
    currdelay = 0

    def __init__(self, x, y, z, name, rating, firerate, projspeed, projdamage, projexplradius, owner):
        self.location, self.x, self.y, self.z, self.name, self.rating, self.firerate, self.owner, self.projspeed, self.projdamage, self.projexplradius = Vector(x, y, z), x, y, z, name, rating, firerate, owner, projspeed, projdamage, projexplradius

    def Collected(self, owner):
        if isinstance(owner, Pawn) or issubclass(type(owner, Pawn)):
            self.collected = owner
            owner.inventory.append(self)
            self.weapowner = owner

    def FireProjectile(self, targetlocation):
        if currdelay > 0:
            return
        self.owner.actorlist.append(Projectile(self.x, self.y, self.z, "Weapon " + str(self.name) + "'s projectile", self.owner, targetlocation, self.projspeed, self.projdamage, self.projexplradius))
        currdelay = firerate

    def tick(self):
        currdelay -= 1


#================
# Pawns

class Pawn(Actor):

    def TakeDamage(self, amount, instigator):
        if self.armor > 0.0:
            self.health -= (amount / 3.0) * 2.0
            self.armor -= (amount / 3.0) * 1.0
            if armor < 0.0:
                armor = 0.0
        else:
            self.health -= amount
        self.ShootTarget = instigator

        if self.Health < 0:
            self.Killed(instigator)

    def Shoot(self, TargetActor):
        pass

    def GiveHealth(self, amount, healthinv):
        health += amount
        if health > maxHealth:
            health = maxHealth
        del healthinv

    def Killed(self, killer):
        health = -666

    def tick(self):
        self.x, self.y, self.z = self.location.x, self.location.y, self.location.z
        self.location += Vector(self.XVelocity, self.YVelocity, self.ZVelocity)
        self.ZVelocity -= self.owner.gravity
        Touched = False
        for w in self.owner.brushlist:
            if w.HasCoordinate(self.x, self.y, self.z):
                Touched = True
                w.Touch(self)
        if Touched == True:
            self.location -= Vector(self.XVelocity, self.YVelocity, self.ZVelocity)
            ZVelocity = 0


    def Jump(self):
        self.ZVelocity += self.JumpZ
        self.Jumping = true

    def MoveToActor(self, actor):
        assert isinstance(actor, Actor) or issubclass(type(actor), Actor)

        self.MoveToPoint(actor.x, actor.y, actor.z)

    def MoveToPoint(self, x, y, z):
        assert isinstance(x, float) and\
        isinstance(y, float) and\
        isinstance(z, float)

        if (z > self.z + (self.JumpZ * (self.JumpZ / -self.owner.gravity))):
            if not self.Jumping:
                self.Jump()
            self.location = self.location.move_towards(Vector(x, y, self.z), self.location.distance_to(Vector(x, y, self.z)) / self.airspeedfactor)
        else:
            self.location = self.location.move_towards(Vector(x, y, self.z), self.location.distance_to(Vector(x, y, self.z)) / self.groundspeedfactor)

    def __init__(self, x, y, z, health, name, armor, tag, owner, pitch = 0, yaw = 0, roll = 0):
        super(Pawn, self).__init__(x, y, z, name, owner, pitch, yaw, roll)
        self.health, self.armor, self.tag = health, armor, tag
        self.airspeedfactor = 1.16
        self.maxHealth = 100
        self.ShootTarget = None
        self.ViewFactor = 70
        self.JumpZ = 75
        self.Jumping = False
        self.XVelocity = 0
        self.YVelocity = 0
        self.ZVelocity = 0
        self.groundspeedfactor = 1.92
        self.CurrentNavigationPoint = None
        self.Roam()

    def FindInventory(self):
        foundinventories = []
        for w in self.owner.actorlist:
            if not isinstance(w, Inventory) or issubclass(type(w, Inventory)):
                continue
            if LineOfSightTo(w):
                foundinventories.append(w)
        return foundinventories

    def Roam(self):
        if not hasattr(self, "CurrentNavigationPoint") or self.CurrentNavigationPoint == None:
            maxdist = 2000
            for w in self.owner.actorlist:
                if not (isinstance(w, NavigationPoint) or issubclass(type(w), NavigationPoint)):
                    continue
                cdist = self.DistanceToActor(w)
                if cdist < maxdist:
                    maxdist = cdist
                    self.CurrentNavigationPoint = w
            self.NextNavigationPoint = self.CurrentNavigationPoint

        else:
            self.NextNavigationPoint = choice(self.CurrentNavigationPoint.ConnectedNodes)

class Bot(Pawn):

    inventory = []
    pathbuffer = []

    state = "Roaming"

    def __init__(self, x, y, z, health, name, armor, tag, owner, pitch = 0, yaw = 0, roll = 0):
        super(Bot, self).__init__(x, y, z, health, name, armor, tag, owner, pitch, yaw, roll)
        self.currentweapon = WeaponInventory(self.x, self.y, self.z, "Shotty", 0.3, 20, 60, 12, 1, self.owner)
        self.Roam()

    def Shoot(targetactor):
        ChooseBestWeapon()
        self.currentweapon.FireProjectile(targetactor.location)

    def ChooseBestWeapon():
        currating = 0

        for w in self.Inventory:
            if not isinstance(w, WeaponInventory):
                continue
            if w.rating > currating:
                currating = w.rating
                currentweapon = w

    def CollectInventory(self, inventory):
        if DistanceToActor(inventory) < 150:
            return False
        inventory.Collected(self)
        self.inventory.append(inventory)
        logandprint("| Bot " + self.name + " collected inventory " + inventory.name)
        return True

    def GetNextNavigationPoint(self, CallerNavigationPoint):
        if self.FindInventory() != []:
            return choice(FindInventory())
        if self.state == "Roaming":
            return choice(CallerNavigationPoint.ConnectedNodes)
        elif self.state == "GoingForTarget":
            return CallerNavigationPoint.GetPathToTarget

    def tick(self):
        super(Bot, self).tick()
        if not hasattr(self, "NextNavigationPoint") or self.NextNavigationPoint == None:
            self.Roam()
        else:
            self.MoveToActor(self.NextNavigationPoint)
        if self.DistanceToActor(self.NextNavigationPoint) < 235 and ( isinstance(self.NextNavigationPoint, NavigationPoint) or issubclass(type(self.NextNavigationPoint), NavigationPoint) ):
            self.NextNavigationPoint = self.NextNavigationPoint.SpecialHandling(self)
        elif isinstance(self.NextNavigationPoint, Inventory) or issubclass(type(self.NextNavigationPoint), Inventory):
            if self.NextNavigationPoint in inventory:
                Roam()
        if self.ShootTarget != None:
            if self.ShootTarget.health == -666:
                self.ShootTarget = None
            else:
                if not self.LineOfSightTo(self.ShootTarget):
                    if self.pathbuffer != []:
                        self.pathbuffer = self.CurrentNavigationPoint.GetPathToActor(self.ShootTarget)
                    if self.DistanceToActor(self.NextNavigationPoint) < 150:
                        self.CurrentNavigationPoint = self.NextNavigationPoint
                        self.pathbuffer = self.CurrentNavigationPoint.FindPathToActor(self.ShootTarget)
                        self.NextNavigationPoint = self.pathbuffer.pop(0)
                else:
                    if self.DistanceToActor(self.NextNavigationPoint) < 250:
                        self.Roam()
                    self.Shoot(self.ShootTarget)
                    self.pathbuffer = []

class Monster(Pawn):

    pathbuffer = []

    def __init__(self, x, y, z, health, name, armor, tag, owner, event, projdmg, projspeed, projradius, pitch = 0, yaw = 0, roll = 0):
        super(Monster, self).__init__(self, x, y, z, health, name, armor, tag, pitch, yaw, roll, owner)
        self.event, self.projectile_damage, self.projectile_speed, self.projectile_radius = event, projdmg, projspeed, projradius
        maxndist = 2000
        for w in owner.actorlist:
            if not w.isinstance(NavigationPoint) or w.issubclass(type(NavigationPoint)):
                continue
            if DistanceToActor(w) < maxndist:
                maxndist = DistanceToActor(w)
                CurrentNavigationPoint = w

    def Shoot(target):
        self.owner.actorlist.append(Projectile(self.x, self.y, self.z, "Monster " + str(self.name) + "'s projectile", self.owner, target.location, self.projectile_speed, self.projectile_damage, self.projectile_radius, self))

    def Killed(self, killer):
        super(self, Monster).Killed(killer)

        self.owner.Event(killer, self)

    def tick(self):
        super(self, Monster).tick()
        for w in self.owner.actorlist:
            if not w.isinstance(Bot):
                continue
            if LineOfSightTo(w):
                Target = w

        if hasattr(self, Target):
            if not LineOfSightTo(Target):
                if self.pathbuffer == []:
                    self.pathbuffer = CurrentNavigationPoint.GetPathToActor(Target)
                if DistanceToActor(self.NextNavigationPoint) < 200:
                    self.CurrentNavigationPoint = self.NextNavigationPoint
                    self.NextNavigationPoint = self.pathbuffer.pop(0)

            else:
                Roam()
                self.pathbuffer = []
                Shoot(Target)