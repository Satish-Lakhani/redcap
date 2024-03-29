#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import re
import C_DB                                             #Classe che rappresenta il DB
import C_GSRV                                           #Classe che rappresenta il gameserver
import C_PLAYER                                         #Classe per creare players
import C_SOCKET                                         #Classe socket per comunicazione con UrT
import M_CMD                                            #Lista comandi
import M_CONF                                           #Carico le configurazioni programma
import M_SAYS                                           #dati ausiliari per gestire i say ed i comandi
import GEOIP.geoip                                      #geolocalizzazione
exec("import M_%s" %M_CONF.RC_lang)                     #importo modulo localizzazione linguaggio

versione = "1.23_(20120829)" 	                        #RedCap Version. !!! PLEASE ADD "-MOD by YOURNAME" TO THE VERSION NUMBER IF YOU MODIFY SOMETHING IN THE SCRIPT!!!

#Carico i moduli di lingua
Lang = eval( "M_%s.RC_outputs" %M_CONF.RC_lang)
Status = eval( "M_%s.RC_status" %M_CONF.RC_lang)
Logs = eval("M_%s.RC_logoutputs" %M_CONF.RC_lang)
Killz = eval("M_%s.RC_kills" %M_CONF.RC_lang)
Help_desc = eval("M_%s.RC_help" %M_CONF.RC_lang)

SCK = C_SOCKET.Sock()                                                                                   #Istanzio il socket
GSRV = C_GSRV.Server()                                                                                  #Istanzio il gameserver
DB = C_DB.Database(M_CONF.NomeDB)                                                                       #Istanzio il DB
GLC = GEOIP.geoip.GeoIP('GEOIP/GeoLiteCity.dat')                                                        #istanzio il geolocator

#DB.connetti()
#GSRV.Banlist= (DB.esegui("""SELECT * FROM BAN""")).fetchall()   #carico la banlist #TODO da scaricare periodicamente (spostare in modulo apposito?)
#DB.disconnetti()

##FUNZIONI INTERNE DEL REDCAP##
def balance_do():
    """esegue il bilanciamento"""
    moved = False
    if GSRV.BalanceMode == 3:                                                                           #modalita clan balance
        to_move = GSRV.team_clanbalance()
        for player in to_move[0]:                                                                       #sposto i red
            SCK.cmd("forceteam %s red" %GSRV.PT[player].slot_id)
            if not M_CONF.SV_silentmode:
                say("^5%s ^3moved to red because he is a ^5%s" %(GSRV.PT[player].nick, M_CONF.clanbalanceTag), 1)
            moved = True
        for player in to_move[1]:                                                                       #sposto i blu
            SCK.cmd("forceteam %s blue" %GSRV.PT[player].slot_id)
            if not M_CONF.SV_silentmode:
                say("^5%s ^3moved to blue because is not a ^5%s" %(GSRV.PT[player].nick, M_CONF.clanbalanceTag), 1)
            moved = True
        if moved:   #se ho fatto il bilanciamento di clan esco, se no  faccio quello normale.
            return moved
    if abs(GSRV.TeamMembers[1] - GSRV.TeamMembers[2]) > 1:  #Modalita normale: verifico se gli sbilanciamenti richiedono balance
        moving = GSRV.team_balance()
        SCK.cmd("forceteam " + moving)
        GSRV.BalanceRequired = False
        if not M_CONF.SV_silentmode:
            say(Lang["balancexecuted"], 1)
        moved = True
    return moved

def censura(frase):
    """Controlla se nella frase ci sono parole non ammesse"""
    testo=frase.replace(".","")                                                     #tolgo i punti dei furbetti.
    testo=testo.replace("_","")
    for insulto in M_SAYS.censura:
        if re.search(insulto,testo,re.I):                                           #ho trovato un insulto
            return True

def clientconnect(id):                                                              #TODO non serve se c'e' lo stesso in clientuserinfo
    """Gestisce un nuovo client"""
    if id not in GSRV.PT:                                                           #Se e un nuovo player (nel senso di appena entrato in game)
        newplayer = C_PLAYER.Player()                                               #lo creo
        GSRV.player_NEW(newplayer, id, time.time())                                 #lo aggiungo alla PlayerTable ed ai TeamMember

def clientdisconnect(id):
    """Operazioni da fare alla disconnessione"""
    if id not in GSRV.PT:
        return                                                                      #nel log raramente capitano anche 2 clientdisconnect dello stesso player di seguito
    if GSRV.PT[id].justconnected:
        GSRV.player_DEL(id)                                                         #se e' un justconnected non accettato per badnick o badguid non salvo nulla in db #TODO salvare IP per eventuale ban?
        return
    alias = GSRV.PT[id].alias_to_DB()
    varie = GSRV.PT[id].varie_to_DB()
    for PL in GSRV.PT:                                                              #pulisco i warning relativi a questo player in modo che un nuovo player con lo stesso slot non possa perdonare al suo posto.
        if GSRV.PT[id].slot_id in GSRV.PT[PL].warnings:
            del GSRV.PT[PL].warnings[GSRV.PT[id].slot_id]
    DB.connetti()
    DB.esegui(DB.query["salvadati"], (GSRV.PT[id].DBnick, GSRV.PT[id].skill, GSRV.PT[id].rounds, GSRV.PT[id].lastconnect, GSRV.PT[id].level, \
                                      GSRV.PT[id].tempban, GSRV.PT[id].reputation, GSRV.PT[id].ksmax,alias, varie, GSRV.PT[id].guid ))          #salvo in tabella DATI #TODO aggiustare relativa query
    ##12:knife 13:knife thrown 14:Beretta 15:DE 16:spas 17:UMP 18:Mp5k 19:LR300 20:G36 21:PSG1 22:HK69 23:Bleed 24:Kick 25:Nade 27:SR8 29:AK 30 33 35 36 37 39 deaths guid
    DB.esegui(DB.query["salvakills"],(GSRV.PT[id].kills['12'] + GSRV.PT[id].kills['13'], GSRV.PT[id].kills['14'], GSRV.PT[id].kills['15'], \
                                      GSRV.PT[id].kills['16'], GSRV.PT[id].kills['17'], GSRV.PT[id].kills['18'], GSRV.PT[id].kills['19'], \
                                      GSRV.PT[id].kills['20'], GSRV.PT[id].kills['21'], GSRV.PT[id].kills['22'] + GSRV.PT[id].kills['36'], \
                                      GSRV.PT[id].kills['23'], GSRV.PT[id].kills['24'], GSRV.PT[id].kills['25'], GSRV.PT[id].kills['27'], \
                                      GSRV.PT[id].kills['29'], GSRV.PT[id].kills['35'], GSRV.PT[id].kills['37'], GSRV.PT[id].kills['39'], \
                                      GSRV.PT[id].deaths, GSRV.PT[id].guid))                                                                    #salvo in tabella KILL #TODO aggiustare relativa query
    DB.esegui(DB.query["salvahit"], (GSRV.PT[id].hits['1'] + GSRV.PT[id].hits['4'], GSRV.PT[id].hits['5'] + GSRV.PT[id].hits['6'], \
                                     GSRV.PT[id].hits['7'] + GSRV.PT[id].hits['8'], GSRV.PT[id].hits['9'], GSRV.PT[id].guid))                   #salvo in tabella HIT #TODO aggiustare relativa query
    DB.esegui(DB.query["salvaloc"], (GSRV.PT[id].ip, GSRV.PT[id].provider, GSRV.PT[id].location, GSRV.PT[id].oldIP, GSRV.PT[id].guid))          #salvo locazioni
    #TODO salvare altre tabelle?
    DB.salva()
    DB.disconnetti()
    GSRV.player_DEL(id)

def clientuserinfo(info):                                                                               #info (0=slot_id, 1=ip, 2=guid 3=gears)
    if info[0] not in GSRV.PT:                                                                          #Se e un nuovo client
        newplayer = C_PLAYER.Player()                                                                   #lo creo
        GSRV.player_NEW(newplayer, info[0], time.time())                                                #lo aggiungo alla PlayerTable ed ai TeamMember
    if GSRV.PT[info[0]].justconnected:                                                                  #Se e un nuovo player
        GSRV.player_ADDINFO(info)                                                                       #gli aggiungo GUID, IP e location
        geoinfo = get_geoinfo(info[1])                                                                  #recupero le geoinfo
        GSRV.PT[info[0]].location = ("%s - %s") %(geoinfo[0], geoinfo[1])                               #geoinfo[0]=citta', geoinfo[1]=paese
    elif info[2] <> GSRV.PT[info[0]].guid:                                                              #CAMBIO GUID durante il gioco.
        if GSRV.Server_mode <> 2:                                                                       #non attivo esclusivamente in warmode
            GSRV.PT[info[0]].notoriety += M_CONF.Nt_guidchange                                          #gli abbasso la notoriety in proporzione
            scrivilog(" GUID CHANGE: Nick: " + str(GSRV.PT[info[0]].nick) + " DB Nick: " + str(GSRV.PT[info[0]].DBnick)  + " IP: " + str(GSRV.PT[info[0]].ip) + " Location: " + str(GSRV.PT[info[0]].location) +  " GUID: " + GSRV.PT[info[0]].guid + " CHANGED TO: " + info[2], M_CONF.badguid)
            kick("Redcap", info[0], Lang["guidchange"]%info[1])

