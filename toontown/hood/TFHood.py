import ToonHood
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.toonbase import ToontownGlobals
from toontown.safezone import TFSafeZoneLoader
import SkyUtil

class TFHood(ToonHood.ToonHood):
    notify = directNotify.newCategory('TFHood')

    def __init__(self, parentFSM, doneEvent, dnaStore, hoodId):
        ToonHood.ToonHood.__init__(self, parentFSM, doneEvent, dnaStore, hoodId)
        self.id = ToontownGlobals.FunnyFarm
        self.safeZoneLoaderClass = TFSafeZoneLoader.TFSafeZoneLoader
        self.storageDNAFile = 'phase_6/dna/storage_TF.xml'
        self.skyFile = 'phase_3.5/models/props/TT_sky'
        self.titleColor = (1.0, 0.5, 0.4, 1.0)

    def load(self):
        ToonHood.ToonHood.load(self)
        self.parentFSM.getStateNamed('TFHood').addChild(self.fsm)
        self.loadFlippyStand()

    def loadFlippyStand(self):
        self.flippyStand = Actor.Actor('phase_4/models/events/election_flippyStand-mod', {'idle': 'phase_4/models/events/election_flippyStand-idle'})
        self.flippyStand.reparentTo(self.showFloor)
        self.flippyStand.setPosHprScale(-43.6, -24.5, 0.01, 200, 0, 0, 0.55, 0.55, 0.55)
        self.flippyStand.exposeJoint(None,"modelRoot", "LInnerShoulder")
        flippyTable = self.flippyStand.find('**/LInnerShoulder')
        self.flippyStand.exposeJoint(None,"modelRoot", "Box_Joint")
        wheelbarrowJoint = self.flippyStand.find('**/Box_Joint').attachNewNode('Pie_Joint')
        wheelbarrow = self.flippyStand.find('**/Box')
        wheelbarrow.setPosHprScale(-2.39, 0.00, 1.77, 0.00, 0.00, 6.00, 1.14, 1.54, 0.93)
        
        cs = CollisionBox(Point3(7, 0, 0), 12, 5, 18)
        self.pieCollision = self.flippyStand.attachNewNode(CollisionNode('wheelbarrow_collision'))
        self.pieCollision.node().addSolid(cs)
        self.accept('enter' + self.pieCollision.node().getName(), self.handleWheelbarrowCollisionSphereEnter)

    def handleWheelbarrowCollisionSphereEnter(self, collEntry):
        if base.localAvatar.numPies >= 0 and base.localAvatar.numPies < 20:
            # TODO: Handle pies, maybe give TF's event its own class?
            self.restockSfx.play()
        

    def enter(self, *args):
        ToonHood.ToonHood.enter(self, *args)
        base.camLens.setNearFar(ToontownGlobals.SpeedwayCameraNear, ToontownGlobals.SpeedwayCameraFar)

        self.startFlippy()

    def startFlippy(self):
        self.flippy = NPCToons.createLocalNPC(2001)
        self.flippy.initializeBodyCollisions('toon')
        self.flippy.reparentTo(render)
        self.flippy.setPosHpr(172.37, -259.175, 9.623, 115.732, 0, 0)
        self.flippy.addActive()
        self.flippy.show()
        self.flippy.startBlink()
        self.flippy.loop('neutral')

    def exit(self):
        base.camLens.setNearFar(ToontownGlobals.DefaultCameraNear, ToontownGlobals.DefaultCameraFar)
        ToonHood.ToonHood.exit(self)

    def unload(self):
        self.parentFSM.getStateNamed('TFHood').removeChild(self.fsm)
        ToonHood.ToonHood.unload(self)

    def skyTrack(self, task):
        return SkyUtil.cloudSkyTrack(task)

    def startSky(self):
        SkyUtil.startCloudSky(self)
