'''
Created on 23.02.2014

@author: Niklas Hempel
'''

class Message:
    
    #user messages
    MSG_ADMIN_LOGIN         =   "%s has logged in as an admin!"
    MSG_ADMIN_LOGIN_PM      =   "%s you're now an admin!"
    MSG_ADMIN_LOGOUT        =   "Admin %s has logged out!"
    MSG_MOD_LOGIN           =   "%s has logged in as a mod!"
    MSG_MOD_LOGIN_PM        =   "%s you're now a mod!"
    MSG_MOD_LOGOUT          =   "Mod %s has logged out!"
    
    #error messages
    MSG_ERROR_PERMISSION            =   "You've no permission to use this command!"
    MSG_ERROR_PERMISSION_PM         =   "You've no permission to use this command, please log-in!"
    MSG_ERROR_RCON                  =   "There was an error issuing the rcon command"
    MSG_ERROR_GENERAL               =   "Oops, something went wrong!"
    MSG_ERROR_ALREADYINCHANNEL      =   "The bot is already in %s"
    MSG_ERROR_NOTINCHANNEL          =   "The bot can't part from %s, not in channel"
    MSG_ERROR_INVALID_CHANNELNAME   =   "%s is an invalid channel name, please try again"
    MSG_ERROR_MAINCHANNEL           =   "Can't leave this channel. %s is the bots main channel!"
    MSG_ERROR_MAPNAME               =   "%s is an invalid map name, please try again"
    MSG_ERROR_GAMETYPE              =   "%s is an invalid gametype, please issue a numeric value. E.g.: 1 for Last Man Standing."
    MSG_ERROR_NUMVALUE              =   "%s is not a numeric value, please try again."
    MSG_ERROR_TEAMNAME              =   "%s cannot be used as team parameter. Try red or blue."
    MSG_ERROR_BOTTYPE               =   "%s is an invalid bot type. Try http://urt.so/?/188 for help"
    MSG_ERROR_BOOLNUMERIC           =   "%s is either not a numeric value, or neither 0 nor 1."
    MSG_ERROR_NOTESTSESSION         =   "There is no test session started. Use !test <servnum> <num> to start a test session."
    MSG_ERROR_NOTJOINEDTESTSESSION  =   "%s you haven't joined the test session, can't remove. !add to join."
    MSG_ERROR_ALREADYINTESTSESSION  =   "%s you're already in the current test session!"
    
    #rcon messages
    MSG_RCON_STATUS         =   "%s:%s is running on version %s. Mode: %s | Map: %s"
    MSG_RCON_PLAYERLIST     =   "Players Online (%s): %s on %s:%s"
    MSG_RCON_KICK           =   "%s has kicked %s off the server %s:%s"
    MSG_RCON_RELOAD         =   "%s is reloading the map on server %s:%s"
    MSG_RCON_MAP            =   "%s is changing the map on server %s:%s to %s"
    MSG_RCON_MODE           =   "%s is changing the gamemode on server %s:%s to %s"
    MSG_RCON_ADDBOT         =   "%s added a bot on server %s:%s (%s, %s, %s, %s, %s)"
    MSG_RCON_QUIT           =   "%s just killed the server %s:%s"
    MSG_RCON_GENERAL        =   "%s issued the rcon command %s on %s:%s"
    MSG_RCON_RELOAD         =   "%s has reloaded the map on %s:%s"
    MSG_RCON_RESTART        =   "%s has restarted the map on %s:%s"
    MSG_RCON_RESTARTSERV    =   "%s killed the server %s:%s"
    MSG_RCON_RCONPASSWORD   =   "%s changed the rconpassword on %s:%s to %s"
    MSG_RCON_BOTSENABLE     =   "%s enabled bots on server %s:%s"
    MSG_RCON_BOTSDISABLE    =   "%s disabled bots on server %s:%s"
    
    #bot messages
    MSG_BOT_JOINEDCHANNEL               =   "The bot has joined %s"
    MSG_BOT_PARTEDCHANNEL               =   "The bot parted from %s"
    MSG_BOT_HELP                        =   "http://urt.so/?/222"
    MSG_BOT_PLAYERJOINEDTESTSESSION     =   "%s joined the test session, %s of %s player joined!"
    MSG_BOT_PRIVMSG_TESTSESSIONSTARTED  =   "The test session has started, please check %s for further information."
    MSG_BOT_PUBMSG_TESTSESSIONSTARTED   =   "The test session has started. /connect %s:%s; password %s"
    MSG_BOT_INITTESTSESSION             =   "%s has initiated a test session. %s players required."
    MSG_BOT_REMOVEDFROMTESTSESSION      =   "%s you got successfully removed from the test session."
    
    
    
    
    