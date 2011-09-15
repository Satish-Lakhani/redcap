import M_CONF
#! /usr/bin/python
# -*- coding: utf-8 -*-

import math


class Server:
    """Rappresenta il gameserver"""
    def __init__(self,parametri, sk_pars, warn_pars):
        self.AliasDuration = parametri["AliasDuration"]
        self.AntiReconInterval = parametri["AntiReconInterval"]         #Tempo minimo fra due connessioni
        self.Attivo = True                                              #TODO: da gestire. Presuppongo che il server sia up finche non provo il contrario
        self.BalanceMode = parametri["BalanceMode"]                     #modalita' di bilanciamento 0=disattivato 1=attivato 2=automatico
        self.BalanceRequired = False                                #e' stato richiesto un balance se True
        self.Baseconf = parametri["Baseconf"]                           #config di base
        #self.Banlist = []                                              #copia in memoria della table BAN
        self.FloodControl = parametri["FloodControl"]                   #Flood control abilitato
        self.Full = 1                                                         #0 = vuoto, 1= c'e gente 2= pieno (da usare per kikkare gli spect o cose simili)
        self.Gametype = ""                                              #gametype
        self.KsMin = sk_pars["Ks_min"]                                  #minima streak affinche' il bot segnali la killstreak
        self.KsNot = sk_pars["Ks_not"]                                  #minima notoriety per segnalazione killstreak
        self.Ks_show = sk_pars["Ks_show"]                               #minima ks per segnalazione in chat
        self.Ks_showbig = sk_pars["Ks_showbig"]                         #minima ks per segnalazione in bigtext
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
        self.Logfolder = parametri["Logfolder"]                         #cartella dei logs
        #self.Passport = parametri["Passport"]                          #1=passport attivo 0=passport inattivo.
        self.PT = {}                                                    #PlayerTable: dizionario che rappresenta i players presenti sul server e le loro caratteristiche
        self.RedCapStatus = 0                                           #stato RedCap (1=paused 0=attivo)
        self.Sbil = 1                                                   #coefficiente di sbilanciamento teams
        self.Server_mode = 0                                            #0 = fase avvio 1 = normale 2 = warmode
        self.Sk_Kpp = sk_pars["Sk_Kpp"]                                 #Sensibilita' skill: numero di kill (a delta skill 0) necessarie per guadagnare un punto skill.
        self.Sk_penalty = sk_pars["Sk_penalty"]                         #penalita' per teamkill (espressa come n. di kill da fare per bilanciare una penalty)
        self.Sk_range = sk_pars["Sk_range"]                             #Ampiezza curva skill:piu grande e' il valore, piu' alti sono i valori di skill che si possono raggiungere.
        self.Sk_team_impact = sk_pars["Sk_team_impact"]                 #frazione della skill calcolata sul team avversario, rispetto a quella calcolata sulla vittima
        self.TopScores = [[0.0, 0, " "],[0.0, 0, " "],[0.0, 0, " "],[0.0, 0, " "]]          #Top scores del server (alltime, month, week, day) (time, valore, DBnick)
        self.TeamSkill = [0,0]                                          #skill media team red e blue
        self.TeamSkillCoeff = 1                                         #coefficiente di bilanciamento per teams squilibrati
        self.TeamMembers = [0,0,0,0]                                    #players 0=sconosciuto, 1=red, 2=blue, 3=spect
        self.UrtPath = parametri["UrtPath"]                             #path relativo della cartella q3ut4 di urt
        self.VoteMode = False                                           #indica se il voto e' abilitato
        self.WarnMax = warn_pars["max_warns"]                           #valore di warning dopo di che vieni kikkato  (si azzerano al reconnect). Uno slap dati da Redcap o un tk o un hit comportano automaticamente un warning.
        self.WarnAdm = warn_pars["adm_warn"]                            #valore di uno warn dato da un admin
        self.WarnTk = warn_pars["tk_warn"]                              #valore di uno warn causato da un tk (in realta' un tk vale circa tk_warn + 3 hit_warn
        self.WarnHit = warn_pars["hit_warn"]                            #valore di uno warn dato da un team hit

    def is_kstreak(self, K, V, ora):
        """gestisce la killstreak"""
        res = 0
        self.PT[K].ks += 1                                              #controllo streak del killer
        if self.PT[K].ks >= self.Ks_showbig:
            res +=  1                                                   #killstreak: Annuncio in bigtext
        elif self.PT[K].ks >= self.Ks_show:
            res += 2                                                    #killstreak: Annuncio in console
        if self.PT[K].ks > self.PT[K].ksmax:
            self.PT[K].ksmax = self.PT[K].ks
            res += 4                                                    #killstreak: personal record
        if self.tot_players(1) >= M_CONF.MinPlayers and self.PT[K].notoriety > M_CONF.MinNotoriety:     #ci sono le condizioni per il record?
            dati = [ora, self.PT[K].ks, self.PT[K].DBnick]
            if self.PT[K].ks > self.TopScores[0][1]:
                self.TopScores = [dati, dati, dati, dati]   #killstreak: alltime record
                res += 8
            elif self.PT[K].ks > self.TopScores[1][1]:
                self.TopScores = [self.TopScores[0], dati, dati, dati]      #killstreak: monthly record
                res += 16
            elif self.PT[K].ks > self.TopScores[2][1]:
                self.TopScores = [self.TopScores[0], self.TopScores[1], dati, dati]         #killstreak: weekly record
                res += 32
            elif self.PT[K].ks > self.TopScores[3][1]:
                self.TopScores[3] = dati                                                                    #killstreak: daily record
                res += 64
        if self.PT[V].ks >= self.Ks_showbig:
           res += 128                                                   #Stop in bigtext
        elif self.PT[V].ks >= self.Ks_show:
           res += 256                                                   #Stop in console
        self.PT[V].ks = 0                                               #metto a zero la ks della vittima
        return res     

    def is_thit(self, K, V):
        """verifica se e stato fatto un thit e procede di conseguenza"""
        if self.PT[K].team == self.PT[V].team:
            self.PT[K].warning += self.WarnHit                           #aumento il warning
            return True

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

    def players_alive(self):
        """mette tutti i player non spect a vivo e gli assegna un round in piu e aggiorna il coefficiente di rapidita' variazione skill"""
        for player in self.PT:
            if self.PT[player].team < 3:         #se il player non e' spect
                self.PT[player].vivo = 1
                self.PT[player].rounds += 1
                self.PT[player].skill_coeff_update() #aggiorno il coefficiente skill

    def skill_variation(self, K, V):
        """calcola la variazione di skill dei players K e V in seguito alla kill"""
        if self.PT[V].team == 3:
            return                                                                      #A volte viene killato qualcuno che risulta spect
        D = self.PT[K].skill - self.PT[V].skill                                         #Delta skill tra i due player
        Dk = self.PT[K].skill - self.TeamSkill[(self.PT[V].team - 1)]                   #Delta skill Killer rispetto al team avversario
        Dv =  self.TeamSkill[(self.PT[K].team - 1)] -self.PT[V].skill                   #Delta skill Vittima rispetto al team avversario
        K_opponent_variation = (1- math.tanh(D / self.Sk_range)) / self.Sk_Kpp          #Variazione skill del Killer in base a skill vittima
        V_opponent_variation = (2 / self.Sk_Kpp - K_opponent_variation)                #Variazione skill della Vittima in base a skill killer
        KT_variation =  (1- math.tanh(Dk/self.Sk_range)) / self.Sk_Kpp                  #Variazione skill del Killer in base a skill team vittima
        VT_variation =  -(1- math.tanh(Dv/self.Sk_range)) / self.Sk_Kpp                 #Variazione skill della Vittima in base a skill team killer
        Dsk_K = self.Sbil * (self.Sk_team_impact * KT_variation + (1 - self.Sk_team_impact) * K_opponent_variation)     #delta skill del Killer
        Dsk_V = self.Sbil * (self.Sk_team_impact * VT_variation + (1 - self.Sk_team_impact) * V_opponent_variation)     #delta skill della vittima
        self.PT[K].skill += Dsk_K * self.PT[K].skill_coeff          #(nuova skill)
        self.PT[V].skill += Dsk_V * self.PT[V].skill_coeff          #(nuova skill)
        self.PT[K].skill_var += Dsk_K                               #(variazione skill da inizio connessione #TODO o per mappa?)
        self.PT[V].skill_var += Dsk_V                               #(variazione  skill da inizio connessione)
        return

    def team_balance(self):                                  #color = 1 muove red, 2 muove blu
        """esegue il bilanciamento pesato dei teams"""
        if self.TeamMembers[1] - self.TeamMembers[2] > 0:
            team_to_increase = " blue"
            team_to_reduce = 1
        else:
            team_to_increase = " red"
            team_to_reduce = 2
        skill_to_move = (self.TeamSkill[0] * self.TeamMembers[1] - self.TeamSkill[1] * self.TeamMembers[2]) / 2
        delta_min = 1000000.0                                         #valore sicuramente alto
        for player in self.PT:
            if self.PT[player].team == team_to_reduce:                       #e' del colore che devo muovere
                delta = self.PT[player].skill - skill_to_move
                if delta < delta_min:
                    delta_min = delta
                    target = player
        return target + team_to_increase

    def teamskill_eval(self):
        """Calcola le teamskill dei red e dei blue"""
        tot_red_skill = 0
        tot_blue_skill = 0
        for pl in self.PT:
            if self.PT[pl].team == "1":
                tot_red_skill += self.PT[pl].skill
            elif self.PT[pl].team == "2":
                tot_blue_skill += self.PT[pl].skill
        if self.TeamMembers[1]:
            self.TeamSkill[0] = tot_red_skill / self.TeamMembers[1]     #Team non vuoto
        if self.TeamMembers[2]:
            self.TeamSkill[1] = tot_blue_skill / self.TeamMembers[2]    #Team non vuoto
            self.Sbil = (float(self.TeamMembers[1]) / float(self.TeamMembers[2]))**0.75          #coefficiente di sbilanciamento teams

    def tot_players(self, X=0):     #X=0 tutti X=1 red+blue X=2 vivi
        """ritorna il numero di player sul server"""
        if X == 0:
            return len(self.PT)
        elif X == 1:
            return self.TeamMembers[1] + self.TeamMembers[2]
        elif X == 2:
            vivi =[]
            for pl in self.PT:
                if self.PT[pl].vivo == 1:
                    vivi[0] += 1
                    vivi[1].append(pl)
                    return vivi
                


