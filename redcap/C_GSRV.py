#! /usr/bin/python
# -*- coding: utf-8 -*-

import math


class Server:
    """Rappresenta il gameserver"""
    def __init__(self,parametri, sk_pars, warn_pars):
        self.AliasDuration = parametri["AliasDuration"]
        self.AntiReconInterval = parametri["AntiReconInterval"]         #Tempo minimo fra due connessioni
        self.Attivo = True                                              #TODO: da gestire. Presuppongo che il server sia up finche non provo il contrario
        self.AutoBalance = parametri["AutoBalance"]                     #modalita' di bilanciamento 0=disattivato 1=attivato 2=automatico
        self.Baseconf = parametri["Baseconf"]                           #config di base
        self.FloodControl = parametri["FloodControl"]                   #Flood control abilitato
        self.Full = False                                               #Server pieno TODO da usare per kikkare gli spect o cose simili
        self.Gametype = ""                                              #gametype
        self.KsMin = sk_pars["Ks_min"]                                  #minima streak affinche' il bot segnali la killstreak
        self.KsNot = sk_pars["Ks_not"]                                  #minima notoriety per segnalazione killstreak
        self.MapName = ""                                               #nome mappa corrente
        self.MatchMode = ""                                             #stato matchmode
        self.MaxClients = ""                                            #Numero massimo player
        self.MaxFlood = parametri["MaxFlood"]                           #massimo numero di say in un tempo fissato
        self.MaxNickChanges = parametri["MaxNickChanges"]               #massimi change nick in un tempo fissato
        self.MinNotoriety = parametri["MinNotoriety"]                   #Notoriety minima per entrare nel server
        self.Nick_is_good = parametri["goodNick"]                       #Nick ben formato
        self.Nick_is_length = parametri["minNick"]                      #Lunghezza minima nick
        self.LastMapChange = 0                                          #Time al quale e' stato chiesto un cambio mappa
        self.LastVote = 0                                               #Time al quale e' stato chiesto l'ultimo voto
        self.Logfolder = parametri["Logfolder"]
        #self.Passport = parametri["Passport"]                          #1=passport attivo 0=passport inattivo.
        self.PT = {}                                                    #PlayerTable: dizionario che rappresenta i players presenti sul server e le loro caratteristiche
        self.RedCapStatus = 0                                           #stato RedCap (1=paused 0=attivo)
        self.Sbil = 1                                                   #coefficiente di sbilanciamento teams
        self.Sk_Kpp = sk_pars["Sk_Kpp"]                                 #Sensibilita' skill: numero di kill (a delta skill 0) necessarie per guadagnare un punto skill.
        self.Sk_penalty = sk_pars["Sk_penalty"]                         #penalita' per teamkill (espressa come n� di kill da fare per bilanciare una penalty)
        self.Sk_range = sk_pars["Sk_range"]                             #Ampiezza curva skill:piu grande e' il valore, piu' alti sono i valori di skill che si possono raggiungere.
        self.Sk_team_impact = sk_pars["Sk_team_impact"]                 #frazione della skill calcolata sul team avversario, rispetto a quella calcolata sulla vittima
        self.Specialconf = False                                        #specifica se il server sta usando una config diversa da quella base
        self.Startup_end = False                                        #Se False il server e' in fase di avvio.
        self.TopScores = [0,0,0,0]                                      #Top scores del server
        self.TeamSkill = [0,0]                                          #skill media team red e blue
        self.TeamSkillCoeff = 1                                         #coefficiente di bilanciamento per teams squilibrati
        self.TeamMembers = [0,0,0,0]                                    #players 0=sconosciuto, 1=red, 2=blue, 3=spect
        self.UrtPath = parametri["UrtPath"]                             #path relativo della cartella q3ut4 di urt
        self.VoteMode = False                                           #indica se il voto e' abilitato
        self.WarnMax = warn_pars["max_warns"]                           #valore di warning dopo di che vieni kikkato  (si azzerano al reconnect). Uno slap dati da Redcap o un tk o un hit comportano automaticamente un warning.
        self.WarnAdm = warn_pars["adm_warn"]                            #valore di uno warn dato da un admin
        self.WarnTk = warn_pars["tk_warn"]                              #valore di uno warn causato da un tk (in realta' un tk vale circa tk_warn + 3 hit_warn
        self.WarnHit = warn_pars["hit_warn"]                            #valore di uno warn dato da un team hit

    def is_kstreak(self, K,V, stop = ""):
        """gestisce la killstreak"""
        pass

        


    def is_tkill(self, K, V):
        """verifica se e stato fatto un tkill e procede di conseguenza"""
        if self.PT[K].team == self.PT[V].team:
            self.PT[K].warning += self.WarnTk                           #aumento il warning
            self.PT[K].skill -= self.Sk_penalty /  self.Sk_Kpp          #penalizzo la skill
            self.PT[K].ks = 0                                           #gli azzero la streak
            return True

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

    def player_USERINFOCHANGED(self, info):                            #info (0=id, 1=nick, 2=team)
        if self.PT[info[0]].team <> info[2]:                       #vedo se ha cambiato TEAM
            self.TeamMembers[self.PT[info[0]].team] -= 1  #lo tolgo dal vecchio team
            self.TeamMembers[int( info[2])] += 1              #lo metto nel nuovo team
            self.PT[info[0]].team = int( info[2])                  #gli assegno il nuovo team
        if self.PT[info[0]].nick <> info[1]:                        #controllo se cambia NICK
            self.PT[info[0]].nick =  info[1]
            self.PT[info[0]].nickchanges += 1                   #il controllo per i troppi nickchanges si fa da un'altra parte
            return True                                                     #il player ha cambiato nick

    def skill_variation(self, K, V):
        """calcola la variazione di skill dei players K e V in seguito alla kill"""
        D = self.PT[K].skill - self.PT[V].skill                                         #Delta skill tra i due player
        Dk = self.PT[K].skill - self.TeamSkill[(self.PT[V].team - 1)]                         #Delta skill Killer rispetto al team avversario
        Dv =  self.TeamSkill[(self.PT[K].team - 1)] -self.PT[V].skill                          #Delta skill Vittima rispetto al team avversario
        K_opponent_variation = (1- math.tanh(D / self.Sk_range)) / self.Sk_Kpp         #Variazione skill del Killer in base a skill vittima
        V_opponent_variation = -(2 / self.Sk_Kpp - K_opponent_variation)                #Variazione skill della Vittima in base a skill killer
        KT_variation =  (1- math.tanh(Dk/self.Sk_range)) / self.Sk_Kpp              #Variazione skill del Killer in base a skill team vittima
        VT_variation =  -(1- math.tanh(Dv/self.Sk_range)) / self.Sk_Kpp              #Variazione skill della Vittima in base a skill team killer
        self.PT[K].skill += self.Sbil * (self.Sk_team_impact * KT_variation + (1 - self.Sk_team_impact) * K_opponent_variation) #(nuova skill)
        self.PT[V].skill += self.Sbil * (self.Sk_team_impact * VT_variation + (1 - self.Sk_team_impact) * V_opponent_variation) #(nuova skill)
        self.PT[K].skill_var += self.Sbil * (self.Sk_team_impact * KT_variation + (1 - self.Sk_team_impact) * K_opponent_variation) #(variazione skill da inizio connessione)
        self.PT[V].skill_var += self.Sbil * (self.Sk_team_impact * VT_variation + (1-  self.Sk_team_impact) * V_opponent_variation) #(variazione  skill da inizio connessione)
        return

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
        self.TeamSkill[1] = tot_blue_skill / self.TeamMembers[2]
        self.Sbil = (float(self.TeamMembers[self.PT[V].team]) / float(self.TeamMembers[self.PT[K].team]))          #coefficiente di sbilanciamento teams


