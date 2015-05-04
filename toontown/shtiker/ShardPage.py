from pandac.PandaModules import *
import ShtikerPage
from direct.task.Task import Task
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
from direct.directnotify import DirectNotifyGlobal
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals
from toontown.distributed import ToontownDistrictStats
from toontown.toontowngui import TTDialog
from otp.ai.MagicWordGlobal import *
from toontown.suit import Suit
from toontown.battle.SuitBattleGlobals import SuitAttributes
POP_COLORS_NTT = (Vec4(0.0, 1.0, 0.0, 1.0), Vec4(1.0, 1.0, 0.0, 1.0), Vec4(1.0, 0.0, 0.0, 1.0))
POP_COLORS = (Vec4(0.4, 0.4, 1.0, 1.0), Vec4(0.4, 1.0, 0.4, 1.0), Vec4(1.0, 0.4, 0.4, 1.0))
TOTAL_POP_TEXT_COLOR = Vec4(0.5, 0.1, 0.1, 1.0)

class ShardPage(ShtikerPage.ShtikerPage):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShardPage')

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.shardButtonMap = {}
        self.shardButtons = []
        self.invasionDistricts = {}
        self.scrollList = None
        self.selectedShard = [None, None, None]
        self.suitHead = None
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.9, 1, 1)
        self.textDisabledColor = Vec4(0.4, 0.8, 0.4, 1)
        self.textSelectedColor = Vec4(0.85, 0.65, 0.12, 1)
        self.ShardInfoUpdateInterval = 5.0
        self.lowPop, self.midPop, self.highPop = base.getShardPopLimits()
        self.showPop = config.GetBool('show-total-population', 0)
        self.noTeleport = config.GetBool('shard-page-disable', 0)
        self.adminForceReload = 0
        return

    def load(self):
        main_text_scale = 0.06
        title_text_scale = 0.12
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.ShardPageTitle, text_scale=title_text_scale, textMayChange=0, pos=(0, 0, 0.6))
        helpText_ycoord = 0.403
        self.helpText = DirectLabel(parent=self, relief=None, text='', text_scale=main_text_scale, text_wordwrap=12, text_align=TextNode.ALeft, textMayChange=1, pos=(0.058, 0, helpText_ycoord))
        shardPop_ycoord = helpText_ycoord - 0.523
        totalPop_ycoord = shardPop_ycoord - 0.26
        shardName_xcoord = 0.4
        shardName_ycoord = 0.4
        self.totalPopulationText = DirectLabel(parent=self, relief=None, text=TTLocalizer.ShardPagePopulationTotal % 1, text_scale=main_text_scale, text_wordwrap=20, text_fg=TOTAL_POP_TEXT_COLOR, textMayChange=1, text_align=TextNode.ACenter, pos=(0, 0, 0.525))
        self.totalPopulationText.show()
        self.gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        self.dropShadow = loader.loadModel('phase_3/models/props/drop_shadow')
        self.dropShadow.setScale(0.2)
        self.dropShadow.setColor(0.0, 0.0, 0.0, 0.5)
        self.textures = loader.loadModel('phase_3.5/models/gui/sos_textures.bam')
        self.districtModel = self.textures.find('**/district')
        self.textures.detachNode()
        self.districtIcon = DirectFrame(parent=self, geom=self.districtModel, pos=(0.435, 0, 0), geom_scale=(0.4, 0.4, 0.4), frameColor=(0.1, 0.1, 0.1, 0))
        self.districtIcon.hide()
        self.textures.removeNode()
        self.invitationGui = loader.loadModel('phase_4/models/parties/schtickerbookInvitationGUI')
        pos = self.invitationGui.find('**/startText_locator').getPos()
        self.teleportButton = DirectButton(parent=self, relief=None, geom=(self.invitationGui.find('**/startButton_up'),
         self.invitationGui.find('**/startButton_down'),
         self.invitationGui.find('**/startButton_rollover'),
         self.invitationGui.find('**/startButton_inactive')), geom_scale=1.5, text='Teleport\nHere!', text_scale=0.045, text_pos=(0.475, -0.7), pos=(0.1, 0, 0.2), command=self.goToShard)
        self.teleportButton['state'] = DGG.DISABLED
        self.shardNameText = DirectLabel(parent=self, relief=None, text='', text_scale=main_text_scale*1.5, textMayChange=1, pos=(shardName_xcoord, 0, shardName_ycoord))
        self.shardNameText.hide()
        self.populationText = DirectLabel(parent=self, relief=None, text='', text_scale=main_text_scale, textMayChange=1, pos=(shardName_xcoord, 0, shardName_ycoord-0.1))
        self.populationText.hide()
        self.suitHeadLabel = DirectLabel(parent=self, relief=None, pos=(0.42, 0, 0))
        self.invasionText = DirectLabel(parent=self, relief=None, pos=(0.42, 0, -0.21), text='', textMayChange=1, text_fg=TOTAL_POP_TEXT_COLOR, text_scale=main_text_scale)
        self.invasionText.hide()
        self.listXorigin = -0.02
        self.listFrameSizeX = 0.67
        self.listZorigin = -0.96
        self.listFrameSizeZ = 1.04
        self.arrowButtonScale = 1.3
        self.itemFrameXorigin = -0.237
        self.itemFrameZorigin = 0.365
        self.buttonXstart = self.itemFrameXorigin + 0.293
        self.regenerateScrollList()
        scrollTitle = DirectFrame(parent=self.scrollList, text=TTLocalizer.ShardPageScrollTitle, text_scale=main_text_scale, text_align=TextNode.ACenter, relief=None, pos=(self.buttonXstart, 0, self.itemFrameZorigin + 0.127))
        return

    def unload(self):
        self.gui.removeNode()
        del self.title
        self.scrollList.destroy()
        del self.scrollList
        del self.shardButtons
        taskMgr.remove('ShardPageUpdateTask-doLater')
        ShtikerPage.ShtikerPage.unload(self)

    def regenerateScrollList(self):
        selectedIndex = 0
        if self.scrollList:
            selectedIndex = self.scrollList.getSelectedIndex()
            for button in self.shardButtons:
                button.detachNode()

            self.scrollList.destroy()
            self.scrollList = None
        self.scrollList = DirectScrolledList(parent=self, relief=None, pos=(-0.5, 0, 0), incButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
         self.gui.find('**/FndsLst_ScrollDN'),
         self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
         self.gui.find('**/FndsLst_ScrollUp')), incButton_relief=None, incButton_scale=(self.arrowButtonScale, self.arrowButtonScale, -self.arrowButtonScale), incButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin - 0.999), incButton_image3_color=Vec4(1, 1, 1, 0.2), decButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
         self.gui.find('**/FndsLst_ScrollDN'),
         self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
         self.gui.find('**/FndsLst_ScrollUp')), decButton_relief=None, decButton_scale=(self.arrowButtonScale, self.arrowButtonScale, self.arrowButtonScale), decButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin + 0.227), decButton_image3_color=Vec4(1, 1, 1, 0.2), itemFrame_pos=(self.itemFrameXorigin, 0, self.itemFrameZorigin), itemFrame_scale=1.0, itemFrame_relief=DGG.SUNKEN, itemFrame_frameSize=(self.listXorigin,
         self.listXorigin + self.listFrameSizeX,
         self.listZorigin,
         self.listZorigin + self.listFrameSizeZ), itemFrame_frameColor=(0.85, 0.95, 1, 1), itemFrame_borderWidth=(0.01, 0.01), numItemsVisible=15, forceHeight=0.065, items=self.shardButtons)
        self.scrollList.scrollTo(selectedIndex)
        return

    def askForShardInfoUpdate(self, task = None):
        ToontownDistrictStats.refresh('shardInfoUpdated')
        taskMgr.doMethodLater(self.ShardInfoUpdateInterval, self.askForShardInfoUpdate, 'ShardPageUpdateTask-doLater')
        return Task.done

    def setSuitHead(self, suitName):
        self.suitHead = Suit.attachSuitHead(self.suitHeadLabel, suitName)
        self.suitHead.setScale(0.2)
        self.dropShadow.reparentTo(self.suitHead)
        
    def getFullSuitName(self, suitName):
        return SuitAttributes[suitName]['pluralname']

    def makeShardButton(self, shardId, shardName, shardPop):
        shardButtonParent = DirectFrame()
        shardButtonL = DirectButton(parent=shardButtonParent, relief=None, text=shardName, text_scale=0.06, text_align=TextNode.ALeft,
          text1_bg=self.textDownColor, text2_bg=self.textRolloverColor, text3_fg=self.textDisabledColor, textMayChange=1, command=self.selectShard, extraArgs=[shardId, shardName, shardPop])
        model = loader.loadModel('phase_3.5/models/gui/matching_game_gui')
        button = model.find('**/minnieCircle')
        shardButtonR = DirectButton(parent=shardButtonParent, relief=None, image=button, image_scale=(0.3, 1, 0.3), image2_scale=(0.35, 1, 0.35),
          image_color=self.getPopColor(shardPop), pos=(0.6, 0, 0.0125), text=self.getPopText(shardPop), text_scale=0.06, text_align=TextNode.ACenter, text_pos=(-0.0125, -0.0125), text_fg=Vec4(0, 0, 0, 0), text1_fg=Vec4(0, 0, 0, 0), text2_fg=Vec4(0, 0, 0, 1), text3_fg=Vec4(0, 0, 0, 0), command=self.selectShard, extraArgs=[shardId, shardName, shardPop])
        del model
        del button
        return (shardButtonParent, shardButtonR, shardButtonL)

    def selectShard(self, shardId, shardName, shardPop):
        self.shardNameText.show()
        self.populationText.show()
        if self.selectedShard[0]:
            print 'we already had a shard selected before'
            if self.suitHead:
                self.suitHead.removeNode()
                self.suitHeadLabel.hide()
            buttonTuple = self.shardButtonMap[self.selectedShard[0]]
            buttonTuple[2]['text_fg'] = (0, 0, 0, 1)
            buttonTuple[2]['state'] =  DGG.NORMAL
        self.selectedShard = [shardId, shardName, shardPop]
        print self.selectedShard
        buttonTuple = self.shardButtonMap[shardId]
        buttonTuple[2]['state'] = DGG.DISABLED
        buttonTuple[2]['text_fg'] = self.textSelectedColor
        self.teleportButton['state'] = DGG.NORMAL
        self.helpText.hide()
        self.shardNameText['text'] = shardName
        if shardId in self.invasionDistricts:
            print 'Shard %s has a invasion!' % shardId
            self.districtIcon.hide()
            if self.suitHead:
                self.suitHead.removeNode()
            self.setSuitHead(self.invasionDistricts[shardId])
            self.suitHeadLabel.show()
            self.invasionText['text'] = TTLocalizer.ShardPageInvasion % self.getFullSuitName(self.invasionDistricts[shardId])
            self.invasionText.show()
            #Show invasion text
        else:
            if self.suitHead:
                self.suitHead.removeNode()
            self.invasionText.hide()
            self.suitHeadLabel.hide()
            self.districtIcon.show()
    
    def goToShard(self):
        handler = self.getPopChoiceHandler(self.selectedShard[2])
        handler(self.selectedShard[0])
        

    def getPopColor(self, pop):
        if config.GetBool('want-lerping-pop-colors', False):
            if pop < self.midPop:
                color1 = POP_COLORS_NTT[0]
                color2 = POP_COLORS_NTT[1]
                popRange = self.midPop - self.lowPop
                pop = pop - self.lowPop
            else:
                color1 = POP_COLORS_NTT[1]
                color2 = POP_COLORS_NTT[2]
                popRange = self.highPop - self.midPop
                pop = pop - self.midPop
            popPercent = pop / float(popRange)
            if popPercent > 1:
                popPercent = 1
            newColor = color2 * popPercent + color1 * (1 - popPercent)
        elif pop <= self.lowPop:
            newColor = POP_COLORS[0]
        elif pop <= self.midPop:
            newColor = POP_COLORS[1]
        else:
            newColor = POP_COLORS[2]
        return newColor

    def getPopText(self, pop):
        if pop <= self.lowPop:
            popText = TTLocalizer.ShardPageLow
        elif pop <= self.midPop:
            popText = TTLocalizer.ShardPageMed
        else:
            popText = TTLocalizer.ShardPageHigh
        return popText

    def getPopChoiceHandler(self, pop):
        if base.cr.productName == 'JP':
            handler = self.choseShard
        elif pop <= self.midPop:
            if self.noTeleport and not self.showPop:
                handler = self.shardChoiceReject
            else:
                handler = self.choseShard
        elif self.showPop:
            handler = self.choseShard
        else:
            handler = self.shardChoiceReject
        return handler

    def getCurrentZoneId(self):
        try:
            zoneId = base.cr.playGame.getPlace().getZoneId()
        except:
            zoneId = None

        return zoneId

    def getCurrentShardId(self):
        zoneId = self.getCurrentZoneId()
        if zoneId != None and ZoneUtil.isWelcomeValley(zoneId):
            return ToontownGlobals.WelcomeValleyToken
        else:
            return base.localAvatar.defaultShard
        return

    def updateScrollList(self):
        curShardTuples = base.cr.listActiveShards()

        def compareShardTuples(a, b):
            if a[1] < b[1]:
                return -1
            elif b[1] < a[1]:
                return 1
            else:
                return 0

        curShardTuples.sort(compareShardTuples)
        if base.cr.welcomeValleyManager:
            curShardTuples.append((ToontownGlobals.WelcomeValleyToken,
             TTLocalizer.WelcomeValley[-1],
             0,
             0))
        currentShardId = self.getCurrentShardId()
        actualShardId = base.localAvatar.defaultShard
        actualShardName = None
        anyChanges = 0
        totalPop = 0
        totalWVPop = 0
        currentMap = {}
        self.shardButtons = []
        for i in range(len(curShardTuples)):
            shardId, name, pop, WVPop, invasionStatus = curShardTuples[i]
            if shardId == actualShardId:
                actualShardName = name
            totalPop += pop
            totalWVPop += WVPop
            currentMap[shardId] = 1
            buttonTuple = self.shardButtonMap.get(shardId)
            if buttonTuple == None or self.adminForceReload:
                buttonTuple = self.makeShardButton(shardId, name, pop)
                self.shardButtonMap[shardId] = buttonTuple
                anyChanges = 1
            else:
                buttonTuple[1]['image_color'] = self.getPopColor(pop)
                if not base.cr.productName == 'JP':
                    buttonTuple[1]['text'] = self.getPopText(pop)
                    buttonTuple[1]['command'] = self.selectShard
                    buttonTuple[2]['command'] = self.selectShard
                    buttonTuple[1]['extraArgs'] = [shardId, name, pop]
                    buttonTuple[2]['extraArgs'] = [shardId, name, pop]
                    self.populationText['text'] = TTLocalizer.ShardPageShardPopulation % pop
                    if invasionStatus:
                        self.invasionDistricts[shardId] = invasionStatus
                    elif not invasionStatus and shardId in self.invasionDistricts:
                        self.invasionDistricts[shardId] = ''
            self.shardButtons.append(buttonTuple[0])
            if shardId == currentShardId or self.book.safeMode:
                buttonTuple[1]['state'] = DGG.DISABLED
                buttonTuple[2]['state'] = DGG.DISABLED
            else:
                buttonTuple[1]['state'] = DGG.NORMAL
                buttonTuple[2]['state'] = DGG.NORMAL

        for shardId, buttonTuple in self.shardButtonMap.items():
            if shardId not in currentMap:
                buttonTuple[0].destroy()
                del self.shardButtonMap[shardId]
                anyChanges = 1

        buttonTuple = self.shardButtonMap.get(ToontownGlobals.WelcomeValleyToken)
        if buttonTuple:
            if self.showPop:
                buttonTuple[1]['text'] = str(totalWVPop)
            else:
                buttonTuple[1]['image_color'] = self.getPopColor(totalWVPop)
                if not base.cr.productName == 'JP':
                    buttonTuple[1]['text'] = self.getPopText(totalWVPop)
                    buttonTuple[1]['command'] = self.selectShard
                    buttonTuple[2]['command'] = self.selectShard
                    buttonTuple[1]['extraArgs'] = [ToontownGlobals.WelcomeValleyToken, 'Welcome Valley', totalWVPop]
                    buttonTuple[2]['extraArgs'] = [ToontownGlobals.WelcomeValleyToken, 'Welcome Valley', totalWVPop]

        if anyChanges or self.adminForceReload:
            self.regenerateScrollList()
        self.totalPopulationText['text'] = TTLocalizer.ShardPagePopulationTotal % totalPop
        helpText = TTLocalizer.ShardPageHelpIntro
        if actualShardName:
            if currentShardId == ToontownGlobals.WelcomeValleyToken:
                helpText += TTLocalizer.ShardPageHelpWelcomeValley % actualShardName
            else:
                helpText += TTLocalizer.ShardPageHelpWhere % actualShardName
        if not self.book.safeMode:
            helpText += TTLocalizer.ShardPageHelpMove
        self.helpText['text'] = helpText
        if self.adminForceReload:
            self.adminForceReload = 0
        return

    def enter(self):
        self.askForShardInfoUpdate()
        self.updateScrollList()
        currentShardId = self.getCurrentShardId()
        buttonTuple = self.shardButtonMap.get(currentShardId)
        if buttonTuple:
            i = self.shardButtons.index(buttonTuple[0])
            self.scrollList.scrollTo(i, centered=1)
        ShtikerPage.ShtikerPage.enter(self)
        self.accept('shardInfoUpdated', self.updateScrollList)

    def exit(self):
        self.ignore('shardInfoUpdated')
        self.ignore('confirmDone')
        self.selectedShard = [None, None, None]
        taskMgr.remove('ShardPageUpdateTask-doLater')
        ShtikerPage.ShtikerPage.exit(self)

    def shardChoiceReject(self, shardId):
        self.confirm = TTDialog.TTGlobalDialog(doneEvent='confirmDone', message=TTLocalizer.ShardPageChoiceReject, style=TTDialog.Acknowledge)
        self.confirm.show()
        self.accept('confirmDone', self.__handleConfirm)

    def __handleConfirm(self):
        self.ignore('confirmDone')
        self.confirm.cleanup()
        del self.confirm

    def choseShard(self, shardId):
        print 'CHOSE SHARD %s' % shardId 
        zoneId = self.getCurrentZoneId()
        canonicalHoodId = ZoneUtil.getCanonicalHoodId(base.localAvatar.lastHood)
        currentShardId = self.getCurrentShardId()
        if shardId == currentShardId:
            return
        elif shardId == ToontownGlobals.WelcomeValleyToken:
            self.doneStatus = {'mode': 'teleport',
             'hood': ToontownGlobals.WelcomeValleyToken}
            messenger.send(self.doneEvent)
        elif shardId == base.localAvatar.defaultShard:
            self.doneStatus = {'mode': 'teleport',
             'hood': canonicalHoodId}
            messenger.send(self.doneEvent)
        else:
            try:
                place = base.cr.playGame.getPlace()
            except:
                try:
                    place = base.cr.playGame.hood.loader.place
                except:
                    place = base.cr.playGame.hood.place

            place.requestTeleport(canonicalHoodId, canonicalHoodId, shardId, -1)

@magicWord(category=CATEGORY_MODERATION)
def togpop():
    """
    Moderation command to toggle shard population. If toggled off, moderators can teleport in
    to full districts, regardless of their population.

    This command should NOT be abused for normal game play, as districts have a "full" status
    for a reason, and cramming more toons in to a district can cause stability issues.
    """
    base.localAvatar.shardPage.showPop = not base.localAvatar.shardPage.showPop
    base.localAvatar.shardPage.adminForceReload = 1
    base.localAvatar.shardPage.updateScrollList()
    return "District population has been %s." % ("enabled" if base.localAvatar.shardPage.showPop else "disabled")
