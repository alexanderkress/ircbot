'''
Created on 07.02.2014

@author: Niklas
'''

import ConfigParser
import sys

class Config:
    adminPassword = None    ### Administrator password for the bot
    modPassword = None      ### Moderator password for the bot
    
    ircServer = None        ### Hostname or IP for the IRC server
    ircPort = 0             ### Port for the IRC server
    ircChannel = None       ### IRC Channel the bot is going to join
    ircChannelPass = None   ### IRC Channel password
    ircNick = None          ### Nickname the bot is going to have on IRC
    
    gameserverIP = None
    gameserverPort = None
    gameserverPass = None
    gameserverRcon = None
    
    def __init__(self, configfile):
        self.configfile = configfile
        
        try:
            self.cfg = ConfigParser.ConfigParser()
            self.cfg.read(self.configfile)
        except ConfigParser.Error:
            print "An error occurred while reading config file"
            sys.exit(-1)
            
    def setValue(self, section, option, value):
        try:
            self.cfg.set(section, option, value)
        except ConfigParser.NoSectionError:
            print 'Cannot find required section'
            sys.exit(-1)
        except ConfigParser.NoOptionError:
            print 'Cannot find required option'
            sys.exit(-1)
        except ConfigParser.Error:
            print 'An error occurred while reading config file'
            sys.exit(-1)
            
    def read(self):
        try:
            self._readGeneralSettings()
            self._readIRCServerSettings()
            self._readGameServerSettings()
        except ConfigParser.NoSectionError:
            print 'Cannot find required section'
            sys.exit(-1)
        except ConfigParser.NoOptionError:
            print 'Cannot find required option'
            sys.exit(-1)
        except ConfigParser.Error:
            print 'An error occurred while reading config file'
            sys.exit(-1)
            
    def _readGeneralSettings(self):
        self.adminPassword = self.cfg.get('general', 'admin')
        self.modPassword = self.cfg.get('general', 'mod')
        
    def _readIRCServerSettings(self):
        self.ircServer = self.cfg.get('irc', 'server')
        self.ircPort = self.cfg.getint('irc', 'port')
        self.ircNick = self.cfg.get('irc', 'nick')
        self.ircChannel = self.cfg.get('irc', 'channel')
        self.ircChannelPass = self.cfg.get('irc', 'channelpass')
        
    def _readGameServerSettings(self):
        self.gameserverIP = self.cfg.get('gameserv', 'gameserverip').split()
        self.gameserverPort = self.cfg.get('gameserv', 'gameserverport').split()
        self.gameserverPass = self.cfg.get('gameserv', 'gameserverpass').split()
        self.gameserverRcon = self.cfg.get('gameserv', 'gameserverrcon').split()
        
    def printValues(self):
        print "* [ADMIN] Password: %s" % self.adminPassword
        print "* [MOD]   Password: %s" % self.modPassword
        print "* [IRC]   Server:   %s:%s - %s" % (self.ircServer, self.ircPort, self.ircNick)
        for i in range(0, len(self.gameserverIP)):
            print "* [GSERV] IP:       %s:%s - PASSWORD: %s - RCON: %s" % (self.gameserverIP[i], self.gameserverPort[i], self.gameserverPass[i], self.gameserverRcon[i])
        