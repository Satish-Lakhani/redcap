#! /usr/bin/python
# -*- coding: utf-8 -*-

import re

class Player:
    """rappresenta un singolo player e le sue proprieta'"""
    def __init__(self ):  #la proprieta SLOT devo averla
        self.alias = [] #tutti gli ultimi nick usati dal player
        self.camp = 0 #hit/tempo di vita
        self.DBnick = "" #(string) nick di registrazione in DB
        self.deaths = {"6":0,"7":0,"9":0,"23":0,"24":0,"31":0,"34":0,"arma":0,"total":0} #morti subite dal player (non incluso il changeteam)
        self.flood = 0 #numero di say in TempoControllo1
        self.gained_skill = 0 #skill guadagnata nell'ultima connessione
        self.guid = None  #(string) GUID
        self.guidage = 0    #eta della guid che sta usando
        self.hits = {"0":0,"1":0,"3":0,"4":0,"5":0,"6":0,"9":0,"total":0} #hit fatte dal player
        #self.isk = float(0.0) #Skill istantanea
        self.ip = "" #(string) IP
        #self.isInDB = False #Player esistente in DB.
        self.kills = {"12":0,"14":0,"15":0,"16":0,"17":0,"18":0,"19":0,"20":0,"21":0,"22":0,"23":0,"24":0,"25":0,"28":0,"30":0,"34":0,"35":0,"38":0,"40":0,"total":0} #kill fatte dal player
        self.ks = 0 #killstreak
        self.ksmax = 0 #max killstreak
        self.lastconnect = 0 #data dell'ultimo connect
        #self.lastdisconnect = None #data dell'ultimo disconnect
        self.level = 0 #livello di autorizzazione all'uso del RedCap
        self.new = True #e' appena entrato
        self.nick = "" #nick (stringa)
        self.nickchanges = 0 #cambi nick in TempoControllo1
        self.notoriety = 0 #livello di reputazione (sale con anzianita guid, rounds, bonus admin, scende con warning, tempban, tk, malus admin)
        self.rounds = 0 #round giocati
        #self.rusher =0 #tempo totale di vita sul gameserver / tempo totale (da un'idea della bravura e camperosita)
        self.skill = 0 #skill
        self.slot_id = None #(string) slot id
        self.team = 0 #(string) 0=Sconosciuto 1=red, 2=blue, 3=spect
        self.tempban = 0 #data dell'ultimo tempban
        #self.totalplayedtime = 0 #tempo totale di gioco
        self.vivo = 0   #0=Sconosciuto 1=vivo, 2=morto
        self.warning = 0    #warning assegnati al player

    def invalid_guid(self):
        """verifica se la guid del player NON e' corretta"""
        if re.search("[A-F0-9]{32}", self.guid):    #controllo guid
            return False
        else:
            return True

    def invalid_nick(self, minNick, goodNick, nome):
        """verifica se il nick del player NON e' corretto"""
        if len(nome) >= minNick:                 #controllo lunghezza nick
            if re.search(goodNick, nome):      #controllo formattazione nick
                return False    #ovvero NON e' un bad nick
            else:
                return True
        else:
            return True

    def dati_load(self,dati,N1,N2,time):
        """Aggiorna il player con i dati presi dal database tabella DATI"""                                                               
        self.DBnick = dati[1]                                         #dati = (guid, DBnick, skill, rounds, lastconn, level, tempban, notoriety, firstconn, streak, alias)
        self.skill = dati[2]
        self.rounds = dati[3]
        self.lastconnect = dati[4]                                   #data dell'ultima connessione
        self.level = dati[5]
        self.tempban = dati[6]
        self.guidage = (time - dati[8])/87400      #eta' della guid in giorni
        self.notoriety = round(dati[3] / N1 + self.guidage / N2 + dati[7], 1)    #calcolo della notoriety (basata su round, guid age, e bonus/malus) - arrotondo a 1
        self.ksmax = dati[9]
        aliases = dati[10].split(u'\xa7')                                            #formatto gli alias in maniera leggibile
        for al in aliases:
            al=al.split(u'\x08')
            self.alias.append(al)

'''
    def pick_all_data(self, DB):
        """recupera i tutti dati del player da DB e li assegna al player stesso"""
        res = DB.esegui(DB.DBcmd["alldata"], (self.guid,)) #Recupera: NICK, ROUND, SKILL, STREAK, BANNED, LASTSEEN, LEVEL, TMPBAN
        record = res.fetchone()
        if record:
            self.isInDB = True
            self.DBnick = record[0]
            self.rounds = record[1]
            self.skill = record[2]
            self.ksmax = record[3]
            self.notoriety = record[4]
            self.lastconnect = record[5]
            self.level = record[6]
            self.tempban = record[7]
            return True
        else:
            return False

    def reg_in_DB(self, DB):
        """registra un nuovo player in DB"""
        #inserisco i dati conosciuti del nuovo player in DB
        DB.esegui(DB.DBcmd["addplayer"], (self.guid, self.nick, 0, self.lastconnect, 0, 0))
        self.isInDB = True
'''
