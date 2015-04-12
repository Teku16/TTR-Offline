import toontown.minigame.MinigameCreatorAI
from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
from direct.distributed.PyDatagram import *
from otp.rpc.RPCServer import RPCServer
from otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from otp.distributed.OtpDoGlobals import *

class ToontownUberRepository(ToontownInternalRepository):
    notify = directNotify.newCategory('ToontownUberRepository')
    
    def __init__(self, baseChannel, serverId):
        ToontownInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='UD')
        self.wantUD = config.GetBool('want-ud', True)

    def handleConnected(self):
        ToontownInternalRepository.handleConnected(self)
        self.notify.info(True)
        if config.GetBool('want-ClientServicesManagerUD', self.wantUD):
            self.notify.info('Creating ClientServicesManagerUD...')
            # Only generate the root object once, with the CSMUD.
            rootObj = DistributedDirectoryAI(self)
            rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)
        self.notify.info('Creating globals...')
        self.createGlobals()

        if config.GetBool('want-rpc-server', False):
            self.notify.info('Starting RPC server...')
            import ToontownRPCHandler
            self.rpcserver = RPCServer(ToontownRPCHandler(self))
        self.notify.info('Done.')

    def createGlobals(self):
        """
        Create "global" objects.
        """
        self.csm = self.generateGlobalIfWanted(OTP_DO_ID_CLIENT_SERVICES_MANAGER, 'ClientServicesManager')
        self.chatAgent = self.generateGlobalIfWanted(OTP_DO_ID_CHAT_MANAGER, 'ChatAgent')
        self.friendsManager = self.generateGlobalIfWanted(OTP_DO_ID_TTR_FRIENDS_MANAGER, 'TTRFriendsManager')
        if config.GetBool('want-parties', True):
            # want-parties overrides config for want-GlobalPartyManagerUD
            self.globalPartyMgr = self.generateGlobalIfWanted(OTP_DO_ID_GLOBAL_PARTY_MANAGER, 'GlobalPartyManager')
        else:
            self.globalPartyMgr = None

    def generateGlobalIfWanted(self, doId, name):
        """
        We only create the "global" objects if we explicitly want them, or if
        the config file doesn't define it, we resort to the value of self.wantUD.
        If we don't want the object, we return None.
        """
        if config.GetBool('want-%sUD' % name, self.wantUD):
            return self.generateGlobalObject(doId, name)
        else:
            return None