def clientuserinfochanged(info):                                                                        #info (0=id, 1=nick, 2=team)
    res = GSRV.player_USERINFOCHANGED(info)                                                             #Aggiorno NICK e TEAM (se res True, il player ha cambiato nick (o e' nuovo)
    if GSRV.Server_mode == 0:                                                                           #controllo se e' finito lo startup
        if GSRV.TeamMembers[0] == 0:                                                                    #non ci sono player non assegnati ai teams
            if M_CONF.SV_silentmode:
                GSRV.Server_mode = 3                                                                    #Silentmode
            else:
                GSRV.Server_mode = 5                                                                    #Normale
                say(Lang["startupend"], 1)
    if GSRV.Server_mode <> 2:                                                                           #non attivo in warmode
        if GSRV.PT[info[0]].invalid_guid():                                                             #CONTROLLO VALIDITA GUID (adesso che ho pure il nick!)
            GSRV.PT[info[0]].notoriety += M_CONF.Nt_badguid                                             #abbasso la notoriety
            scrivilog("BADGUID: Nick " + str(GSRV.PT[info[0]].nick) + " DB Nick: " + str(GSRV.PT[info[0]].DBnick)  + " IP: " + str(GSRV.PT[info[0]].ip) + " Location: " + str(GSRV.PT[info[0]].location) + " GUID: " + GSRV.PT[info[0]].guid, M_CONF.badguid)
            kick("Redcap", info[0], Lang["invalidguid"]%info[1])                                        #e lo kikko  #TODO  registrare nick e ip in DB o in log
            return                                                                                      #inutile andare avanti
        if GSRV.PT[info[0]].invalid_nick(GSRV.Nick_is_length, GSRV.Nick_is_good, info[1]):              #CONTROLLO VALIDITA NICK (non ancora assegnato al player!)
            kick("Redcap", info[0], Lang["invalidnick"]%info[1])
            return                                                                                      #inutile andare avanti
    if GSRV.PT[info[0]].justconnected:                                                                  #PLAYER APPENA CONNESSO
        db_datacontrol(GSRV.PT[info[0]].guid, info[0])                                                  #controllo se il player esiste nel DB e ne recupero i dati (tb DATA) se no lo registro
        if GSRV.PT[info[0]].isinDB:                                                                     #se il player gia esisteva nel DB
            db_loccontrol(GSRV.PT[info[0]].guid, info[0])                                               #controllo la tabella LOC  #TODO caricare i dati anche dalle altre tables?
        if GSRV.Server_mode <> 2:                                                                       #non attivo in warmode
            if GSRV.PT[info[0]].tempban > time.time():                                                  #CONTROLLO BAN
                ban = time.strftime("%d.%b.%Y %H.%M", time.localtime(GSRV.PT[info[0]].tempban))
                kick("Redcap", info[0], Lang["stillban"]%(GSRV.PT[info[0]].nick, ban))
                return
            if (time.time() -  GSRV.PT[info[0]].lastconnect) < GSRV.AntiReconInterval:                  #CONTROLLO RECONNECT
                kick("Redcap", info[0], Lang["antirecon"]%(GSRV.PT[info[0]].nick, str( GSRV.AntiReconInterval)))
                return
            if "muted" in GSRV.PT[info[0]].varie:                                                       #CONTROLLO MUTED
                mute("Redcap",info[0])                                                                  #lo muto in quanto si e' disconnesso da muto
                tell(GSRV.PT[info[0]].slot_id, Lang["muted"]%GSRV.PT[info[0]].nick)
            if "protected" in GSRV.PT[info[0]].varie:                                                   #CONTROLLO PROTECTED nick .
                pass                                                                                    #TODO non più necessario in 4.2 con authed?
        GSRV.PT[info[0]].skill_coeff_update()                                                           #aggiorno il coefficiente skill
        GSRV.PT[info[0]].justconnected = False                                                          #non e piu nuovo
        if GSRV.Server_mode > 3:                                                                        #attivo solo in normal mode
            saluta(M_CONF.saluti, info[0])                                                              #chiamo la funzione che si occupa eventualmente di salutare il player
        GSRV.PT[info[0]].lastconnect = time.time()                                                      #aggiorno il lastconnect
    if res:                                                                                             #CONTROLLO ALIAS (solo per player NON nuovi. I justconnected si)
        esiste = False
        for alias in GSRV.PT[info[0]].alias:
            if info[1] in alias:
                esiste = True
                alias[0] = str(time.time())                                                             #se esiste aggiorno la data di ultimo utilizzo
        if not esiste:
            GSRV.PT[info[0]].alias.append([str(time.time()), info[1]])                                  #se non esiste lo aggiungo
            if len(GSRV.PT[info[0]].alias) >= M_CONF.maxAlias - 1:                                      #se ho gia troppi alias
                if GSRV.Server_mode <> 2 and M_CONF.SV_AntiFake:                                        #se non e in warmode e antifake attivo
                    if GSRV.PT[info[0]].notoriety > 2*M_CONF.Nt_MinNot_toplay:                          #se notoriety alta applico penalita de 50%
                        penalty = -1*GSRV.PT[info[0]].notoriety/2                                       #la dimezzo
                        GSRV.PT[info[0]].reputation += penalty
                    else:
                        penalty = -1*M_CONF.Nt_MinNot_toplay                                            #se notoriety bassa
                        GSRV.PT[info[0]].reputation += penalty
                    GSRV.PT[info[0]].notoriety = GSRV.PT[info[0]].notoriety_upd(M_CONF.Nt_roundXpoint, M_CONF.Nt_dayXpoint)   #aggiorno la notoriety
                    tell(info[0], Lang["newfake"] %(str(penalty), str(GSRV.PT[info[0]].notoriety)))

def comandi (frase):                                                                #frase [id, testo] (es: "2:31 say: 3 Nero: !slap Cobr4" diventa: ["3", "!slap Cobr4"]
    """processo il comando prima di inviarlo alla funzione specializzata"""
    if frase[0]not in GSRV.PT:                                                      #potrebbero partire dei say prima del ClientBegin, dando errore "KeyError: '0'
        return
    for comando in M_CMD.comandi:                                                   #comando ["nomecomando","regex", livello]
        res = re.search(comando[1], frase[1], re.I)                                 #Individuo il tipo di comando
        if res:                                                                     #Ho trovato un comando
            if comando[2] == -1:                                                    #non processo comandi disabilitati
                return
            elif comando[2] >= M_CONF.commandlogMinLevel:                           #se e' un comando importante lo registro nel commandlog
                scrivilog(Logs["command"] %(GSRV.PT[frase[0]].nick,  GSRV.PT[frase[0]].DBnick, GSRV.PT[frase[0]].level,  frase[1], comando[2]) , M_CONF.commandlog)
            if GSRV.PT[frase[0]].level < comando[2]:
                tell(frase[0], Lang["nolevel"] %(str(comando[2]), GSRV.PT[frase[0]].level)) #player non autorizzato
            else:
                eval("%s(frase[0],res)" %comando[0])                                #eseguo il comando e gli passo richiedente e parametri
            break
    if not res:
        tell(frase[0], Lang["wrongcmd"] )                                           #comando non riconosciuto

def cr_floodcontrol():
    """verifica (periodica) che nessun player abbia fatto flood"""
    for PL in GSRV.PT:
        if GSRV.PT[PL].flood >= GSRV.MaxFlood:
            GSRV.PT[PL].reputation += M_CONF.Nt_floodpenalty
            GSRV.PT[PL].notoriety = GSRV.PT[PL].notoriety_upd(M_CONF.Nt_roundXpoint, M_CONF.Nt_dayXpoint)   #aggiorno la notoriety
            kick("Redcap", GSRV.PT[PL].slot_id, Lang["flood"]%GSRV.PT[PL].nick)
        else:
            GSRV.PT[PL].flood = 0        #Se non e kikkato lo rimetto a zero

"""
def cr_full():
    clients = (GSRV.TeamMembers[0] + GSRV.TeamMembers[1] + GSRV.TeamMembers[2] + GSRV.TeamMembers[3])
    if clients == int(GSRV.MaxClients):                                                                 #faccio operazioni da SERVER PIENO
        GSRV.Full = 2
        return 2
    elif not clients:
        GSRV.Full = 0
        return 0
    else:
        GSRV.Full = 1
        return 1
"""

def cr_full():
    """verifica se il server e' pieno o vuoto"""
    clients = sum(GSRV.TeamMembers)
    if clients == int(GSRV.MaxClients):                                                                 #faccio operazioni da SERVER PIENO
        GSRV.Full = 2                                                                                   #flag server pieno
        if M_CONF.KickForSpace and GSRV.Server_mode >2:                                                 #Silent e normal mode
            for PL in GSRV.PT:
                if GSRV.PT[PL].team == 3 and GSRV.PT[PL].level < M_CONF.lev_admin:
                    GSRV.PT[PL].tobekicked = 4                                                          #non lo kikko subito ma gli mando un msg
                    tell(PL, Lang["space"]%GSRV.PT[PL].nick)
                    GSRV.Full = 1                                                                       #flag server con gente ma non pieno
    elif not clients:                                                                                   #faccio operazioni da SERVER VUOTO
        GSRV.Full = 0                                                                                   #flag server vuoto
        GSRV.MinNot_toplay = M_CONF.Nt_MinNot_toplay                                                    #rimetto la MinNot_toplay al valore base.
        if GSRV.Server_mode == 2:                                                                       #tolgo la configurazione war
            SCK.cmd("g_matchmode 0")
            SCK.cmd("exec %s" %GSRV.Baseconf)                                                           #eseguo la config di base
            scrivilog("War config removed", M_CONF.activity)
            if M_CONF.SV_silentmode:
                GSRV.Server_mode = 3                                                                    #Silentmode
            else:
                GSRV.Server_mode = 5                                                                    #Normale
            SCK.cmd("reload")
        if M_CONF.gameserver_autorestart == 2 and GSRV.Restart_when_empty:
            import os
            import sys
            os.system("./S_full_restart.sh")
            sleep(10)                                                                                   #aspetto che il server abbia restartato
            sys.exit() 
    else:
        GSRV.Full = 1
        GSRV.Restart_when_empty = True                                                                  #restartera' appena vuoto

def cr_nickrotation():
    """verifica (periodica) che nessun player abbia fatto nickrotation"""
    for PL in GSRV.PT:
        if GSRV.PT[PL].nickchanges > GSRV.MaxNickChanges:
            kick("Redcap", GSRV.PT[PL].slot_id, Lang["nickchanges"]%(GSRV.PT[PL].nick, GSRV.PT[PL].nickchanges))
        else:
            GSRV.PT[PL].nickchanges = 0        #Se non e' kikkato lo rimetto a zero

