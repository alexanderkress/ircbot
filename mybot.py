#! /usr/bin/env python
#
# This bot is a gateway between Urban Terror servers and IRC.
# 
# It is based on frubot using irclib.py written by
# fruk <tm@ols.vectranet.pl>
# irclib.py by Joel Rosdahl <joel@rosdahl.net>
#
# rcon.py is borrowed from Kiwi Bot written by
# Mathieu "MathX" Xhonneux
#
# Thank you!
#
# This program is free without restrictions; do anything you like
# with it.
#
# Modifications are made by
# Liquid <liq@liq-urt.de>
#

import irclib
import sys
import config
import time
import rcon
import re
from player import Player
from messages import Message

VERSION = "0.0.1"

class MyBot(irclib.SimpleIRCClient):

    def __init__(self, target, targetpass, rcon, cfg):
        irclib.SimpleIRCClient.__init__(self)
        self.target = target            ## target is the bot's main channel
        self.targetpass = targetpass    ## password of the channel if there's one
        self.rcon = rcon                ## rcon-"connection" to the urt-server
        self.cfg = cfg                  ## bot's config
        self.m = Message()              ## bot's messages
        self.admins = {}                ## for the bot's admin/mod login
        self.chanadmins = {}            ## saving oped / voiced status of people in channel
        self.channel = []               ## channels the bot has joined
        self.player = {}                ## saving players connected to the urt-server
        self.maxplayercount = 0
        self.playerjoined = []
        self.channel.append(self.target)
    
    '''
    Outputs a message on the UrT-Servers and IRC-Channel
    after joining the IRC-Server
    '''    
    def on_welcome(self, connection, event):
        if irclib.is_channel(self.target):
            print "*** Joining channel %s" %self.target
            connection.join(self.target, self.targetpass)
            self.connection.privmsg_many(self.target, "[%s] v%s" % (self.cfg.ircNick, VERSION)) 
            #self.rcon.send("say \"[%s] v%s\"" % (self.cfg.ircNick, VERSION))
    
    '''
    Kills the program after disconnecting form the IRC-Server
    '''        
    def on_disconnect(self, connection, event):
        sys.exit(0)
    
    '''
    Bot's response on private messages. Two available commands:
    - !login <type> <password>
    - !logout
    all other messages get ignored.
    '''
    def on_privmsg(self, connection, event):
        source = event.source()
        nick = source.split('!')[0]
        args = event.arguments()
        message = args[0].split(' ') 
        
        if message[0] == "!login" and len(message) >2:
            if message[1] == "admin" and message[2] == self.cfg.adminPassword:
                self.admins[event.source()] = 'admin'
                self.connection.privmsg(nick, self.m.MSG_ADMIN_LOGIN_PM % (nick))
                self.connection.privmsg(self.target, self.m.MSG_ADMIN_LOGIN % (nick))
            elif message[1] == "mod" and message[2] == self.cfg.modPassword:
                self.admins[event.source()] = 'mod'
                self.connection.privmsg(nick, self.m.MSG_MOD_LOGIN_PM % (nick))
                self.connection.privmsg(self.target, self.m.MSG_MOD_LOGIN % (nick))
        elif message[0] == "!logout":
            try:
                if self.admins[event.source] == 'admin':
                    self.connection.privmsg(self.target, self.m.MSG_ADMIN_LOGOUT % (nick))
                else:
                    self.connection.privmsg(self.target, self.m.MSG_MOD_LOGOUT % (nick))
                del self.admins[event.source()]
            except:
                pass
    
    '''
    Bot's response on public messages. (All channels the bot has joined)
    Available commands:
    - !die 
         - Should kill the bot, but only restarts it for now
    - !join <channel> </key/>
         - Allows the bot to join additional channel, with our without key
    - !part <channel>
        - Makes the bot part a channel it's in. Can't part the main channel
    - !help
        - Displays a link to the help page on urt.info
    - !test <num>
        - Starts a test session with num-players
    - !add
        - Makes a player join a test session
    - !remove
        - Removes the player from the active test session, if joined.
    - !rcon <params>
        - Sends a direct rcon command to the urt-server
    - !playerlist
        - Displays all current connected players to the urt-server
    - !status
        - Displays general urt-server information like version, etc.
    - !map <mapname>
        - Changes the map on the urt-server
    - !mode <gametype>
        - Changes the gametype on the urt-server and reloads it afterwards
    - !kick <player/id>
        - Kicks a player off the urt-server
    - !restart
        - Restarts the map on the urt-server
    - !reload
        - Reloads the map on the urt-server
    - !restartserv
        - Sends the rcon-command quit to the urt-server -> Bash script restarts it
    - !botenable <1/0>
        - Enables or disables bots on the urt-server and reloads it afterwards
    - !botadd <bottype> <skill level> <team> <join delay> <botname>
        - Adds a bot on the urt-server
    '''
    def on_pubmsg(self, connection, event):
        source = event.source()
        nick = source.split('!')[0]
        args = event.arguments()
        message = args[0].split(' ')
        
        '''
        Checking if the player has OP or Voice in the IRC-Channel.
        Getting the status through a whois. It's not beautiful, but
        working. Doesn't detect if someone get's un-OPed or un-Voiced.
        Detecting that would require a bot-restart.
        '''
        try:
            self.chanadmins[nick]
        except KeyError:
            self.connection.whois_liq(nick)
            if nick == "/whois":
                whoischannels = args[1].split(' ')
                if ("@"+self.target) in whoischannels:
                    self.chanadmins[message[0]] = '@'
                elif ("+"+self.target) in whoischannels:
                    self.chanadmins[message[0]] = '+'
                else:
                    self.chanadmins[message[0]] = 'None'
        
        ### BOT COMMANDS
        if message[0] == '!die':
            try:
                if self.chanadmins[nick] == '@' or self.admins[event.source()] == 'admin':
                    try:
                        self.disconnect("%s killed me ._." % (nick))
                    except:
                        self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
            except KeyError:
                self.connection.privmsg(nick, self.m.MSG_ERROR_PERMISSION_PM)
                self.connection.privmsg(self.target, self.m.MSG_ERROR_PERMISSION) 
        elif message[0] == '!join' and len(message) >1:
            try:
                if self.chanadmins[nick] == '@' or self.admins[event.source()] == 'admin':
                    try:
                        channel_str = re.match(r'#(.*)', message[1], re.M|re.I)
                        if channel_str:
                            if not message[1] in self.channel:
                                if len(message) == 2:
                                    self.connection.join(message[1])
                                    self.channel.append(message[1])
                                    self.connection.privmsg(self.target, self.m.MSG_BOT_JOINEDCHANNEL % (message[1]))
                                elif len(message) == 3:
                                    self.connection.join(message[1], message[2])
                                    self.channel.append(message[1])
                                    self.connection.privmsg(self.target, self.m.MSG_BOT_JOINEDCHANNEL % (message[1]))
                                else:
                                    self.connection.privmsg(self.target, "Too many parameters issued.")
                            else:
                                self.connection.privmsg(self.target, self.m.MSG_ERROR_ALREADYINCHANNEL % (message[1]))
                        else:
                            self.connection.privmsg(self.target, self.m.MSG_ERROR_INVALID_CHANNELNAME % (message[1]))
                    except:
                        self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
            except KeyError:
                self.connection.privmsg(nick, self.m.MSG_ERROR_PERMISSION_PM)
                self.connection.privmsg(self.target, self.m.MSG_ERROR_PERMISSION)                         
        elif message[0] == '!part' and len(message) >1:
            try:
                if  self.chanadmins[nick] == '@' or self.admins[event.source()] == 'admin':
                    try:
                        channel_str = re.match(r'#(.*)', message[1], re.M|re.I)
                        if channel_str:
                            if message[1] in self.channel:
                                if message[1] != self.target:
                                    self.connection.part(message[1])
                                    self.channel.remove(message[1])
                                    self.connection.privmsg(self.target, self.m.MSG_BOT_PARTEDCHANNEL % (message[1]))
                                else:
                                    self.connection.privmsg(self.target, self.m.MSG_ERROR_MAINCHANNEL % (self.target))
                            else:
                                self.connection.privmsg(self.target, self.m.MSG_ERROR_NOTINCHANNEL % (message[1]))
                        else:
                            self.connection.privmsg(self.target, self.m.MSG_ERROR_INVALID_CHANNELNAME % (message[1]))
                    except:
                        self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
            except KeyError:
                self.connection.privmsg(nick, self.m.MSG_ERROR_PERMISSION_PM)
                self.connection.privmsg(self.target, self.m.MSG_ERROR_PERMISSION)
        ### OTHER COMMANDS
        elif message[0] == '!help':
            try:
                self.connection.privmsg_many(self.target, self.m.MSG_BOT_HELP)
            except:
                self.connection.privmsg_many(self.channel, self.m.MSG_ERROR_GENERAL)
        elif message[0] == '!test' and len(message) >1:
            try:
                if int(message[1]):
                    try:
                        self.maxplayercount = int(message[1])
                        self.connection.privmsg(self.target, self.m.MSG_BOT_INITTESTSESSION % (nick, message[1]))
                    except ValueError:
                        self.connection.privmsg(self.target, "Parameter needs to be a numeric value.")
                    except:
                        self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
            except:
                self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
        elif message[0] == '!add':
            try:
                if len(self.playerjoined) < self.maxplayercount:
                    try:
                        if not nick in self.playerjoined:
                            try:
                                self.playerjoined.append(nick)
                                self.connection.privmsg(self.target, self.m.MSG_BOT_PLAYERJOINEDTESTSESSION % (nick, str(len(self.playerjoined)), self.maxplayercount))
                                if len(self.playerjoined) == self.maxplayercount:
                                    try:
                                        self.connection.privmsg_many(self.playerjoined, self.m.MSG_BOT_PRIVMSG_TESTSESSIONSTARTED % (self.target))                                                  ## Session started - messaging player
                                        self.connection.privmsg(self.target, self.m.MSG_BOT_PUBMSG_TESTSESSIONSTARTED % (self.cfg.gameserverIP, self.cfg.gameserverPort, self.cfg.gameserverPass))  ## General message into the channel
                                        self.maxplayercount = 0
                                        for v in self.playerjoined:
                                            self.playerjoined.remove(v)
                                    except:
                                        self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL+"1")
                            except:
                                self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
                        else:
                            self.connection.privmsg(nick, self.m.MSG_ERROR_ALREADYINTESTSESSION % (nick))
                    except:
                        self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL+"2")
                else:
                    self.connection.privmsg(self.target, self.m.MSG_ERROR_NOTESTSESSION)
            except:
                self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
        elif message[0] == '!remove':
            try:
                if nick in self.playerjoined:
                    try:
                        self.playerjoined.remove(nick)
                        self.connection.privmsg(nick, self.m.MSG_BOT_REMOVEDFROMTESTSESSION % (nick))
                    except:
                        self.connection.privmsg(nick, self.m.MSG_ERROR_NOTJOINEDTESTSESSION % (nick))
            except:
                self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
        ### RCON COMMANDS -> TO SERVER
        elif message[0] == '!rcon' and len(message) >1:
            try:
                if self.chanadmins[nick] == '+' or self.chanadmins[nick] == '@' or self.admins[event.source()] == 'admin':
                    try:
                        command = ""
                        for i in range(1, len(message)):
                            try:
                                if i == len(message):
                                    command = command + message[i]
                                else:
                                    command = command + message[i] + " "
                            except IndexError:
                                self.connection.privmsg(self.target, "Array out of range.")
                        self.rcon.send(command)
                        self.connection.privmsg(self.target, self.m.MSG_RCON_GENERAL % (nick, message[1], self.cfg.gameserverIP, self.cfg.gameserverPort))
                    except:
                        self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
            except KeyError:
                self.connection.privmsg(nick, self.m.MSG_ERROR_PERMISSION_PM)
                self.connection.privmsg(self.target, self.m.MSG_ERROR_PERMISSION)
        elif message[0] == '!status':
            try:
                response = self.rcon.send_norcon("getstatus")
                if response:
                    response = response.splitlines()
                    response = response[1].split('\\')
                    modversion = response[response.index("g_modversion")+1]
                    gametype = response[response.index("g_gametype")+1]
                    mapname = response[response.index("mapname")+1]
                            
                self.connection.privmsg(self.target, self.m.MSG_RCON_STATUS % (self.cfg.gameserverIP, self.cfg.gameserverPort, modversion, gametype, mapname))
            except:
                self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
        elif message[0] == '!playerlist':
            try:
                rcon_status = self.rcon.send("status")
                status_split = rcon_status.splitlines()
                if len(status_split) > 3:
                    try:
                        for x in range(3, len(status_split)): ### range starting at 3, because of the static status lines.
                            try:
                                rcon_str = re.compile(r'\s*(\d+)\s+(-?)(\d+)\s+(\d+)\s+(.*)\s+(\d+)\s+(\S*)\s+(\d+)\s+(\d+)')
                                match = rcon_str.match(status_split[x])
                                if match:
                                    try:
                                        count = x-3
                                        line = match.groups()
                                        num, negative, score, ping, name, lastmsg, address, qport, rate = line
                                        if negative == "-":
                                            score = "-" + score
                                        
                                        name = ''.join(name.split())
                                        self.player[count] = Player(num, negative, score, ping, name, lastmsg, address, qport, rate)
                                    except:
                                        print self.m.MSG_ERROR_GENERAL
                            except IndexError:
                                print "Array out of range."
                            
                        playerlist = ""
                        
                        for i in range(0, len(self.player)):
                            try:
                                if i == (len(self.player)-1):
                                    playerlist = playerlist + self.player[i].getName()
                                else:
                                    playerlist = playerlist + self.player[i].getName() + ", "
                            except IndexError:
                                self.connection.privmsg(self.target, "Array out of range.")
                                        
                        self.connection.privmsg(self.target, self.m.MSG_RCON_PLAYERLIST % (str(count+1), playerlist, self.cfg.gameserverIP, self.cfg.gameserverPort))
                    except:
                        self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
                else:
                    self.connection.privmsg(self.target, self.m.MSG_RCON_PLAYERLIST % ("0", None, self.cfg.gameserverIP, self.cfg.gameserverPort))
            except:
                self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
        elif message[0] == '!restartserv':
            try:
                if self.chanadmins[nick] == '+' or self.chanadmins[nick] == '@' or self.admins[event.source()] == 'admin':
                    try:
                        self.rcon.send("quit")
                        self.connection.privmsg(self.target, self.m.MSG_RCON_RESTARTSERV % (nick, self.cfg.gameserverIP, self.cfg.gameserverPort))
                    except:
                        self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
            except KeyError:
                self.connection.privmsg(nick, self.m.MSG_ERROR_PERMISSION_PM)
                self.connection.privmsg(self.target, self.m.MSG_ERROR_PERMISSION) 
        elif message[0] == '!kick' and len(message) >1:
            try:
                self.rcon.send("kick " + message[1])
                self.connection.privmsg(self.target, self.m.MSG_RCON_KICK % (nick, message[1], self.cfg.gameserverIP, self.cfg.gameserverPort)) 
            except:
                self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)  
        elif message[0] == '!map' and len(message) >1:
            try:
                mapname_str = re.match(r'ut4_(.*)', message[1], re.M|re.I)
                if mapname_str:
                    self.rcon.send("map " + message[1])
                    self.connection.privmsg(self.target, self.m.MSG_RCON_MAP % (nick, self.cfg.gameserverIP, self.cfg.gameserverPort, message[1])) 
                else:
                    self.connection.privmsg(self.target, self.m.MSG_ERROR_MAPNAME % (message[1]))
            except:
                self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)  
        elif message[0] == '!mode' and len(message) >1:
            try:
                mode_int = int(message[1])
                try:
                    self.rcon.send("g_gametype \"" + str(mode_int) + "\"")
                    self.rcon.send("reload")
                    self.connection.privmsg(self.target, self.m.MSG_RCON_MODE % (nick, self.cfg.gameserverIP, self.cfg.gameserverPort, str(mode_int)))
                except:
                    self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
            except ValueError:
                self.connection.privmsg(self.target, self.m.MSG_ERROR_GAMETYPE % (message[1]))
        elif message[0] == '!restart':
            try:
                self.rcon.send("restart")
                self.connection.privmsg(self.target, self.m.MSG_RCON_RESTART % (nick, self.cfg.gameserverIP, self.cfg.gameserverPort))
            except:
                self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
        elif message[0] == '!reload':
            try:
                self.rcon.send("reload")
                self.connection.privmsg(self.target, self.m.MSG_RCON_RELOAD % (nick, self.cfg.gameserverIP, self.cfg.gameserverPort))
            except:
                self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
        elif message[0] == '!botenable' and len(message) >1:
            try:
                if int(message[1]) >= 0 and int(message[1]) <= 1:
                    try:
                        if int(message[1]) == 0:
                            self.rcon.send("bot_enable 0")
                            self.rcon.send("reload")
                            self.connection.privmsg(self.target, self.m.MSG_RCON_BOTSDISABLE % (nick, self.cfg.gameserverIP, self.cfg.gameserverPort))
                        elif int(message[1]) == 1:
                            self.rcon.send("bot_enable 1")
                            self.rcon.send("reload")
                            self.connection.privmsg(self.target, self.m.MSG_RCON_BOTSENABLE % (nick, self.cfg.gameserverIP, self.cfg.gameserverPort))
                    except ValueError:
                        self.connection.privmsg(self.target, self.m.MSG_ERROR_BOOLNUMERIC % (message[1]))
            except:    
                self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
        elif message[0] == '!botadd' and len(message) >4:
            try:
                bot_types = ["boa", "cheetah", "chicken", "cobra", "cockroach", "cougar", "goose", "mantis", "penguin", "puma", "python", "raven", "scarab", "scorpion", "tiger", "widow"]
                teams = ["blue", "red"]
                if message[1] in bot_types:
                    try:
                        if int(message[2]):
                            try:
                                if message[3] in teams:
                                    try:
                                        if int(message[4]):
                                            self.rcon.send("addbot %s %s %s %s %s" % (message[1], message[2], message[3], message[4], message[5]))
                                            self.connection.privmsg(self.target, self.m.MSG_RCON_ADDBOT % (nick, self.cfg.gameserverIP, self.cfg.gameserverPort, message[1], message[2], message[3], message[4], message[5]))
                                    except ValueError:
                                        self.connection.privmsg(self.target, self.m.MSG_ERROR_NUMVALUE % (message[4]))
                            except:
                                self.connection.privmsg(self.target, self.m.MSG_ERROR_TEAMNAME % (message[3])) 
                    except ValueError:
                        self.connection.privmsg(self.target, self.m.MSG_ERROR_NUMVALUE % (message[1])) 
                else:
                    self.connection.privmsg(self.target, self.m.MSG_ERROR_BOTTYPE % (message[1]))
            except:
                self.connection.privmsg(self.target, self.m.MSG_ERROR_GENERAL)
            
    def on_kick(self, connection, event):
        if event.arguments()[0] == self.cfg.ircNick and irclib.is_channel(self.target):
            print "*** Got kicked, re-joining channel %s" %self.target
            self.connection.join(self.target, self.targetpass)
        
    def disconnect(self, message):
        self.connection.disconnect(message)
    
    
