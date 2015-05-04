from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class ToontownDistrictStatsAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("ToontownDistrictStatsAI")
    districtId = 0
    avatarCount = 0
    newAvatarCount = 0
    invasionStatus = ''

    def settoontownDistrictId(self, districtId):
        self.districtId = districtId

    def gettoontownDistrictId(self):
        return self.districtId

    def d_settoontownDistrictId(self, districtId):
        self.sendUpdate('settoontownDistrictId', [districtId])

    def b_settoontownDistrictId(self, districtId):
        self.d_settoontownDistrictId(districtId)
        self.settoontownDistrictId(districtId)

    def setAvatarCount(self, avCount):
        self.avatarCount = avCount

    def getAvatarCount(self):
        return self.avatarCount

    def d_setAvatarCount(self, avCount):
        self.sendUpdate('setAvatarCount', [avCount])

    def b_setAvatarCount(self, avCount):
        self.d_setAvatarCount(avCount)
        self.setAvatarCount(avCount)

    def setNewAvatarCount(self, newAvCount):
        self.newAvatarCount = newAvCount

    def getNewAvatarCount(self):
        return self.newAvatarCount

    def d_setNewAvatarCount(self, newAvCount):
        self.sendUpdate('setNewAvatarCount', [newAvCount])

    def b_setNewAvatarCount(self, newAvCount):
        self.d_setNewAvatarCount(newAvCount)
        self.setNewAvatarCount(newAvCount)

    def setInvasionStatus(self, invasionStatus):
        self.invasionStatus = invasionStatus

    def d_setInvasionStatus(self, invasionStatus):
        self.sendUpdate('setInvasionStatus', [invasionStatus])

    def b_setInvasionStatus(self, invasionStatus):
        self.setInvasionStatus(invasionStatus)
        self.d_setInvasionStatus(invasionStatus)

    def getInvasionStatus(self):
        return self.invasionStatus

