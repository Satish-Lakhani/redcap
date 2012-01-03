#! /usr/bin/python
# -*- coding: utf-8 -*-

import re

class Player:
    """rappresenta un singolo player e le sue proprieta'"""
    def __init__(self ):        #la proprieta SLOT devo averla
        self.alias = []         #tutti gli ultimi nick usati dal player
        #self.camp = 0          #hit/tempo di vita #TODO serve?
        self.DBnick = ""        #(string) nick di registrazione in DB
        self.deaths = 0         #morti subite dal player (non incluso il changeteam)
        self.flood = 0          #numero di say in TempoControllo1
        self.guid = None        #(string) GUID
        self.guidage = 0        #eta della guid che sta usando
        self.hits = {"0":0, "1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "total":0}   #hit fatte dal player (0:head 1:helmet 2:torso 3:kevlar 4:arms 5:legs 6:body)
        self.ip = ""            #(string) IP
        self.isinDB = False     #Player esistente in DB.
        self.kills = {"12":0,"14":0,"15":0,"16":0,"17":0,"18":0,"19":0,"20":0,"21":0,"22":0,"23":0,"24":0,"25":0,"28":0,"30":0,"35":0,"38":0,"40":0}   #kill fatte dal player
        self.ks = 0             #killstreak
        self.ksmax = 0          #max killstreak
        self.lastconnect = 0    #data dell'ultimo connect
        #self.lastdisconnect = None                                         #data dell'ultimo disconnect
        self.level = 0          #livello di autorizzazione all'uso del RedCap
        self.location = ""      #locazione geografica del player
        self.justconnected = True                                           #e' appena entrato
        self.nick = ""          #nick (stringa)
        self.nickchanges = 0    #cambi nick in TempoControllo1
        self.notoriety = 0      #livello di reputazione (sale con anzianita guid, rounds, bonus admin, scende con warning, tempban, tk, malus admin). Calcolata alla connessione
        self.oldIP = ""         #IP usati precedentemente
        self.provider = ""      #provider
        self.reputation = 0     #reputazione assegnata dagli altri players o dal Redcap (salvata in DB)
        self.rounds = 0         #round giocati
        #self.rusher =0         #tempo totale di vita sul gameserver / tempo totale (da un'idea della bravura e camperosita)
        self.skill = 0.0        #skill
        self.skill_coeff = 1.0  #coefficiente di moltiplicazione skill che tende a 1 a round infiniti coeff = 1+[A/(round^C+B)]
        self.skill_var = 0.0    #variazione skill durante la mappa corrente?
        self.slot_id = None     #(string) slot id
        self.team = 0           #(string) 0=Sconosciuto 1=red, 2=blue, 3=spect
        self.tempban = 0        #data dell'ultimo tempban
        self.tobekicked = 0     #player da kikkare al prossimo controllo
        #self.totalplayedtime = 0                                           #tempo totale di gioco
        self.varie = []         #varie
        self.vivo = 0           #0=Sconosciuto 1=vivo, 2=morto #TODO mi interessa saperlo?
        self.warning = 0.0      #warning assegnati al player da admin o per TK o thit

    def alias_to_DB(self):
        """prepara gli alias per scrittura in db"""
        if self.alias == [[u'']]:
            return "0.0 unknown"
        joiner1 = " "
        joiner2 = "  "
        alias = ""
        for item in self.alias:
            al = item[0] + joiner1 + item[1]+ joiner2
            alias += al
        return alias.rstrip()           #tolgo gli spazi finali

    def load_dati(self, dati, N1, N2, time):
        """Aggiorna il player con i dati presi dal database tabella DATI"""
        self.DBnick = dati[1]                   #dati = (guid, DBnick, skill, rounds, lastconn, level, tempban, notoriety, firstconn, streak, alias, varie)
        self.skill = dati[2]
        self.rounds = dati[3]
        self.lastconnect = dati[4]              #data dell'ultima connessione
        self.level = dati[5]
        self.tempban = dati[6]
        self.guidage = (time - dati[8])/87400   #eta' della guid in giorni
        self.reputation = dati[7]
        self.notoriety = self.notoriety_upd(N1, N2)    #calcolo della notoriety (basata su round, guid age, e bonus/malus) - arrotondo a 1
        self.ksmax = dati[9]
        aliases = dati[10].split("  ")          #formatto gli alias in maniera leggibile
        for al in aliases:
            al=al.split(" ")
            self.alias.append(al)
        self.varie = dati[11].split()

    def load_loc(self, loc):                    #loc = (guid, IP, provider, location, old_ip)
        """aggiorna i dati presi dalla tabella loc"""
        if not loc[4] and self.ip:                              #campo vuoto
            self.oldIP = self.ip
            return
        else:
            self.oldIP = loc[4]                     #carico i vecchi IP
            if self.oldIP.find(self.ip) == -1:      #se non c'e l'IP lo aggiungo
                self.oldIP += " %s" %(self.ip)

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

    def notoriety_upd(self, roundXpoint, dayXpoint):
        """calcola la notoriety"""
        return round(self.rounds / roundXpoint + self.guidage / dayXpoint + self.reputation, 1)   #calcolo della notoriety (basata su round, guid age, e bonus/malus) - arrotondo a 1

    def skill_coeff_update(self):
        self.skill_coeff = 1 + (1000/(self.rounds**1.2 + 60))           #coefficiente skill che dipende dal n. di round giocati

    def stats (self):
        aliases = ""
        if self.alias == [['']]:
            self.alias = [['1318098208.58', self.nick],]  #alias vuoto per errore dovuto a crash
        for al in self.alias:          
            aliases += al[1] + " "
        aliases = aliases.rstrip()
        X = {
        1: self.nick,
        2: self.skill,
        4: self.skill_var,
        8: self.ksmax,
        16: self.rounds,
        32: self.notoriety,
        64: self.slot_id,
        128: self.DBnick,
        256: self.ip,
        512: self.level,
        1024: self.warning,
        2048:self.lastconnect,
        4096: aliases,
        }
        return X

    def varie_to_DB(self):
        """prepara le varie per scrittura in db"""
        varie = ""
        for item in self.varie:
            varie += item + " "
        return varie.rstrip()           #tolgo gli spazi finali