def cr_nukeall():
    pass    #TODO

def cr_notorietycheck():
    """controllo notoriety"""
    for PL in GSRV.PT:
        if GSRV.PT[PL].notoriety < GSRV.MinNot_toplay and GSRV.PT[PL].tobekicked == 0:  #false per evitare di spammare 2 volte
            tell(GSRV.PT[PL].slot_id, Lang["lownotoriety"]%(GSRV.PT[PL].nick, GSRV.PT[PL].notoriety, GSRV.MinNot_toplay))
            time_to_wait = (GSRV.MinNot_toplay - GSRV.PT[PL].notoriety) * M_CONF.Nt_dayXpoint
            tell(GSRV.PT[PL].slot_id, Lang["lownotoriety2"]%str(time_to_wait))
            GSRV.PT[PL].tobekicked = 1

def cr_recordErase():
    """cancella il o i record specificati se fuori periodo"""
    DB.connetti()
    if int(time.strftime("%j", time.localtime(GSRV.TopScores["Day"][0]))) <> int(time.strftime("%j", time.localtime())):     #il daily record e piu vecchio di un giorno
        GSRV.TopScores["Day"] = [0.0, 0, " "]
        DB.esegui(DB.query["saverecords"], ("0.0", "0", " ", "Day"))
        scrivilog("Daily record cleaned", M_CONF.activity)
    if int(time.strftime("%U", time.localtime(GSRV.TopScores["Week"][0]))) <> int(time.strftime("%U", time.localtime())):     #il weekly record e piu vecchio di una settimana
        GSRV.TopScores["Week"] = [0.0, 0, " "]
        DB.esegui(DB.query["saverecords"], ("0.0", "0", " ", "Week"))
        scrivilog("Weekly record cleaned", M_CONF.activity)
    if int(time.strftime("%m", time.localtime(GSRV.TopScores["Month"][0]))) <> int(time.strftime("%m", time.localtime())):     #il monthly record e piu vecchio di un mese
        GSRV.TopScores["Month"] = [0.0, 0, " "]
        DB.esegui(DB.query["saverecords"], ("0.0", "0", " ", "Month"))
        scrivilog("Monthly record cleaned", M_CONF.activity)
    DB.salva()
    DB.disconnetti()

def cr_spam():
    """spam periodici"""
    if GSRV.Server_mode < 5:
        return                                          #no spam in warmode e silentmode
    if len(GSRV.SpamList) == 0:
        return                                          #spamlist vuota
    else:
        say(str(GSRV.SpamlistIndex) + ": " + GSRV.SpamList[GSRV.SpamlistIndex], 0)       #spammo
    if GSRV.SpamlistIndex == len(GSRV.SpamList) - 1:    #Aumento l'index
        GSRV.SpamlistIndex = 0
    else:
        GSRV.SpamlistIndex += 1

def cr_tbkicked():
    """verifica se ce qualcuno da kikkare"""
    for PL in GSRV.PT:
        if GSRV.PT[PL].tobekicked == 0:
            continue
        if GSRV.PT[PL].tobekicked == 1:         #controllo tobekicked
            kick("Redcap", GSRV.PT[PL].slot_id)
            if not M_CONF.SV_silentmode:
                say(Lang["tbkicked"] %GSRV.PT[PL].nick, 0)
        elif GSRV.PT[PL].tobekicked == 2:       #kick per slot pieni
            if GSRV.PT[PL].team == 3:           #se e ancora spect lo kikko
                kick("Redcap", GSRV.PT[PL].slot_id)
                if not M_CONF.SV_silentmode:
                    say(Lang["spacekicked"] %GSRV.PT[PL].nick, 0)
            else:
                GSRV.PT[PL].tobekicked = 0      #e entrato in game
        elif GSRV.PT[PL].tobekicked <= 4:       # kick per slot pieni aspetto 2 tick
            GSRV.PT[PL].tobekicked -= 1         #diminuisco di un tick

def cr_unvote():
    """verifica (periodica) che il voto non sia rimasto attivo dopo il comando !v"""
    if GSRV.VoteMode and ((time.time() - GSRV.LastVote) > M_CONF.voteTime):
        GSRV.VoteMode = False
        SCK.cmd("g_allowVote " + str(M_CONF.unvoteType))     # disabilito il voto
        say(Lang["voteOFF"], 0)

def cr_warning():
    """verifica se qualche player ha troppi warning o se e tobekicked"""
    for PL in GSRV.PT:
        if GSRV.PT[PL].warnings["total"] >= GSRV.WarnMax:
            GSRV.PT[PL].reputation += M_CONF.Nt_warnpenalty
            GSRV.PT[PL].notoriety = GSRV.PT[PL].notoriety_upd(M_CONF.Nt_roundXpoint, M_CONF.Nt_dayXpoint)   #aggiorno la notoriety
            kick("Redcap", GSRV.PT[PL].slot_id, Lang["warning"]%GSRV.PT[PL].nick)

def db_datacontrol(guid,id):
    """Applicato ai player appena connessi: recupera i valori della tabella DATA, o se il player non e' registrato lo registra"""
    DB.connetti()
    dati = DB.esegui(DB.query["cercadati"], (guid,)).fetchone()     #PROVO A CARICARE da TABELLA DATI
    if dati:                                                        #IL PLAYER ESISTE IN DB recupero i dati (guid, DBnick, skill, rounds, lastconn, level, tempban, notoriety, firstconn, streak, alias, varie)
        GSRV.PT[id].isinDB = True                                   #esiste gia nel DB
        GSRV.PT[id].load_dati(dati, M_CONF.Nt_roundXpoint, M_CONF.Nt_dayXpoint, time.time())
    else:                                                               #IL PLAYER NON ESISTE IN DB: gli assegno i valori non ancora assegnati e lo registro inserendo guid e nick
        GSRV.PT[id].DBnick = GSRV.PT[id].nick                           #gli assegno il DBnick (potra' essere cambiato in seguito con il comando !nick)
        GSRV.PT[id].alias = [[str(time.time()), GSRV.PT[id].nick]]      #gli assegno il suo primo alias
        GSRV.PT[id].oldIP = GSRV.PT[id].ip                              #gli assegno il suo primo oldIP #TODO aggiungere data?
        alias = str(time.time()) + " " + GSRV.PT[id].nick               #alias scritto nella forma per database
        DB.esegui(DB.query["newdati"], (GSRV.PT[id].guid, GSRV.PT[id].nick, 0, 0, GSRV.PT[id].lastconnect, 0, 0.0, 0, time.time(), 0, alias, ""))
        DB.esegui(DB.query["newdeath"], (GSRV.PT[id].guid,))
        DB.esegui(DB.query["newhit"], (GSRV.PT[id].guid,))
        DB.esegui(DB.query["newkill"], (GSRV.PT[id].guid,))
        DB.esegui(DB.query["newloc"], (GSRV.PT[id].guid, GSRV.PT[id].ip, GSRV.PT[id].ip))    #gli salvo il suo primo IP e OLD_IP
        DB.salva()
    DB.disconnetti()
    if guid in M_CONF.AdminGuids:       #se e' admin gli do il massimo livello
         GSRV.PT[id].level = 100
         tell(GSRV.PT[id].slot_id, Lang["adminrights"]%GSRV.PT[id].nick)

def db_loccontrol(guid, id):    
    DB.connetti()
    loc = DB.esegui(DB.query["cercaloc"], (guid,)).fetchone()           # esiste in db (guid, IP, provider, location, old_ip)
    GSRV.PT[id].load_loc(loc)
    DB.disconnetti()

def endMap(frase):
    """operazioni da fare a fine mappa"""
    rank=[]                                             # CREAZIONE SKILL LIST
    for pl in GSRV.PT:
        if "muted" in GSRV.PT[pl].varie:
            GSRV.PT[pl].varie.remove("muted")           #tolgo la tag muted
        rank.append((GSRV.PT[pl].skill_var, GSRV.PT[pl].nick))
        GSRV.PT[pl].skill_var = 0                       #azzero la skill_var
    if GSRV.Server_mode <> 2 and M_CONF.EndmapSpam:         #non attivo in warmode e se EndmapSpam=False
        rank.sort()
        rank.reverse()
        if len(rank) > 4:                                   #se piu' di quattro player in game mostro solo i quattro migliori.
            rank = rank[0:4]
        say(Lang["bestplayers"], 0)
        while len(rank):
            p =rank.pop(0)
            say(Lang["mapskill"] %(p[1],round(p[0],2)), 0)   #spammo la classifica
        DB.connetti()
        DB.esegui(DB.query["saverecords"], (GSRV.TopScores["Alltime"][0], GSRV.TopScores["Alltime"][1], GSRV.TopScores["Alltime"][2], "Alltime"))              #salvo i records che siano cambiati o meno #TODO mettere in un cron?
        DB.esegui(DB.query["saverecords"], (GSRV.TopScores["Month"][0], GSRV.TopScores["Month"][1], GSRV.TopScores["Month"][2], "Month"))
        DB.esegui(DB.query["saverecords"], (GSRV.TopScores["Week"][0], GSRV.TopScores["Week"][1], GSRV.TopScores["Week"][2], "Week"))
        DB.esegui(DB.query["saverecords"], (GSRV.TopScores["Day"][0], GSRV.TopScores["Day"][1], GSRV.TopScores["Day"][2], "Day"))
        DB.salva()
        DB.disconnetti()
    endRound(frase)                                     #richiamo anche le solite operazioni da endround

def endRound(frase):
    if GSRV.Server_mode > 2:                                       #solo in modalita normale e silent. No war e no startup
        if GSRV.BalanceMode > 1 or GSRV.BalanceRequired:           #eseguo bilanciamento automatico o su richiesta
            res = balance_do()

