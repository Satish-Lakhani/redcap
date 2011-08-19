#! /usr/bin/python
# -*- coding: utf-8 -*-

class Server:
    """Rappresenta il gameserver"""
    def __init__(self,parametri):
        self.AliasDuration = parametri["AliasDuration"]
        self.AntiRecon = parametri["AntiRecon"]                         #Stato del sistema antireconnect (bool)
        self.AntiReconInterval = parametri["AntiReconInterval"]         #Tempo minimo fra due connessioni
        self.Attivo = True                                              #TODO: da gestire. Presuppongo che il server sia up finche non provo il contrario
        self.AutoBalance = parametri["AutoBalance"]                     #modalita' di bilanciamento 0=disattivato 1=attivato 2=automatico
        self.Baseconf = parametri["Baseconf"]                           #config di base
        self.FloodControl = parametri["FloodControl"]                   #Flood control abilitato
        self.Full = False                                                               #Server pieno TODO da usare per kikkare gli spect o cose simili
        self.Gametype = ""                                                      #gametype
        self.MapName = ""                                                       #nome mappa corrente
        self.MatchMode = ""                                                   #stato matchmode
        self.MaxClients = ""                                                      #Numero massimo player
        self.MaxFlood = parametri["MaxFlood"]                           #massimo numero di say in un tempo fissato
        self.MaxNickChanges = parametri["MaxNickChanges"]               #massimi change nick in un tempo fissato
        self.MinNotoriety = parametri["MinNotoriety"]               #Notoriety minima per entrare nel server
        self.Nick_is_good = parametri["goodNick"]               #Nick ben formato
        self.Nick_is_length = parametri["minNick"]              #Lunghezza minima nick
        self.LastMapChange = 0                                   #Time al quale e' stato chiesto un cambio mappa
        self.LastVote = 0                                               #Time al quale e' stato chiesto l'ultimo voto
        self.Passport = parametri["Passport"]                           #1=passport attivo 0=passport inattivo.
        self.PT = {}                                                    #PlayerTable: dizionario che rappresenta i players presenti sul server e le loro caratteristiche
        self.RedCapStatus = 0                                           #stato RedCap (1=paused 0=attivo)
        self.Specialconf = False                                        #specifica se il server sta usando una config diversa da quella base
        self.Startup_end = False                                             #Se False il server e' in fase di avvio.
        self.TopScores = [0,0,0,0]                                      #Top scores del server
        self.TeamSkill = [0,0]                                          #skill media team red e blue
        self.TeamMembers = [0,0,0,0]                                    #players 0=sconosciuto, 1=red, 2=blue, 3=spect
        self.UrtPath = parametri["UrtPath"]                             #path relativo della cartella q3ut4 di urt
        self.VoteMode = False                                                 #indica se il voto e' abilitato

    def player_ADDINFO(self, info):                     #player (0=id, 1=ip, 2=guid)
        """Aggiunge IP e GUID al player"""
        self.PT[info[0]].ip = info[1]                                 #assegno IP
        self.PT[info[0]].guid = info[2]                             #assegno GUID

    def player_DEL(self, id):
        """Cancella un player dalla playertable"""
        self.TeamMembers[self.PT[id].team] -= 1         #lo elimino dal conto dei players
        del self.PT[id]

    def player_NEW(self, newplayer, id, conntime):
        """crea un nuovo player"""
        self.PT[id] = newplayer                        #creo il player
        self.PT[id].slot_id = id                          #assegno la slot
        self.TeamMembers[0] += 1                #assegno un player al team sconosciuti
        self.PT[id].lastconnect = conntime

    def teamskill_eval(self):
        """Calcola le teamskill dei red e dei blue"""
        tot_red_skill = 0
        tot_blue_skill = 0
        for pl in self.PT:
            if pl.team == "1":
                tot_red_skill += pl.skill
            elif pl.team == "2":
                tot_blue_skill += pl.skill
        self.TeamSkill[0] = tot_red_skill / self.TeamMembers[1]
        self.TeamSkill[0] = tot_blue_skill / self.TeamMembers[2]

    def userinfochanged(self, info):                            #info (0=id, 1=nick, 2=team)
        if self.PT[info[0]].team <> info[2]:                       #vedo se ha cambiato TEAM
            self.TeamMembers[self.PT[info[0]].team] -= 1  #lo tolgo dal vecchio team
            self.TeamMembers[int( info[2])] += 1              #lo metto nel nuovo team
            self.PT[info[0]].team = int( info[2])                  #gli assegno il nuovo team
        if self.PT[info[0]].nick <> info[1]:                        #controllo se cambia NICK
            self.PT[info[0]].nick =  info[1]
            self.PT[info[0]].nickchanges += 1                   #il controllo per i troppi nickchanges si fa da un'altra parte
            return True                                                     #il player ha cambiato nick


