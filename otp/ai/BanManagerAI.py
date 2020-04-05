from direct.directnotify import DirectNotifyGlobal
from toontown.uberdog.ClientServicesManagerUD import executeHttpRequest
import datetime
from direct.fsm.FSM import FSM
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *
from otp.ai.MagicWordGlobal import *
from direct.showbase.DirectObject import DirectObject
import time

accountDBType = simbase.config.GetString('accountdb-type', 'developer')
if accountDBType == 'mysqldb':
    from passlib.hash import bcrypt
    import mysql.connector

class BanFSM(FSM):

    def __init__(self, air, avId, comment, duration, bannerId):
        FSM.__init__(self, 'banFSM-%s' % avId)
        self.air = air
        self.avId = avId
        self.bannerId = bannerId

        # Needed variables for the actual banning.
        self.comment = comment
        self.duration = duration
        self.DISLid = None
        self.accountId = None
        self.avName = None
        accountDBType = simbase.config.GetString('accountdb-type', 'developer')
        if accountDBType == 'mysqldb':
            mysql_username = simbase.config.GetString('mysql-username', 'toontown')
            mysql_password = simbase.config.GetString('mysql-password', 'password')
            mysql_db = simbase.config.GetString('mysql-db', 'toontown')
            mysql_host = simbase.config.GetString('mysql-host', '127.0.0.1')
            mysql_port = simbase.config.GetInt('mysql-port', 3306)
            mysql_ssl = simbase.config.GetBool('mysql-ssl', False)
            mysql_ssl_ca = simbase.config.GetString('mysql-ssl-ca', '')
            mysql_ssl_cert = simbase.config.GetString('mysql-ssl-cert', '')
            mysql_ssl_key = simbase.config.GetString('mysql-ssl-key', '')
            mysql_ssl_verify_cert = simbase.config.GetBool('mysql-ssl-verify-cert', False)
    
            # Lets try connection to the db
            if mysql_ssl:
                self.mysql_config = {
                  'user': mysql_username,
                  'password': mysql_password,
                  'db': mysql_db,
                  'host': mysql_host,
                  'port': mysql_port,
                  'client_flags': [ClientFlag.SSL],
                  'ssl_ca': mysql_ssl_ca,
                  'ssl_cert': mysql_ssl_cert,
                  'ssl_key': mysql_ssl_key,
                  'ssl_verify_cert': mysql_ssl_verify_cert
                }
            else:
                self.mysql_config = {
                  'user': mysql_username,
                  'password': mysql_password,
                  'db': mysql_db,
                  'host': mysql_host,
                  'port': mysql_port,
                }
    
            self.cnx = mysql.connector.connect(**self.mysql_config)
            self.cur = self.cnx.cursor(buffered=True)
            self.cnx.database = mysql_db
            self.update_ban = ("UPDATE Accounts SET canPlay = 0, bannedTime = %s, banRelease = %s, banReason = %s, banBy = %s where username = %s")

    def performBan(self, bannedUntil):
        accountDBType = simbase.config.GetString('accountdb-type', 'developer')
        if accountDBType == 'remote':
            executeHttpRequest('accounts/ban/', Id=self.accountId, Release=bannedUntil,
                           Reason=self.comment)
        if accountDBType == 'mysqldb':
            print (self.update_ban, (int(time.time()), bannedUntil, self.comment, self.bannerId, self.accountId))
            self.cur.execute(self.update_ban, (int(time.time()), int(bannedUntil), self.comment, self.bannerId, self.accountId))
            self.cnx.commit()

    def ejectPlayer(self):
        av = self.air.doId2do.get(self.avId)
        if not av:
            return

        # Send the client a 'CLIENTAGENT_EJECT' with the players name.
        datagram = PyDatagram()
        datagram.addServerHeader(
                av.GetPuppetConnectionChannel(self.avId),
                self.air.ourChannel, CLIENTAGENT_EJECT)
        datagram.addUint16(152)
        datagram.addString(self.avName)
        simbase.air.send(datagram)

    def dbCallback(self, dclass, fields):
        try:
            if dclass != self.air.dclassesByName['AccountAI']:
                return
    
            self.accountId = fields.get('ACCOUNT_ID')
    
            if not self.accountId:
                return
    
            date = time.time()
            if simbase.config.GetBool('want-bans', True):
                le = len(self.duration)
                if le < 2:
                    l = int(self.duration)
                    if l == 0:
                      l = 10 * (60 * 60 * 24 * 365);
                else:
                    t = self.duration[le-1]
                    l = int(self.duration[0:(le-1)])
                    if t == 'y' or t == 'Y':
                        l = l * (60 * 60 * 24 * 365);
                    elif t == 'M':
                        l = l * (60 * 60 * 24 * 31);
                    elif t == 'd' or t == 'D':
                        l = l * (60 * 60 * 24);
                    elif t == 'h' or t == 'H':
                        l = l * (60 * 60);
                    elif t == 'm':
                        l = l * 60;
    
                bannedUntil = time.time() + l
    
                self.duration = None
                self.performBan(bannedUntil)
        except:
            pass

    def getAvatarDetails(self):
        av = self.air.doId2do.get(self.avId)
        if not av:
            return

        self.DISLid = av.getDISLid()
        self.avName = av.getName()

    def log(self):
        simbase.air.writeServerEvent('ban', self.accountId, self.comment)

    def cleanup(self):
        self.air = None
        self.avId = None

        self.DISLid = None
        self.avName = None
        self.accountId = None
        self.comment = None
        self.duration = None
        self = None

    def enterStart(self):
        self.getAvatarDetails()
        self.air.dbInterface.queryObject(self.air.dbId, self.DISLid,
                                         self.dbCallback)
        self.ejectPlayer()

    def exitStart(self):
        self.log()
        self.cleanup()

    def enterOff(self):
        pass

    def exitOff(self):
        pass


