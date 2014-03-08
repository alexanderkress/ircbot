'''
Created on 05.03.2014

@author: Niklas Hempel
'''

class Player(object):
    num = None
    score = None
    ping = None
    name = None
    lastmsg = None
    address = None
    qport = None
    rate = None


    def __init__(self, num, negative, score, ping, name, lastmsg, address, qport, rate):
        self.num = num
        self.score = negative + score
        self.ping = ping
        self.name = name
        self.lastmsg = lastmsg
        self.address = address
        self.qport = qport
        self.rate = rate
        
    def getName(self):
        return self.name
    
    def getScore(self):
        return self.score
    
    def getPing(self):
        return self.ping
    
    def getLastmsg(self):
        return self.lastmsg
    
    def getAddress(self):
        return self.address
    
    def getQport(self):
        return self.qport
    
    def getRate(self):
        return self.rate
        