def get_geoinfo(IP):
    """Ritorna Citta' e Paese"""
    #�,�,�,�,�,�,�,�,�,�,�,�,�,�,�,�,�
    repl = {"\xe0":"a",  "\xe1":"a", "\xe4":"a", "\xe8":"e", "\xe9":"e", "\xeb":"e", "\xec":"i", "\xed":"i", "\xef":"i", "\xf2":"o", "\xf3":"o", "\xf6":"o", "\xf9":"u", "\xfa":"u", "\xfc":"u","\xf1":"n","\xe7":"c"}       #sostituisco le lettere non ASCII
    ginfo = GLC.record_by_addr(IP)      #recupero le info dall'IP
    for L in repl:
        if L in ginfo["city"]:
            ginfo["city"] = ginfo["city"].replace(L, repl[L])
    b = unicode(ginfo["city"], errors='ignore')                     #se la lettera non ASCII non e' nel replacer, la ignoro.
    return (str(b), ginfo["country_code3"])

def hits(frase):                                                #del tipo ['1', '0', '3', '5'] Vittima, Killer, Zona, Arma (per il momento arma non e' utilizzato)
    if frase[0] not in GSRV.PT or frase[1] not in GSRV.PT:                         #in rari casi il player puo' essere hittato dopo clientdisconnect
        return
    if GSRV.is_thit(frase[1], frase[0]):               #controllo che non faccia THIT
        tell(GSRV.PT[frase[1]].slot_id, Lang["thit"] %str(GSRV.PT[frase[1]].warnings["total"]))  #TEAMHIT
        return
    else:                                                           #hit normale
        GSRV.PT[frase[1]].hits[frase[2]] += 1           #aggiungo una hit
        GSRV.PT[frase[1]].hits['total'] += 1            #aggiungo una hit al totale
        if GSRV.ShowHeadshots and int(frase[2]) < 5:    #se e' un headshot e lo devo spammare
            hs = GSRV.PT[frase[1]].hits['1'] + GSRV.PT[frase[1]].hits['4']
            perc = hs*100/GSRV.PT[frase[1]].hits['total']
            if not M_CONF.SV_silentmode:
                say(Lang["headshot"]%(GSRV.PT[frase[1]].nick, str(hs), str(perc)), 1)

def ini_addcfg(cfg):
    """aggiunge la cfg di base per la war alla cartella q3ut4"""
    basecfg = open(cfg, "r")
    contenuto = basecfg.read()                                                                          #leggo la baseconfig
    basecfg.close()
    destfile = open(M_CONF.SV_UrtPath + "/" + "RedCapWar.cfg", "w")
    destfile.write(contenuto)                                                                           #creo la baseconfig per war
    destfile.close()

def ini_clientlist():
    """Verifica che il gameserver sia attivo e trova i client gia collegati"""
    #list = []                                                                                          #TODO togliere se non serve
    Res = SCK.cmd("clientlist")
    if not Res[1]:                                                                                      #IL SERVER NON RISPONDE
        if GSRV.Attivo:                                                                                 #e' la prima volta che non risponde, lo metto a false e gli concedo 20 sec.
            GSRV.Attivo = False
            scrivilog("NO ANSWER FROM GAMESERVER", M_CONF.crashlog)
        else:                                                                                           #non risponde da almeno 20 sec
            GSRV.Server_mode = 0                                                                        #rimetto il server in configurazione di avvio
            for pl in GSRV.PT:
                clientdisconnect(GSRV.PT[pl].id)                                                        #disconnetto tutti i players
        GSRV.Attivo = False
        sleep(20)                                                                                       #aspetto 20 secondi e riprovo
        ini_clientlist()                                                                                #LOOP finchè non riceve risposta
        #return list                                                                                    #TODO togliere se non serve
    else:                                                                                               #IL SERVER HA RISPOSTO
        if not GSRV.Attivo:
            scrivilog("GAMESERVER IS RUNNING", M_CONF.crashlog)
            GSRV.Attivo = True
        list = Res[0].split("\n")                                                                       #List = GUID, SLOT, NICK
        if len(list) > 2:
            del(list[0])                                                                                #pulisco la risposta
            list.reverse()
            del(list[0])
            return list
        else:
            return False                                                                        #non ci sono players ma è attivo

def ini_clientadd(list):
    """aggiunge i players trovati con ini_clientlist"""
    if not list:                                                                                #lista vuota o non pervenuta. Il server è vuoto, quindi concludo l'avvio.
        if M_CONF.SV_silentmode:
            GSRV.Server_mode = 3                                                                #Silentmode
        else:
            GSRV.Server_mode = 5                                                                #Normal mode
        return
    for pl in list:                                                                             #aggiungo i nuovi players
        dati = pl.split()
        newplayer = C_PLAYER.Player()                                                           #lo creo
        GSRV.player_NEW(newplayer,dati[1], time.time())                                         #lo aggiungo alla PlayerTable ed ai TeamMember
        GSRV.PT[dati[1]].guid = dati[0]
        GSRV.PT[dati[1]].nick = dati[2]
        db_datacontrol(dati[0], dati[1])                                                        #carico i dati se esistono
        if not M_CONF.SV_silentmode:
            say(Lang["caricoplayer"]%str(GSRV.PT[dati[1]].nick), 1)
        GSRV.PT[dati[1]].skill_coeff_update()                                                   #aggiorno il coefficiente skill
        GSRV.PT[dati[1]].justconnected = False                                                  #non e piu nuovo
        GSRV.PT[dati[1]].lastconnect = time.time()                                              #aggiorno il lastconnect

def ini_recordlist():
    """recupera i record dal db"""
    DB.connetti()
    dati = DB.esegui(DB.query["getrecords"]).fetchall()
    DB.disconnetti()
    for element in dati:                                                                                #TIPO VAL TIME OWNER
        GSRV.TopScores[element[0]][0] = float(element[2])                                               #time
        GSRV.TopScores[element[0]][1] = element[1]                                                      #val
        GSRV.TopScores[element[0]][2] = element[3]                                                      #owner

def ini_spamlist():
    """carica la lista spam"""
    if M_CONF.CustomSpam:
        buf = open(M_CONF.SpamFile, "r")
        spam = buf.read().split("\n")
        buf.close()
        GSRV.SpamList = spam
    if M_CONF.RecordSpam:
        GSRV.SpamList.append("^2RedCap ^4%s ^2by Lebbra! #" %versione)
        GSRV.SpamList.append(Lang["top"]%("Alltime", str(GSRV.TopScores["Alltime"][1]), str(GSRV.TopScores["Alltime"][2]), time.strftime("%d.%b %H.%M.%S", time.localtime(float(GSRV.TopScores["Alltime"][0])))))
        GSRV.SpamList.append(Lang["top"]%("Month", str(GSRV.TopScores["Month"][1]), str(GSRV.TopScores["Month"][2]), time.strftime("%d.%b %H.%M.%S", time.localtime(float(GSRV.TopScores["Month"][0])))))
        GSRV.SpamList.append(Lang["top"]%("Week", str(GSRV.TopScores["Week"][1]), str(GSRV.TopScores["Week"][2]), time.strftime("%d.%b %H.%M.%S", time.localtime(float(GSRV.TopScores["Week"][0])))))
        GSRV.SpamList.append(Lang["top"]%("Day", str(GSRV.TopScores["Day"][1]), str(GSRV.TopScores["Day"][2]), time.strftime("%d.%b %H.%M.%S", time.localtime(float(GSRV.TopScores["Day"][0])))))

def initGame(frase):    # frase (0=matchmode, 1=gametype, 2=maxclients, 3=mapname)
    """Operazioni da fare a inizio mappa"""
    GSRV.MatchMode = frase[0]               #recupero le modalita' server
    GSRV.Gametype = frase[1]
    GSRV.MaxClients = frase[2]
    GSRV.MapName = frase[3]
    GSRV.MapTime = time.time()    #time di inizio mappa
    initRound(frase)                        #richiamo anche le solite operazioni da initround

def initRound(frase):
    """attivita da fare ad inizio round"""
    if GSRV.Server_mode > 2:                                        #solo in modalita normale. No war e no startup
        GSRV.teamskill_eval()                                       #aggiorno le teamskill e il coefficiente di sbilanciamento skill
        GSRV.players_alive()                                        #setto i player non spect a vivo, gli aggiungo un round e updato il coeff skill.
        if (GSRV.MapName + "\n") in GSRV.Q3ut4["mapcycle"]:         #verifico qual'e la prossima mappa
            indice_nextmap = GSRV.Q3ut4["mapcycle"].index(GSRV.MapName+ "\n") +1
            if indice_nextmap == len(GSRV.Q3ut4["mapcycle"]):
                indice_nextmap = 0
            nextmap = GSRV.Q3ut4["mapcycle"][indice_nextmap]
            if not M_CONF.SV_silentmode:
                ini_say = "^1%s^4%s^2%s^8%s ^3Sk:^1(%s)^7-^4(%s) ^3- Nextmap: ^7%s" %(str(GSRV.TeamMembers[1]), str(GSRV.TeamMembers[2]), str(GSRV.TeamMembers[3]), str(GSRV.TeamMembers[0]), str(int(GSRV.TeamSkill[0])), str(int(GSRV.TeamSkill[1])), nextmap)
                say(ini_say, 1)
    elif GSRV.Server_mode == 0:
        say(Lang["startup"], 1)