class BanManagerAI(DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('BanManagerAI')

    def __init__(self, air):
        self.air = air
        self.banFSMs = {}

    def ban(self, avId, duration, comment, bannerId):
        self.banFSMs[avId] = BanFSM(self.air, avId, comment, duration, bannerId)
        self.banFSMs[avId].request('Start')

        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.banDone, [avId])

    def banDone(self, avId):
        self.banFSMs[avId].request('Off')
        self.banFSMs[avId] = None


@magicWord(category=CATEGORY_MODERATOR, types=[str])
def kick(reason='No reason specified'):
    """
    Kick the target from the game server.
    """
    target = spellbook.getTarget()
    if target == spellbook.getInvoker():
        return "You can't kick yourself!"
    datagram = PyDatagram()
    datagram.addServerHeader(
        target.GetPuppetConnectionChannel(target.doId),
        simbase.air.ourChannel, CLIENTAGENT_EJECT)
    datagram.addUint16(155)
    datagram.addString('You were kicked by a moderator for the following reason: %s' % reason)
    simbase.air.send(datagram)
    return "Kicked %s from the game server!" % target.getName()


@magicWord(category=CATEGORY_MODERATOR, types=[str, str])
def ban(duration=0, reason='No reason specified'):
    """
    Ban the target from the game server.
    arguments:  reason  hacking/language/other
                time    10m  
    """
    target = spellbook.getTarget()
    if target == spellbook.getInvoker():
        return "You can't ban yourself!"
    simbase.air.banManager.ban(target.doId, duration, reason, spellbook.getInvoker().doId)
    return "Banned %s from the game server!" % target.getName()
    
@magicWord(category=CATEGORY_MODERATOR, types=[int, str, str])
def banId(avId, duration=0, reason='No reason specified'):
    """
    Ban the target from the game server.
    arguments:  reason  hacking/language/other
                time    10m  
    """
    if not avId:
        return 'Specify an ID to ban.'
    if not isinstance(avId, int):
        return 'avID must be an integer.'
    if avId < 100000000:
        avId+=100000000
    av = self.air.doId2do.get(avId)
    if not av:
        return 'Failed to find avatar.'       
    simbase.air.banManager.ban(avId, duration, reason, spellbook.getInvoker().doId)
    return "Banned %s from the game server!" % avId