def main():
    if len(sys.argv) != 2:
        print "Usage: mybot.py <config>"
        sys.exit(1)
     
    cfg = config.Config(sys.argv[1])
    cfg.read()
    cfg.printValues()
    
    server = cfg.ircServer
    port = cfg.ircPort
    nickname = cfg.ircNick
    initnickname = nickname
    target = cfg.ircChannel
    targetpass = cfg.ircChannelPass
    
    while True:
        try:
            r = rcon.rcon(cfg.gameserverIP, int(cfg.gameserverPort), cfg.gameserverRcon)
            s = MyBot(target, targetpass, r, cfg)
            print "*** Connecting to %s:%d as %s" % (server, port, nickname)
            s.connect(server, port, nickname)
            time.sleep(1.0)
            s.start()
        except irclib.ServerConnectionError:
            print "Could not connect to server"
        except irclib.ServerNotConnectedError:
            print "Reconnecting in 10 secs"
            time.sleep(10.0)
        except KeyboardInterrupt:
            print "*!* Interrupted by keyboard! Waiting for threads..."
            s.disconnect("Someone killed me. Oh noes!")
            sys.exit(0)    
        except:
            print sys.exc_info()[:2]
            print "*** Restarting..."
            
            if nickname != initnickname:
                nickname = initnickname
            else:
                nickname = nickname + "_"
                
            cfg.ircNick = nickname
            time.sleep(10.0)
    
    
if __name__ == "__main__":
    main()

        