##Parametri per le kill
normalKills = ['12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '27', '29', '30', '33', '35', '36', '37', '38', '39']
accident = ['1', '3', '5', '6', '9']
suicide = '7'
changeteam = '10'
adminkill = ['31', '32', '34']

def kills(frase):                                                                                       #frase del tipo ['0', '1', '16'] (K,V,M)
    if frase[0] not in GSRV.PT or frase[1] not in GSRV.PT:                                              #in rari casi il player puo' essere hittato dopo clientdisconnect
        return
    GSRV.PT[frase[1]].vivo = 2                                                                          #in ogni caso setto la vittima a "morto"
    if frase[2] == '10':                                                                                #CHANGETEAM  #TODO gestire il changeteam  se necessario
        return
    elif frase[2] in adminkill:                                                                         #Killato da ADMIN #todo da gestire
        return
    elif frase[2] in accident:                                                                          #INCIDENTE
        GSRV.PT[frase[1]].deaths += 1                                                                   #aumento di 1 le deaths alla vittima
        if not M_CONF.SV_silentmode:
            say(Lang["accident"]%GSRV.PT[frase[1]].nick, 0)
    elif frase[2] == suicide:                                                                           #SUICIDIO
        GSRV.PT[frase[1]].deaths += 1                                                                   #aumento di 1 le deaths alla vittima
        GSRV.PT[frase[1]].skill -= 2 * GSRV.PT[frase[1]].skill_coeff * GSRV.Sk_penalty / GSRV.Sk_Kpp    #penalizzo la skill
        tell(frase[1], Lang["suicide"]%str(round(2 * GSRV.Sk_penalty / GSRV.Sk_Kpp, 2)))
    elif frase[2] in normalKills :                                                                      #KILL NORMALE DA ARMA
        GSRV.PT[frase[1]].deaths += 1                                                                   #aumento di 1 le deaths alla vittima
        if GSRV.is_tkill(frase[0], frase[1]):
            if M_CONF.SV_Death_punish == 1 and GSRV.PT[frase[0]].vivo:                                  #applico death punish solo a player vivi
                smite("Redcap", frase[0], Lang["punishtodeath"]%(GSRV.PT[frase[0]].nick, GSRV.PT[frase[1]].nick))                                        #condanno a morte :-)
            tell(GSRV.PT[frase[0]].slot_id, Lang["tkill"] %str(GSRV.PT[frase[0]].warnings["total"]))    #Annuncia penalità per TK
            GSRV.PT[frase[0]].ks = 0                                                                    #gli interrompo la kstreak
            return
        if GSRV.tot_players(1) >= M_CONF.MinPlayers:                                                    #Skill attiva solo se ci sono abbastanza players
            GSRV.skill_variation(frase[0],frase[1])                                                     #funzione che calcola ed assegna la variazione skill ai due players
        GSRV.PT[frase[0]].kills[frase[2]] += 1                                                          #aggiungo la kill alle statistiche
    else:
        return
    #TODO semplificare questa parte usando if GSRV.tot_players(1) >= M_CONF.MinPlayers
    res0 = GSRV.is_kstreak(frase[0],frase[1], time.time())                                              #calcolo variazioni kstreak (eventuale spam)
    res = option_checker(res0)                                                                          #Separo le opzioni di ritorno
    kz = GSRV.PT[frase[0]].ks                                                                           #n. della frase di kstreak da spammare
    if kz > len(Killz)-1:                                                                               #streak piu lunga del vettore "commenti alle kill"
        kz = len(Killz)-1                                                                               #uso l'ultima stringa.
    if 1 in res:                                                                                        #spammo ks in bigtext
        if not M_CONF.SV_silentmode:
            say(Killz[kz]%GSRV.PT[frase[0]].nick, 2)
    elif 2 in res:                                                                                      #spammo ks in console
        if not M_CONF.SV_silentmode:
            say(Killz[kz]%GSRV.PT[frase[0]].nick, 0)
    if 4 in res:
        if not M_CONF.SV_silentmode:
            say(Lang["record_personal"]%(str(GSRV.PT[frase[0]].nick), str(GSRV.PT[frase[0]].ks)), 0)    #spammo personal record in console
    if 8 in res:
        say(Lang["record_alltime"]%(str(GSRV.PT[frase[0]].nick), str(GSRV.PT[frase[0]].ks)), 2)         #spammo alltime record
        ini_spamlist()                                                                                  #aggiorno la lista spam
    elif 16 in res:
        say(Lang["record_monthly"]%(str(GSRV.PT[frase[0]].nick), str(GSRV.PT[frase[0]].ks)), 2)         #spammo monthly record
        ini_spamlist()                                                                                  #aggiorno la lista spam
    elif 32 in res:
        say(Lang["record_weekly"]%(str(GSRV.PT[frase[0]].nick), str(GSRV.PT[frase[0]].ks)), 2)          #spammo weekly record
        ini_spamlist()                                                                                  #aggiorno la lista spam
    elif 64 in res:
        say(Lang["record_daily"]%(str(GSRV.PT[frase[0]].nick), str(GSRV.PT[frase[0]].ks)), 2)           #spammo daily record
        ini_spamlist()                                                                                  #aggiorno la lista spam
    elif 512 in res:
        if not M_CONF.SV_silentmode:
            say(Lang["record_no_not"]%str(GSRV.PT[frase[0]].nick), 0)                                   #notoriety bassa
    elif 1024 in res:
        if not M_CONF.SV_silentmode:                                                                    #Evito di ripetere la frase quando non esiste record #todo verificare se funziona
            if GSRV.TopScores["Day"][1] > 0:
                say(Lang["record_no_ppl"]%(M_CONF.MinPlayers, str(GSRV.PT[frase[0]].nick)), 0)          #poca gente
    if 128 in res:
        if not M_CONF.SV_silentmode:
            say(Killz[0]%(str(GSRV.PT[frase[0]].nick), str(GSRV.PT[frase[1]].nick)), 2)                 #spammo stop ks in bigtext
    elif 256 in res:
        if not M_CONF.SV_silentmode:
            say(Killz[0]%(str(GSRV.PT[frase[0]].nick), str(GSRV.PT[frase[1]].nick)), 0)                 #spammo stop ks in console


def option_checker(v):
    """serve per estrarre le opzioni in base 2 da un numero"""
    option = []
    n = 0
    go = False
    if v > 0:
        go = True
    while go:
        while v > 0:
            if v >= 2**n:
                n +=1
            else:
                option.append(2**(n-1))
                v -= 2**(n-1)
                n = 0
                if v == 0:
                    go = False
    return option
    
def saluta(modo, id):
    """si occupa di salutare il player al suo ingresso in game"""
    if GSRV.Server_mode < 5:                               #non attivo in warmode e silentmode
        return
    stat = GSRV.PT[id].stats()
    if 2048 in stat:
        stat[2048] = time.strftime("%d.%b.%Y %H.%M", time.localtime(stat[2048]))        #trasformo il tempo universale in leggibile
    opzioni = option_checker(modo)
    saluto = ""
    while opzioni:
        opz = opzioni.pop()
        saluto += Status[opz]%stat[opz]
    say(saluto, 0)

def say(testo,modo):
    """Manda messaggi pubblici da console. 0=say, 1=console, 2=bigtext"""
    modi= {
    0 : 'say "',
    1 : '"',
    2 : 'bigtext "'}
    SCK.cmd(modi[modo] + testo + '"')
   
def says(frase):                 #frase (0=id, 1=testo)
    if frase[0]not in GSRV.PT:   #potrebbero partire dei say prima del ClientBegin, dando errore "KeyError: '0'
        return
    GSRV.PT[frase[0]].flood += 1
    if censura(frase[1]):                              #ho trovato un insulto
        GSRV.PT[frase[0]].warn("Redcap", 1)      #lo warno
        grace = GSRV.WarnMax - GSRV.PT[frase[0]].warnings["total"] #warning rimasti
        slap("Redcap", (1, frase[0]), Lang["insults"]%grace)   #lo slappo

def scrivilog(evento, nomelog):          
    """scrive il messaggio "evento" nel file di log di RedCap"""
    evento = (time.strftime("%d.%b %H.%M.%S", time.localtime()) + ": " + evento + "\r\n")
    f = open(GSRV.Logfolder + "/" + nomelog, "a")
    f.write(evento)
    f.close()

def sleep(tempo):
    time.sleep(tempo)

def tell(target,testo):
    """Invia un messaggio privato a target. Equivalente a "tell" da console. """
    SCK.cmd("tell " + target + " " + testo)
            
def trovaslotdastringa(richiedente, stringa):
    """recupera lo slot del target dalla stringa"""
    slot = []
    if stringa.isdigit() and richiedente == "Redcap":       #comando chiamato da Redcap
        return stringa                                      #comando chiamato tramite routine interna
    if stringa.startswith("#"):                             #se inizia con cancelletto sto chiamando un clientnumber
        stringa = stringa.lstrip("#")
        return stringa                                      #ritorno un clientnumber
    for PL in GSRV.PT:
        if str.lower(GSRV.PT[PL].nick).find(str.lower(str.strip(stringa))) != -1: #porto tutto in minuscole e confronto
            slot.append(GSRV.PT[PL].slot_id)
    if len(slot) == 1:
        return slot[0]                                      #ritorno lo slot se e' univoco
    else:
        tell(richiedente, Lang["nocleartarget"])            #lo slot non esiste o ne esiste piu di uno corrispondente al pezzo di nome. Se il nome e' ambiguo avverto ed esco
        return ""                                          

#####################################
## FUNZIONI CHIAMABILI DAL PLAYER  ##
#####################################

def alias(richiedente, parametri):      #FUNZIONA
    """espone gli alias di un player"""
    target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():
        if GSRV.PT[target].alias == [[u'']]:
            GSRV.PT[target].alias = [[str(time.time()), str(GSRV.PT[target].nick)],]  #alias vuoto per errore dovuto a crash
        alias = GSRV.PT[target].alias
        frase = Lang["alias"]%str(GSRV.PT[target].nick)
        i = 0
        for al in alias:
            i += 1
            frase += "^%s" %str(i) + str(al[1]) + ", "
            if i == 3:
                tell(richiedente, frase)
                frase = ""
                i = 0
        if i <> 0:
                tell(richiedente, frase)

def balance(richiedente, parametri):    #FUNZIONA
    """richiede il bilanciamento dei teams"""
    if GSRV.BalanceMode == 0:                                   #balance non attivo
        tell(richiedente, Lang["balanceoff"])
        return
    elif GSRV.BalanceMode == 1:                                #blanciamento manuale
        if GSRV.Gametype == "7" and GSRV.Server_mode > 2:                                  #bilanciamento immediato in CTF #TODO da testare e aggiornare wiki
            balance_do()
        else:
            tell(richiedente, Lang["balancemanual"])
            GSRV.BalanceRequired = True
        return
    elif GSRV.BalanceMode == 2:                             #bilanciamento automatico
        if GSRV.Gametype == "7" and GSRV.Server_mode > 2:                                  #bilanciamento immediato in CTF #TODO da testare
            balance_do()
        else:
            tell(richiedente, Lang["balanceauto"])
        return
    elif GSRV.BalanceMode == 3:                             #bilanciamento clanmode
        if GSRV.Gametype == "7" and GSRV.Server_mode > 2:                                  #bilanciamento immediato in CTF #TODO da testare
            balance_do()
        else:
            tell(richiedente, Lang["balanceclan"])
        return

def balancemode(richiedente, parametri): #FUNZIONA
    """setta il balancemode"""
    bmode = { 0:"OFF", 1:"Manual", 2:"Auto",  3: M_CONF.clanbalanceTag + " mode" }
    if GSRV.BalanceMode == 0:
        GSRV.BalanceMode = 1
        say(Lang["balancemode"]%bmode[GSRV.BalanceMode], 2)
    elif GSRV.BalanceMode == 1:
        GSRV.BalanceMode = 2
        say(Lang["balancemode"]%bmode[GSRV.BalanceMode], 2)
    elif GSRV.BalanceMode == 2:
        GSRV.BalanceMode = 3
        say(Lang["balancemode"]%bmode[GSRV.BalanceMode], 2)
    else:
        GSRV.BalanceMode = 0
        say(Lang["balancemode"]%bmode[GSRV.BalanceMode], 2)

def ban(richiedente, parametri):
    """banna/sbanna in maniera definitiva"""
    if parametri.group("un") == "un":
        DB.connetti()
        res = DB.esegui(DB.query["unban"],(parametri.group("target"),))
        if res.rowcount == 0:
            tell(richiedente, Lang["noIDfound"])    #l'ID non esiste
            DB.disconnetti()
            return
        res = DB.esegui(DB.query["getIPs"],(parametri.group("target"),)).fetchall() #l'ID esiste
        DB.salva()
        DB.disconnetti()
        ips = res[0][0].split()
        if len(ips) == 0:   #TODO necessario?
            return
        for ip in ips:
            SCK.cmd("removeIP " + str(ip))  #sbanni gli IP
        tell(richiedente, Lang["unbandone"])    #l'ID sbannato
        return
    target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():
        say(Lang["ban"] %GSRV.PT[target].nick, 2)
        time.sleep(1)
        GSRV.PT[target].tempban = time.time() + 63072000   #ban per 2 anni
        #TODO verificare se fare banlist da tenere in memoria (da pulire per i ban vecchi)
        SCK.cmd("addIP " + GSRV.PT[target].ip)      #lo banno
        SCK.cmd("kick " + target)                   #lo kikko (al clientdisconnect si aggiorna il tempban)

def callvote(richiedente, parametri):
    """Chiama il voto di vario tipo"""
    if time.time() - GSRV.MapTime < 60:
        tell(richiedente, Lang["notimefromini"])
        return
    past = (time.time() - GSRV.LastVote)/60
    if  past < M_CONF.timeBetweenVote:               #controllo se e' passato tempo sufficiente
        say(Lang["notimetocmd"] %(int(M_CONF.timeBetweenVote - past)), 0)   #se non e' trascorso il tempo informo di aspettare
    else:
        SCK.cmd("g_allowVote " + str(M_CONF.voteType))     # abilito il voto
        say(Lang["voteON"] %(M_CONF.voteTime), 0)
        GSRV.LastVote = time.time()                          #aggiorno il time di ultima votazione
        GSRV.VoteMode = True                                       #il voto e' abilitato

def cyclemap(richiedente, parametri):   #FUNZIONA
    """esegue un cyclemap. Non si puo' dare piu spesso di RCconf.Tcyclemap"""
    past = (time.time() - GSRV.LastMapChange)/60
    if  past < M_CONF.Tcyclemap:
        tell(richiedente, Lang["notimetocmd"] %(int(M_CONF.Tcyclemap - past)))   #se non e' trascorso il tempo informo di aspettare
    else:
        GSRV.LastMapChange = time.time()
        SCK.cmd("cyclemap")

def dbfind(richiedente, parametri): #find a player in DB (for future use)
    """cerca un player in DB e restituisce info"""
    nomex = "%" + parametri.group("target") + "%"
    DB.connetti()
    res = DB.esegui(DB.query["findplayer"],(nomex,)).fetchall()
    DB.disconnetti()
    if len(res) > 4:
        tell(richiedente, Lang["toomanyres"] %(str(len(res))))
    else:
        for pl in res:
            if parametri.group("target").lower() in pl[1].lower():
                outp = "^3ID ^6%s: ^5%s" %(str(pl[0]), str(pl[1]))
            else:
                pat=r"(?P<nome>\S*" + parametri.group("target") + "\S*)"
                n = re.search(pat, pl[2], re.I)
                outp = "^3ID ^6%s: ^4%s, ^3alias ^5%s" %(str(pl[0]),str(pl[1]), str(n.group("nome")))
            tell(richiedente, outp)

def dbnick(richiedente, parametri): #FUNZIONA #TODO aggiungere verifica se esistente ed eventuale merge
    """rende il DBnick uguale al nick corrente"""
    target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():
        GSRV.PT[target].DBnick = GSRV.PT[target].nick
        tell(richiedente, Lang["dbnick"]%GSRV.PT[target].nick)
        tell(target, Lang["dbnick"]%GSRV.PT[target].nick)

def esegui(richiedente, parametri):     #FUNZIONA
    """esegue un qualsiasi comando rcon"""
    SCK.cmd(parametri.group("cmd"))
    tell (richiedente, Lang["executed"]%(parametri.group("cmd")))

def forceteam(richiedente, parametri):  #FUNZIONA
    """forza il player target in un team o spect"""
    if richiedente == "Redcap":                                 #force richiesto direttamente dal RedCap
        target = parametri[0]
        team = parametri[1]
    else:
        team = {"r":"red","b":"blue","s":"spectator"}[parametri.group("team").lower()]
        target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():
        SCK.cmd("forceteam " + target + " " + team)

def forgive(richiedente, parametri):
    """Perdona il player target per tk o thit"""
    if parametri.group("target") == "":                     #comando status senza target: perdono tutti
        for player in GSRV.PT:
            if GSRV.PT[richiedente].slot_id in GSRV.PT[player].warnings:        #ha qualcosa da perdonare
                GSRV.PT[player].warnings["total"] -= GSRV.PT[player].warnings[GSRV.PT[richiedente].slot_id] #sottraggo dal totale
                del GSRV.PT[player].warnings[GSRV.PT[richiedente].slot_id]  #cancello i warning causati dal richiedente
        tell(richiedente, Lang["forgivenall"])
        return
    target = trovaslotdastringa(richiedente, parametri.group("target"))
    if not target.isdigit():
        return
    if GSRV.PT[richiedente].slot_id in GSRV.PT[target].warnings:        #ha qualcosa da perdonare
        GSRV.PT[target].warnings["total"] -= GSRV.PT[target].warnings[GSRV.PT[richiedente].slot_id] #sottraggo dal totale
        del GSRV.PT[target].warnings[GSRV.PT[richiedente].slot_id]  #cancello i warning causati dal richiedente
        tell(richiedente, Lang["forgiven"] %GSRV.PT[target].nick)
    else:
        tell(richiedente, Lang["forgivenone"] %GSRV.PT[target].nick)

def forgiveall(richiedente, parametri):
    """Perdona totalmente il player"""
    target = trovaslotdastringa(richiedente, parametri.group("target"))
    if not target.isdigit():
        return
    GSRV.PT[target].warnings = {"total": 0.0}   #pulisco tutto
    tell(richiedente, Lang["forgiven"] %GSRV.PT[target].nick)

def help(richiedente, parametri):
    """Mostra i comandi disponibili per il dato player"""
    if not parametri.group("cmd"):                                                                                      #comando help senza target: do lista comandi
        avail_cmd = []
        num = 0                                                                                                         #comandi appesi
        answ = ""
        for comando in M_CMD.comandi:
            if GSRV.PT[richiedente].level >= comando[2]:
                answ += "^6%s^3-"%comando[3]
                num +=1
                if num > 10:
                    answ = Lang["youcanuse"] + answ
                    tell(richiedente, answ)
                    answ = ""
                    num= 0
        answ = Lang["youcanuse"] + answ
        tell(richiedente, answ)
        tell(richiedente, Lang["moreinfo"])
    else:                                                                                                               #comando help con target
        if parametri.group("cmd") in Help_desc:
            answ = "^6%s^3%s"%(parametri.group("cmd"), Help_desc[parametri.group("cmd")])
        else:
            tell(richiedente, Lang["wrongcmd"])
            return
        tell(richiedente, answ)

#Lista armi:
gearlist = [1, 2, 3, 4, 5, 6, 8, 9, 10, 14, 15, 17, 19]                                                 #lista delle hit
def gears(richiedente, parametri):
    """definisce quali armi e possibile utilizzare"""
                                              #TODO (poi fare gearcontrol che all'infochange controlla se hai preso armi non ammesse)
    scelta = parametri.group("gears")
    if not scelta:
        pass #todo specificare che deve scegliere
    elif "sn" in scelta:                                                                                #Sniper only
        GSRV.Gears = ""
    elif "aut" in scelta:                                                                               #Auto only
        pass
    elif "pis" in scelta:                                                                               #Pistols only
        pass
    elif "kn" in scelta:                                                                                #Knives only
        pass
    else:                                                                                               #Stringa armi
        pass

def info(richiedente, parametri):          #FUNZIONA
    """parametri vari server:IP admin, nextmap,ecc"""
    version = "^2I'm RedCap ^4%s " %versione
    server = " ^2on ^4%s:%s" %(M_CONF.Sck_ServerIP, M_CONF.Sck_ServerPort)
    autore = "^3 by bw|Lebbra!"
    tell(richiedente, version + server + autore)
    tell(richiedente, "^3ONLINE HELP and download at: ^6code.google.com/p/redcap/")
    tell(richiedente, "^2Players:^3U:%s ^1R:%s ^5B:%s ^2S:%s ^3Servermode:^5%s" %(str(GSRV.TeamMembers[0]), str(GSRV.TeamMembers[1]), str(GSRV.TeamMembers[2]), str(GSRV.TeamMembers[3]), str(GSRV.Server_mode)))

def kick(richiedente, parametri, reason = ""):  #FUNZIONA
    """Kikka un player dal server"""
    if richiedente == "Redcap":                                 #kick richiesto direttamente dal RedCap
        target = parametri
    else:
        target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():                                                   #se ho trovato lo slot
        if reason <> "":
            if not M_CONF.SV_silentmode:
                say(reason, 0)
                time.sleep(2)
        SCK.cmd("kick " + target)                                 #Invio al socket il comando kick

def level (richiedente, parametri):  #FUNZIONA
    """assegna il livello ad un player"""
    if not parametri.group("num"):
        tell(richiedente, Lang["wrongcmd"])
        return
    if int(parametri.group("num")) > GSRV.PT[richiedente].level:
        tell(richiedente, Lang["toohighlevel"]%str(GSRV.PT[richiedente].level))
        return
    target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():                                                   #se ho trovato lo slot
        GSRV.PT[target].level = int(parametri.group("num"))
        tell(richiedente, Lang["levassigned"]%(int(GSRV.PT[target].level), GSRV.PT[target].nick))
        tell(target, Lang["levassigned"]%(int(GSRV.PT[target].level), GSRV.PT[target].nick))

def map(richiedente, parametri):    #FUNZIONA
    """carica una mappa"""
    mapname = []
    reqmap = parametri.group("map")
    for mappa in GSRV.Q3ut4["map"]:
        if str.lower(str.strip(mappa)).find(str.lower(reqmap)) != -1:   #trovato un file corrispondente
            mapname.append(mappa)
    if len(mapname) == 1:
        SCK.cmd("map " + mapname[0])
    else:
        tell(richiedente, Lang["noclearmap"])

def maplist(richiedente, parametri):
    """lista le mappe del server"""
    frase = "^6Map list: "
    i = 0
    for mappa in GSRV.Q3ut4["map"]:
        i += 1
        frase += ("^" + str(i) + str(mappa) + " ")
        if i == 5:
            tell(richiedente, frase)
            frase = ""
            i = 0
    if i <> 0:
        tell(richiedente, frase)     

def mute(richiedente, parametri, reason = ""):
    """Muta/smuta un player"""
    if richiedente == "Redcap":                                 #mute richiesto direttamente dal RedCap
        target = parametri
    else:
        target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():                                                   #se ho trovato lo slot
        if reason <> "":
            if not M_CONF.SV_silentmode:
                say(reason, 0)
        if "muted" in GSRV.PT[target].varie:
            GSRV.PT[target].varie.remove("muted")           #tolgo la tag muted
        else:
            GSRV.PT[target].varie.append("muted")   #TODO togliere a fine mappa e verificare alla connessione
        SCK.cmd("mute " + target)                                 #Invio al socket il comando mute

def muteall(richiedente, parametri):
    """Muta/smuta tutti i players di livello inferiore al richiedente"""
    if GSRV.Server_mode == 0:                               #comando non disponibile in fase di avvio
        tell(richiedente, Lang["noavailcmd"])
        return
    for player in GSRV.PT:
        if GSRV.PT[player].level < GSRV.PT[richiedente].level:
            if "muted" in GSRV.PT[player].varie:
                GSRV.PT[player].varie.remove("muted")           #tolgo la tag muted
            else:
                GSRV.PT[player].varie.append("muted")
            SCK.cmd("mute " + player)
    say(Lang["muteall"], 2)
        
def nuke(richiedente, parametri):   #FUNZIONA
    """equivalente a "nuke" da console"""                   
    if richiedente == "Redcap":                                 #mute richiesto direttamente dal RedCap
        lanciatore = "RedCap"
        target = parametri
    else:
        target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():                                                   #se ho trovato lo slot
         SCK.cmd("nuke " + target)
         lanciatore = GSRV.PT[richiedente].nick
         say(Lang["nuked"]%(GSRV.PT[target].nick, lanciatore),0)

def notlev(richiedente, parametri):
    """cambia temporaneamente la notoriety necessaria per giocare sul server"""
    if parametri.group("num").isdigit():
        GSRV.MinNot_toplay = float(parametri.group("num"))
    else:
        GSRV.MinNot_toplay = M_CONF.Nt_MinNot_toplay
    say(Lang["not_changed"] %str(GSRV.MinNot_toplay), 2)

def nukeall():
    if GSRV.Nukemode:
        GSRV.Nukemode = False       #nukemode disattivato
        say("^7NUKEMODE ^2OFF", 2)
    else:
        GSRV.Nukemode = True        #nukemode disattivato
        say("^7NUKEMODE ^1ON", 2)

def ora (richiedente, parametri):   #FUNZIONA
    """dice l'ora"""
    tell(richiedente, Lang["ora"] %(time.strftime("%H.%M.%S", time.localtime())))

def password(richiedente, parametri):  #FUNZIONA
    """Setta una password"""
    SCK.cmd("g_password " + parametri.group("pwd"))
    tell(richiedente, Lang["pwdset"])

def radio(frase):                                                                                       #frase (0=id, 1=radio msg (x - y))
    if frase[0]not in GSRV.PT:                                                                          #potrebbero partire dei radio prima del ClientBegin, dando errore "KeyError: '0'
        return
    GSRV.PT[frase[0]].flood += 1                                                                        #Incremento il flood (#todo vedere se gestire i msg)

def rcrestart(richiedente, parametri =""):
    """restarta il RedCap"""
    say(Lang["restart"], 2)
    tmp = []
    for pl in GSRV.PT:
        tmp.append(GSRV.PT[pl].slot_id)
    for id in tmp:
        if not M_CONF.SV_silentmode:
            say(Lang["salvoplayer"]%GSRV.PT[id].nick, 1)
        clientdisconnect(id)        #chiamo la funzione come se il player si disconnettesse
    import sys
    if parametri <> "":
        scrivilog("RESTART RedCap: %s" %parametri, M_CONF.crashlog)
    else:
        scrivilog("RESTART RedCap", M_CONF.crashlog)
    sleep(1)
    sys.exit()

def recordreset(richiedente, parametri):
    """Azzera uno o tutti i record"""
    DB.connetti()
    if parametri.group("target") == "day":
        DB.esegui(DB.query["saverecords"], ("0.0", "0", " ", "Day"))
        GSRV.TopScores["Day"] = [0.0, 0, " "]
    elif parametri.group("target") == "week":
        DB.esegui(DB.query["saverecords"], ("0.0", "0", " ", "Week"))
        GSRV.TopScores["Week"] = [0.0, 0, " "]
    elif parametri.group("target") == "month":
        DB.esegui(DB.query["saverecords"], ("0.0", "0", " ", "Month"))
        GSRV.TopScores["Month"] = [0.0, 0, " "]
    elif parametri.group("target") == "alltime":
        DB.esegui(DB.query["saverecords"], ("0.0", "0", " ", "Alltime"))
        GSRV.TopScores["Alltime"] = [0.0, 0, " "]
    elif parametri.group("target") == "all":
                DB.esegui(DB.query["saverecords"], ("0", "0.0", " ", "Day",))
                GSRV.TopScores["Day"] = [0.0, 0, " "]
                DB.esegui(DB.query["saverecords"], ("0", "0.0", " ", "Week",))
                GSRV.TopScores["Week"] = [0.0, 0, " "]
                DB.esegui(DB.query["saverecords"], ("0", "0.0", " ", "Month",))
                GSRV.TopScores["Month"] = [0.0, 0, " "]
                DB.esegui(DB.query["saverecords"], ("0", "0.0", " ", "Alltime",))
                GSRV.TopScores["Alltime"] = [0.0, 0, " "]
    else:
        tell(richiedente, Lang["resetnotdone"] %"^4day ^6week ^7month ^5alltime ^2all")
        DB.disconnetti()
        return
    tell(richiedente, Lang["resetdone"] %parametri.group("target"))
    DB.salva()
    DB.disconnetti()

def shuffle(richiedente, parametri):
    """shuffla in base alla skill_var"""
    past = (time.time() - GSRV.LastShuffle)/60
    if GSRV.Server_mode < 3:
        pass                                                                                            #shuffle solo in modalita normale o silent.
    elif GSRV.tot_players(1) < 3:
        pass                                                                                            #non ha senso shufflare con due persone
    elif past < M_CONF.TimeBetweenShuffle:                                                              #controllo se e' passato tempo sufficiente
        pass
    else:
        red_list = []
        blue_list = []
        for PL in GSRV.PT:
            if GSRV.PT[PL].team == 1:                                                                   #red
                red_list.append([GSRV.PT["PL"].skill_var, PL])
            elif GSRV.PT[PL].team == 2:                                                                 #blue
                blue_list.append([GSRV.PT["PL"].skill_var, PL])
        lista.sort()                                                                                    #ottengo la lista e la ordino per skill var
        forceteam("Redcap", [lista.pop()[1]," red"])                                                    #sistemo i primi 3 a mano

def silent(richiedente, parametri):
    if not GSRV.Server_mode:
        tell(richiedente, Lang["noavailcmd"])
    elif M_CONF.SV_silentmode:
        M_CONF.SV_silentmode = False
        GSRV.Server_mode = 5
        say(Lang["silentmode"]%"OFF", 2)
    else:
        M_CONF.SV_silentmode = True
        GSRV.Server_mode = 3
        say(Lang["silentmode"]%"ON", 2)

def skill(richiedente, parametri):  #FUNZIONA
    """Comunica la skill del player"""
    if not parametri.group("target"):           #richiesta propria skill
        tell(richiedente, Lang["skill"]%(round(GSRV.PT[richiedente].skill, 1), round(GSRV.PT[richiedente].skill_var, 2), GSRV.PT[richiedente].ksmax))
        return
    target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():                                                   #se ho trovato lo slot
        tell(richiedente, Lang["skill"]%(round(GSRV.PT[target].skill,1), round(GSRV.PT[target].skill_var,1), GSRV.PT[target].ksmax))                    

def slap(richiedente, parametri, reason=""): #FUNZIONA
    """equivalente a "slap" da console, ma puo' essere chiamato piu' volte di fila"""
    if richiedente == "Redcap":                                 #force richiesto direttamente dal RedCap
        target = parametri[1]
        volte = parametri[0]
    else:
        target = trovaslotdastringa(richiedente, parametri.group("target"))
        if parametri.group("num").isdigit():
            volte = int(parametri.group("num"))
            if volte > M_CONF.maxSlap:
                volte = M_CONF.maxSlap
        else:
            volte = 1
    if target.isdigit():                                                                                #se ho trovato lo slot
        if reason <> "":
            tell(target, reason)
        for i in range(int(volte)):                                                                     #Invio al buffer il comando un numero "param[1]" di volte
            SCK.cmd("slap " + target)

def smite(richiedente, parametri, reason = ""):                                                         #FUNZIONA
    """Killa un player sul server (solo 4.2)"""
    if richiedente == "Redcap":                                                                         #smite richiesto direttamente dal RedCap
        target = parametri
    else:
        target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():                                                                                #se ho trovato lo slot
        if reason <> "":
            if not M_CONF.SV_silentmode:
                say(reason, 0)
                time.sleep(2)
        SCK.cmd("smite " + target)                                                                      #Invio al socket il comando smite
        if not richiedente == "Redcap":
            say(Lang["smited"]%GSRV.PT[target].nick,0)

def spam(richiedente, parametri):       
    """inserisce/disinserisce frasi di spam)"""
    if parametri.group("un").lower() == "un":                                                           #sto cancellando
        if parametri.group("frase").isdigit():
            if GSRV.SpamList[int(parametri.group("frase"))].endswith("#"):                              #non posso cancellare un record
                tell(richiedente, Lang["norecorderase"])
                return
            del(GSRV.SpamList[int(parametri.group("frase"))])
            GSRV.SpamlistIndex -= 1 #per ovviare che se stava leggendo l'ultimo spam vada fuori lista
            spam = open("spam.txt", "w")
            for frase in GSRV.SpamList:
                if frase.endswith("#"):     #evito di scrivere i record che sono marcati da # e devono stare in DB, non in spam.txt
                    pass
                else:
                    spam.write(frase + "\n")
            spam.seek(-1, 2)
            spam.truncate() #tolgo l'ultimo a capo
            spam.close()
            tell(richiedente, Lang["spamerased"])
        else:
            tell(richiedente, Lang["spamnotfound"])
    else:                                               #sto aggiungendo
        GSRV.SpamList.append(parametri.group("frase"))
        spam = open("spam.txt", "a")
        spam.write("\n" + parametri.group("frase"))
        spam.close()
        tell(richiedente, Lang["spamadded"])

def spamlist(richiedente, parametri):
    """lista tutti gli spam"""
    for frase in GSRV.SpamList:
        tell(richiedente, "^4" + str(GSRV.SpamList.index(frase)) + ": ^2" + str(frase))

def status(richiedente, parametri, modo = M_CONF.status):       #FUNZIONA
    """fornisce informazioni sui giocatori o saluta"""
    if not parametri.group("target"):                     #comando status senza target: do nick e slot di tutti
        for player in GSRV.PT:
            if GSRV.PT[richiedente].level >= M_CONF.lev_admin:
                tell(richiedente, "^6%s ^%s%s  ^3DB.^5%s ^3Aff.^7%s ^3Lev.^7%s " %(GSRV.PT[player].slot_id, str(GSRV.PT[player].team), GSRV.PT[player].nick, str(GSRV.PT[player].DBnick), str(round(GSRV.PT[player].notoriety, 1)), str(GSRV.PT[player].level)))
            else:
                tell(richiedente, "^6%s ^%s%s ^3Aff.^7%s" %(GSRV.PT[player].slot_id, str(GSRV.PT[player].team), GSRV.PT[player].nick, str(round(GSRV.PT[player].notoriety, 1))))
        return
    elif GSRV.PT[richiedente].level >= M_CONF.lev_admin:
        modo = M_CONF.status_adm
    target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():                                                    #se ho trovato lo slot
        stat = GSRV.PT[target].stats()
        if 2 in stat:
            stat[2] = round(stat[2], 1)
        if 4 in stat:
            stat[4] = round(stat[4], 1)
        if 2048 in stat:
            stat[2048] = time.strftime("%d.%b.%Y %H.%M", time.localtime(stat[2048]))        #trasformo il tempo universale in leggibile
        opzioni = option_checker(modo)
        frase = ""
        i = 0
        while opzioni:
            opz = opzioni.pop()
            frase += Status[opz]%str(stat[opz])
            i += 1
            if i == 3:
                tell(richiedente, frase)
                frase = ""
                i = 0
        if i <> 0:
            tell(richiedente, frase)           

def tempban(richiedente, parametri):    #FUNZIONA
    """ban temporaneo"""
    target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():                                                    #se ho trovato lo slot
        if parametri.group("num").isdigit():                                #ho specificato la durata
            ore = float(parametri.group("num"))
            if ore > M_CONF.Ttempban:
                ore = float(M_CONF.Ttempban)
                tell(richiedente, Lang["tempbanmax"]%str(M_CONF.Ttempban))
        else:
            ore = 1.0         #se non specificato banno 1h
        say(Lang["tempban"] %(GSRV.PT[target].nick, ore), 2)
        time.sleep(1)
        GSRV.PT[target].tempban = time.time() + ore*3600 #data scadenza ban
        SCK.cmd("kick " + target)   #lo kikko (al clientdisconnect si aggiorna il tempban)

def top(richiedente, parametri):    #FUNZIONA
    """dice i record"""
    tell(richiedente, Lang["top"]%("Alltime", str(GSRV.TopScores["Alltime"][1]), str(GSRV.TopScores["Alltime"][2]), time.strftime("%d.%b %H.%M.%S", time.localtime(GSRV.TopScores["Alltime"][0]))))
    tell(richiedente, Lang["top"]%("Month", str(GSRV.TopScores["Month"][1]), str(GSRV.TopScores["Month"][2]), time.strftime("%d.%b %H.%M.%S", time.localtime(GSRV.TopScores["Month"][0]))))
    tell(richiedente, Lang["top"]%("Week", str(GSRV.TopScores["Week"][1]), str(GSRV.TopScores["Week"][2]), time.strftime("%d.%b %H.%M.%S", time.localtime(GSRV.TopScores["Week"][0]))))
    tell(richiedente, Lang["top"]%("Day", str(GSRV.TopScores["Day"][1]), str(GSRV.TopScores["Day"][2]), time.strftime("%d.%b %H.%M.%S", time.localtime(GSRV.TopScores["Day"][0]))))
    #TODO tell(richiedente, Lang["top"]%("HSkill", str(GSRV.TopScores["HSkill"][1]), str(GSRV.TopScores["HSkill"][2]), time.strftime("%d.%b %H.%M.%S", time.localtime(GSRV.TopScores["HSkill"][0])))) #TODO HI e LO skill (da fare)
    #tell(richiedente, Lang["top"]%("LSkill", str(GSRV.TopScores["LSkill"][1]), str(GSRV.TopScores["LSkill"][2]), time.strftime("%d.%b %H.%M.%S", time.localtime(GSRV.TopScores["LSkill"][0]))))

def trust(richiedente, parametri):
    """aumenta o diminuisce la reputation"""
    target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():
        repu_var = 1.0
        if parametri.group("num").isdigit():
            repu_var = repu_var * int(parametri.group("num"))
        if parametri.group("un") == "un":                                                               #diminuisco l'affidabilita
            GSRV.PT[target].reputation -= repu_var                                                      #vario la reputation (va in DB)
        else:
            GSRV.PT[target].reputation += repu_var
            GSRV.PT[target].tobekicked = 0                                                              #se c era un tobekicked lo sospendo
        GSRV.PT[target].notoriety = GSRV.PT[target].notoriety_upd(M_CONF.Nt_roundXpoint, M_CONF.Nt_dayXpoint)   #aggiorno la notoriety
        tell(richiedente, Lang["not_update"] %(str(GSRV.PT[target].nick), str(GSRV.PT[target].notoriety)))
        tell(target, Lang["not_update"] %(str(GSRV.PT[target].nick), str(GSRV.PT[target].notoriety)))

def unwar(richiedente, parametri):                                                                      #FUNZIONA
    """resetta il server in modalita' normale"""
    SCK.cmd("g_matchmode 0")                                                                            #giusto per sicurezza nel caso non sia specificato nel server.cfg
    say(Lang["warunloaded"]%GSRV.Baseconf, 2)
    SCK.cmd("exec %s" %GSRV.Baseconf)                                                                   #eseguo la config di base
    if M_CONF.SV_silentmode:
        GSRV.Server_mode = 3                                                                            #Silentmode
    else:
        GSRV.Server_mode = 5                                                                            #Normale. Passo in modalita normale
    SCK.cmd("reload")                                                                                   #avvio la cfg

def war(richiedente, parametri):                                                                        #FUNZIONA
    """setta il server in modalita' war"""
    tmp = []
    if parametri.group('cfg'):                                                                          #e' stata indicata una configurazione
        for cfg in GSRV.Q3ut4["cfg"]:
            if str.lower(cfg).find(str.lower(str.strip(parametri.group('cfg')))) != -1:                 #porto tutto in minuscole e confronto
                tmp.append(cfg)
        if len(tmp) == 1:
            say(Lang["warloaded"] %tmp[0], 2)
            SCK.cmd("exec %s" %tmp[0])                                                                  #eseguo la config richiesta
        else:
            tell(richiedente, Lang["noclearcfg"])
            return
    else:                                                                                               #Eseguo la config di base
        say(Lang["warbaseloaded"] , 2)
        SCK.cmd("exec RedCapWar.cfg")                                                                   #eseguo la config di base
    SCK.cmd("reload")                                                                                   #avvio la cfg
    GSRV.Server_mode = 2                                                                                #passo in modalita war