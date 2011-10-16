#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import re
import C_DB         #Classe che rappresenta il DB
import C_GSRV       #Classe che rappresenta il gameserver
import C_PLAYER     #Classe per creare players
import C_SOCKET     #Classe socket per comunicazione con UrT
import M_CMD        #Lista comandi
import M_CONF       #Carico le configurazioni programma
import M_SAYS       #dati ausiliari per gestire i say ed i comandi
exec("import M_%s" %M_CONF.RC_lang)            #importo modulo localizzazione linguaggio

#Carico i moduli di lingua
Lang = eval( "M_%s.RC_outputs" %M_CONF.RC_lang)
Status = eval( "M_%s.RC_status" %M_CONF.RC_lang)
Logs = eval("M_%s.RC_logoutputs" %M_CONF.RC_lang)
Killz = eval("M_%s.RC_kills" %M_CONF.RC_lang)

SCK = C_SOCKET.Sock(M_CONF.SocketPars)                                              #Istanzio il socket
GSRV = C_GSRV.Server(M_CONF.ServerPars, M_CONF.sv_SkillPars, M_CONF.sv_WarnPars)    #Istanzio il gameserver
DB = C_DB.Database(M_CONF.NomeDB)                                                   #Istanzio il DB

#DB.connetti()
#GSRV.Banlist= (DB.esegui("""SELECT * FROM BAN""")).fetchall()   #carico la banlist #TODO da scaricare periodicamente (spostare in modulo apposito?)
#DB.disconnetti()

##Parametri per le kill
normalKills = ['12', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '28', '30', '35', '38', '40']
accident = ['6', '9', '31']
suicide = '7'
nuked = '34'

##FUNZIONI INTERNE DEL REDCAP##

def censura(frase):
    """controlla se nella frase ci sono parole non ammesse"""
    testo=frase.replace(".","") #tolgo i punti dei furbetti.
    testo=frase.replace("_","") 
    for insulto in M_SAYS.censura:
        if re.search(insulto,testo,re.I):                       #ho trovato un insulto
            return True

def clientconnect(id):      #TODO non serve se c'è lo stesso in clientuserinfo
    """Gestisce un nuovo client"""
    if id not in GSRV.PT:                           #Se e un nuovo player (nel senso di appena entrato in game)
        newplayer = C_PLAYER.Player()               #lo creo
        GSRV.player_NEW(newplayer, id, time.time()) #lo aggiungo alla PlayerTable ed ai TeamMember
    else:
        pass        #il player gia' esiste ed e' semplicemente un initgame #TODO vedere se serve

def clientdisconnect(id):
    """Operazioni da fare alla disconnessione"""
    if id not in GSRV.PT:
        return                              #nel log raramente capitano anche 2 clientdisconnect dello stesso player di seguito
    if GSRV.PT[id].justconnected:
        GSRV.player_DEL(id)                 #se e' un justconnected non accettato per badnick o badguid non salvo nulla in db #TODO salvare IP per eventuale ban?
        return
    alias = GSRV.PT[id].alias_to_DB()
    varie = GSRV.PT[id].varie_to_DB()
    DB.connetti()
    DB.esegui(DB.query["salvadati"], (GSRV.PT[id].DBnick, GSRV.PT[id].skill, GSRV.PT[id].rounds, GSRV.PT[id].lastconnect, GSRV.PT[id].level, GSRV.PT[id].tempban, GSRV.PT[id].reputation, GSRV.PT[id].ksmax,\
    alias, varie, GSRV.PT[id].guid )) #salvo in tabella DATI
    DB.esegui(DB.query["salvakills"], (GSRV.PT[id].kills['12'], GSRV.PT[id].kills['14'], GSRV.PT[id].kills['15'], GSRV.PT[id].kills['16'], GSRV.PT[id].kills['17'], GSRV.PT[id].kills['18'], GSRV.PT[id].kills['19'],\
    GSRV.PT[id].kills['20'], GSRV.PT[id].kills['21'], GSRV.PT[id].kills['22'], GSRV.PT[id].kills['23'], GSRV.PT[id].kills['24'], GSRV.PT[id].kills['25'], GSRV.PT[id].kills['28'], GSRV.PT[id].kills['30'],\
    GSRV.PT[id].kills['35'], GSRV.PT[id].kills['38'], GSRV.PT[id].kills['40'], GSRV.PT[id].deaths, GSRV.PT[id].guid))   #salvo in tabella KILL
    DB.esegui(DB.query["salvahit"], (GSRV.PT[id].hits['0'] + GSRV.PT[id].hits['1'], GSRV.PT[id].hits['2'] + GSRV.PT[id].hits['3'], GSRV.PT[id].hits['4'], GSRV.PT[id].hits['5'], GSRV.PT[id].hits['6'], GSRV.PT[id].guid)) #salvo in tabella HIT
    #TODO salvare altre tabelle?
    DB.salva()
    DB.disconnetti()
    GSRV.player_DEL(id)

def clientuserinfo(info):                       #info (0=slot_id, 1=ip, 2=guid)
    if info[0] not in GSRV.PT:                           #Se e un nuovo player (nel senso di appena entrato in game)
        newplayer = C_PLAYER.Player()               #lo creo
        GSRV.player_NEW(newplayer, info[0], time.time()) #lo aggiungo alla PlayerTable ed ai TeamMember
    if GSRV.PT[info[0]].justconnected:              #Se e un nuovo player
        GSRV.player_ADDINFO(info)                   #gli aggiungo GUID e IP
    elif info[2] <> GSRV.PT[info[0]].guid:          #cambio guid durante il gioco
        if GSRV.Server_mode <> 2:                   #non attivo in warmode
            GSRV.PT[info[0]].notoriety += M_CONF.Notoriety["guidchange"]            #gli abbasso la notoriety in proporzione
            kick("Redcap", info[0], Lang["guidchange"]%info[1])

def clientuserinfochanged(info):                #info (0=id, 1=nick, 2=team)
    res = GSRV.player_USERINFOCHANGED(info)                                     #Aggiorno NICK e TEAM (se res True, il player ha cambiato nick (o e' nuovo)
    if GSRV.Server_mode == 0:
        if GSRV.TeamMembers[0] == 0:
            GSRV.Server_mode = 1
            say(Lang["startupend"], 1)
    if GSRV.Server_mode <> 2:                               #non attivo in warmode
        if GSRV.PT[info[0]].invalid_guid():                                                             #CONTROLLO VALIDITA GUID (adesso che ho pure il nick!)
            GSRV.PT[info[0]].notoriety += M_CONF.Notoriety["badguid"]               #abbasso la notoriety
            kick("Redcap", info[0], Lang["invalidguid"]%info[1])                    #e lo kikko         #TODO  registrare nick e ip in DB o in log
            return  #inutile andare avanti
        if GSRV.PT[info[0]].invalid_nick(GSRV.Nick_is_length, GSRV.Nick_is_good, info[1]):              #CONTROLLO VALIDITA NICK (non ancora assegnato al player!)
            kick("Redcap", info[0], Lang["invalidnick"]%info[1])
            return   #inutile andare avanti
    if GSRV.PT[info[0]].justconnected:                                                                  #PLAYER APPENA CONNESSO
        res = False                                         #non ha cambiato nick, inutile controllare gli alias. #TODO da togliere se justconnect sparisce alla disconnessione
        db_datacontrol(GSRV.PT[info[0]].guid, info[0])      #controllo se il player esiste nel DB e ne recupero i dati (tb DATA) se no lo registro
        if GSRV.Server_mode <> 2:                           #non attivo in warmode
            if GSRV.PT[info[0]].tempban > time.time():                                                  #CONTROLLO BAN
                ban = time.strftime("%d.%b.%Y %H.%M", time.localtime(GSRV.PT[info[0]].tempban))
                kick("Redcap", info[0], Lang["stillban"]%(GSRV.PT[info[0]].nick, ban))
                return
            if GSRV.PT[info[0]].notoriety < GSRV.MinNotoriety:                                          #CONTROLLO NOTORIETY
                kick("Redcap", info[0], Lang["lownotoriety"]%(info[1],GSRV.PT[info[0]].notoriety,GSRV.MinNotoriety))
                return
            if (time.time() -  GSRV.PT[info[0]].lastconnect) < GSRV.AntiReconInterval:                  #CONTROLLO RECONNECT
                kick("Redcap", info[0], Lang["antirecon"]%(GSRV.PT[info[0]].nick, str( GSRV.AntiReconInterval)))
                return
            if "muted" in GSRV.PT[info[0]].varie:           #lo muto in quanto si e' disconnesso da muto.
                mute("Redcap",info[0])
                say(Lang["muted"]%GSRV.PT[info[0]].nick, 0)
        GSRV.PT[info[0]].skill_coeff_update()               #aggiorno il coefficiente skill
        GSRV.PT[info[0]].justconnected = False              #non e piu nuovo
        if GSRV.Server_mode <> 2:                           #non attivo in warmode
            saluta(M_CONF.saluti, info[0])                  #chiamo la funzione che si occupa eventualmente di salutare il player
        GSRV.PT[info[0]].lastconnect = time.time()          #aggiorno il lastconnect
    if res:                                                 #CONTROLLO ALIAS (solo per player NON nuovi)
        esiste = False
        for alias in GSRV.PT[info[0]].alias:
            if info[1] in alias:
                esiste = True
                alias[0] = str(time.time())                                     #se esiste aggiorno la data di ultimo utilizzo
        if not esiste:
            GSRV.PT[info[0]].alias.append([str(time.time()), info[1]])          #se non esiste lo aggiungo

       # db_loccontrol(GSRV.PT[info[0]].guid)        #controllo il player nel DB (tb LOC)

def comandi (frase):                            #frase [id, testo] (es: "2:31 say: 3 Nero: !slap Cobr4" diventa: ["3", "!slap Cobr4"]
    """processo il comando prima di inviarlo alla finzione specializzata"""
    if frase[0]not in GSRV.PT:                  #potrebbero partire dei say prima del ClientBegin, dando errore "KeyError: '0'
        return
    for comando in M_CMD.comandi:               #comando ["nomecomando","regex", livello]
        res = re.search(comando[1], frase[1], re.I)     #Individuo il tipo di comando
        if res:                                         #Ho trovato un comando
            if comando[2] >= M_CONF.commandlogMinLevel: #se e' un comando importante lo registro nel commandlog
                scrivilog(Logs["command"] %(GSRV.PT[frase[0]].nick,  GSRV.PT[frase[0]].DBnick, GSRV.PT[frase[0]].level,  frase[1], comando[2]) , M_CONF.commandlog)
            if GSRV.PT[frase[0]].level < comando[2]:
                tell(frase[0], Lang["nolevel"] %(str(comando[2]), GSRV.PT[frase[0]].level))        #player non autorizzato
            else:
                eval("%s(frase[0],res)" %comando[0])    #eseguo il comando e gli passo richiedente e parametri
            break
    if not res:
        tell(frase[0], Lang["wrongcmd"] )          #comando non riconosciuto

def cr_floodcontrol():
    """verifica (periodica) che nessun player abbia fatto flood"""
    for PL in GSRV.PT:
        if GSRV.PT[PL].flood >= GSRV.MaxFlood:
            #TODO gli abbasso la notoriety
            kick("Redcap", GSRV.PT[PL].slot_id, Lang["flood"]%GSRV.PT[PL].nick)
        else:
            GSRV.PT[PL].flood = 0        #Se non e kikkato lo rimetto a zero

def cr_full():
    """verifica se il server e' pieno o vuoto"""
    if GSRV.Server_mode <> 0:
        clients = (GSRV.TeamMembers[0] + GSRV.TeamMembers[1] + GSRV.TeamMembers[2] + GSRV.TeamMembers[3])
        if clients == GSRV.MaxClients:              # faccio operazioni da server pieno
            GSRV.Full = 2                           
            if M_CONF.KickForSpace and GSRV.Server_mode <> 2:
                for PL in GSRV.PT:
                    if GSRV.PT[PL].team == 3:
                        kick("Redcap", GSRV.PT[PL].slot_id, Lang["space"]%GSRV.PT[PL].nick)
        elif clients == 0:                          # faccio operazioni da server vuoto
            GSRV.Full = 0
            if GSRV.Server_mode > 1:                #tolgo la configurazione war
                SCK.cmd("g_password ''")            #tolgo la password
                SCK.cmd("exec " + GSRV.Baseconf)    #carico la config di base
                GSRV.Server_mode = 1
        else:
            GSRV.Full = 1

def cr_nickrotation():
    """verifica (periodica) che nessun player abbia fatto nickrotation"""
    for PL in GSRV.PT:
        if GSRV.PT[PL].nickchanges > GSRV.MaxNickChanges:
            #TODO gli abbasso la notoriety?
            kick("Redcap", GSRV.PT[PL].slot_id, Lang["nickchanges"]%(GSRV.PT[PL].nick, GSRV.PT[PL].nickchanges))
        else:
            GSRV.PT[PL].nickchanges = 0        #Se non e' kikkato lo rimetto a zero

def cr_spam():
    """spam periodici"""
    if len(GSRV.SpamList) == 0:
        return                                          #spamlist vuota
    else:
        say(GSRV.SpamList[GSRV.SpamlistIndex], 0)       #spammo
    if GSRV.SpamlistIndex == len(GSRV.SpamList) - 1:    #Aumento l'index
        GSRV.SpamlistIndex = 0
    else:
        GSRV.SpamlistIndex += 1

def cr_unvote():
    """verifica (periodica) che il voto non sia rimasto attivo dopo il comando !v"""
    if GSRV.VoteMode and ((time.time() - GSRV.LastVote) > M_CONF.voteTime):
        GSRV.VoteMode = False

def cr_warning():
    """verifica se qualche player ha troppi warning"""
    for PL in GSRV.PT:
        if GSRV.PT[PL].warning >= GSRV.WarnMax:
            #TODO gli abbasso la notoriety?
            kick("Redcap", GSRV.PT[PL].slot_id, Lang["warning"]%GSRV.PT[PL].nick)

def db_datacontrol(guid,id):
    """Applicato ai player appena connessi: recupera i valori della tabella DATA, o se il player non e' registrato lo registra"""
    DB.connetti()
    dati = DB.esegui(DB.query["cercadati"], (guid,)).fetchone()    # PROVO A CARICARE da TABELLA DATI
    if dati:                                                                    #se ESISTE IN DB recupero i dati (guid, DBnick, skill, rounds, lastconn, level, tempban, notoriety, firstconn, streak, alias, varie)
        GSRV.PT[id].isinDB = True                                               #esiste gia nel DB
        GSRV.PT[id].dati_load(dati, M_CONF.Notoriety["roundXpoint"], M_CONF.Notoriety["dayXpoint"], time.time())
        #TODO caricare i dati anche dalle altre tables?
    else:                                                               #se NON ESISTE IN DB: gli assegno i valori non ancora assegnati e lo registro inserendo guid e nick
        GSRV.PT[id].DBnick = GSRV.PT[id].nick                           #gli assegno il DBnick (potra' essere cambiato in seguito con il comando !nick)
        GSRV.PT[id].alias = [[str(time.time()), GSRV.PT[id].nick]]      #gli assegno il suo primo alias
        alias = str(time.time()) + " " + GSRV.PT[id].nick               #alias scritto nella forma per database
        DB.esegui(DB.query["newdati"], (GSRV.PT[id].guid, GSRV.PT[id].nick, 0, 0, GSRV.PT[id].lastconnect, 0, 0.0, 0, time.time(), 0, alias, ""))
        DB.esegui(DB.query["newdeath"], (GSRV.PT[id].guid,))
        DB.esegui(DB.query["newhit"], (GSRV.PT[id].guid,))
        DB.esegui(DB.query["newkill"], (GSRV.PT[id].guid,))
        DB.esegui(DB.query["newloc"], (GSRV.PT[id].guid, GSRV.PT[id].ip))    #gli salvo il suo primo IP
        DB.salva()
    DB.disconnetti()
    if guid in M_CONF.AdminGuids:       #se e' admin gli do il massimo livello
         GSRV.PT[id].level = 100
         tell(GSRV.PT[id].slot_id, Lang["adminrights"]%GSRV.PT[id].nick)

def db_loccontrol(guid):    #TODO unused
    DB.connetti()
    res = DB.esegui(DB.query["cercaloc"], (guid,)).fetchone()
    if res:                                                             # esiste in db (guid, IP, provider, location, old_guids)
        pass #TODO recuperare IP ,provider location, old_guids

def endMap(frase):
    """operazioni da fare a fine mappa"""
    rank=[]                                             # CREAZIONE SKILL LIST
    for pl in GSRV.PT:
        if "muted" in GSRV.PT[pl].varie:
            GSRV.PT[pl].varie.remove("muted")           #tolgo la tag muted
        rank.append((GSRV.PT[pl].skill_var, GSRV.PT[pl].nick))
        GSRV.PT[pl].skill_var = 0                       #azzero la skill_var
    if GSRV.Server_mode <> 2:                               #non attivo in warmode
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
        DB.disconnetti
    endRound(frase)                                     #richiamo anche le solite operazioni da endround

def endRound(frase):
    pass        #TODO

def hits(frase):                                                #del tipo ['1', '0', '3', '5'] Vittima, Killer, Zona, Arma (per il momento arma non e' utilizzato)
    if frase[0] not in GSRV.PT:                         #in rari casi il player puo' essere hittato dopo clientdisconnect
        return
    if GSRV.is_thit(frase[1], frase[0]):               #controllo che non faccia THIT
        tell(GSRV.PT[frase[1]].slot_id, Lang["thit"] %str(GSRV.PT[frase[1]].warning))  #TEAMHIT
        return
    else:                                                           #hit normale
        GSRV.PT[frase[1]].hits[frase[2]] += 1       #aggiungo una hit
        GSRV.PT[frase[1]].hits['total'] += 1        #aggiungo una hit al totale
        if GSRV.ShowHeadshots and int(frase[2]) < 2:      #se e' un headshot e lo devo spammare
            hs = GSRV.PT[frase[1]].hits['0'] + GSRV.PT[frase[1]].hits['1']
            perc = hs*100/GSRV.PT[frase[1]].hits['total']
            say(Lang["headshot"]%(GSRV.PT[frase[1]].nick, str(hs), str(perc)), 1)

def ini_clientlist():
    """all avvio trova i client gia collegati"""
    Res = SCK.cmd("clientlist")
    if Res[1]:
        list = Res[0].split("\n")   #List = GUID, SLOT, NICK
        if len(list) > 2:
            del(list[0])                        #pulisco la risposta
            list.reverse()
            del(list[0])
            for pl in list:                     #aggiungo i nuovi players
                dati = pl.split()
                newplayer = C_PLAYER.Player()   #lo creo
                GSRV.player_NEW(newplayer,dati[1], time.time())     #lo aggiungo alla PlayerTable ed ai TeamMember
                GSRV.PT[dati[1]].guid = dati[0]
                GSRV.PT[dati[1]].nick = dati[2]
                db_datacontrol(dati[0], dati[1])                    #carico i dati se esistono
                say(Lang["caricoplayer"]%str(GSRV.PT[dati[1]].nick), 1)
                GSRV.PT[dati[1]].skill_coeff_update()               #aggiorno il coefficiente skill
                GSRV.PT[dati[1]].justconnected = False             #non e piu nuovo
                GSRV.PT[dati[1]].lastconnect = time.time()          #aggiorno il lastconnect

def ini_recordlist():
    """recupera i record dal db"""
    DB.connetti()
    dati = DB.esegui(DB.query["getrecords"]).fetchall()
    DB.disconnetti()
    for element in dati:
        GSRV.TopScores[element[0]][0] = element[2]   #time
        GSRV.TopScores[element[0]][1] = element[1]   #val
        GSRV.TopScores[element[0]][2] = element[3]   #owner

def ini_spamlist():
    """carica la lista spam"""
    if M_CONF.CustomSpam:
        buf = open(M_CONF.SpamFile, "r")
        spam = buf.read().split("\n")
        buf.close()
        GSRV.SpamList = spam
    if M_CONF.RecordSpam:
        GSRV.SpamList.append(Lang["top"]%("Alltime", str(GSRV.TopScores["Alltime"][1]), str(GSRV.TopScores["Alltime"][2]), time.strftime("%d.%b %H.%M.%S", time.localtime(GSRV.TopScores["Alltime"][0]))))
        GSRV.SpamList.append(Lang["top"]%("Month", str(GSRV.TopScores["Month"][1]), str(GSRV.TopScores["Month"][2]), time.strftime("%d.%b %H.%M.%S", time.localtime(GSRV.TopScores["Month"][0]))))
        GSRV.SpamList.append(Lang["top"]%("Week", str(GSRV.TopScores["Week"][1]), str(GSRV.TopScores["Week"][2]), time.strftime("%d.%b %H.%M.%S", time.localtime(GSRV.TopScores["Week"][0]))))
        GSRV.SpamList.append(Lang["top"]%("Day", str(GSRV.TopScores["Day"][1]), str(GSRV.TopScores["Day"][2]), time.strftime("%d.%b %H.%M.%S", time.localtime(GSRV.TopScores["Day"][0]))))

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
    if GSRV.Server_mode == 1:                                       #solo in modalita normale. No war e no startup
        GSRV.teamskill_eval()                                       #aggiorno le teamskill e il coefficiente di sbilanciamento skill
        GSRV.players_alive()                                        #setto i player non spect a vivo, gli aggiungo un round e updato il coeff skill.
        if GSRV.BalanceMode == 2 or GSRV.BalanceRequired:           #eseguo bilanciamento automatico o su richiesta
            if abs(GSRV.TeamMembers[1] - GSRV.TeamMembers[2]) > 1:  #verifico se gli sbilanciamenti richiedono balance
                moving = GSRV.team_balance()
                SCK.cmd("forceteam " + moving)
                GSRV.BalanceRequired = False
                say(Lang["balancexecuted"], 0)
            else:
                say(str(GSRV.TeamMembers[0]) + "^1" + str(GSRV.TeamMembers[1])  + "^5" + str(GSRV.TeamMembers[2])  + "^2" + str(GSRV.TeamMembers[3]), 1)
        if (GSRV.MapName + "\n") in GSRV.Q3ut4["mapcycle"]:         #verifico qual'e la prossima mappa
            indice_nextmap = GSRV.Q3ut4["mapcycle"].index(GSRV.MapName+ "\n") +1
            if indice_nextmap == len(GSRV.Q3ut4["mapcycle"]):
                indice_nextmap = 0
            nextmap = GSRV.Q3ut4["mapcycle"][indice_nextmap]         #TODO verificare che funzioni
            say(Lang["nextmap"]%nextmap, 1)
    elif GSRV.Server_mode == 0:
        say(Lang["startup"], 1)


def kills(frase):                                       #frase del tipo ['0', '1', '16'] (K,V,M)
    if frase[1] not in GSRV.PT:                         #in rari casi il player puo' essere hittato dopo clientdisconnect
        return
    GSRV.PT[frase[1]].vivo = 2                          #in ogni caso setto la vittima a "morto"
    if frase[2] == '10':                                #CHANGETEAM  #TODO gestire il changeteam  se necessario
        return
    if frase[2] in normalKills :                                                            #KILL DA ARMA
        GSRV.PT[frase[0]].deaths += 1                        #aumento di 1 le deaths alla vittima
        if GSRV.is_tkill(frase[0], frase[1]):
            tell(GSRV.PT[frase[0]].slot_id, Lang["tkill"] %str(GSRV.PT[frase[0]].warning))  #TEAMKILL
            return
        GSRV.skill_variation(frase[0],frase[1])         #funzione che calcola ed assegna la variazione skill ai due players
        res0 = GSRV.is_kstreak(frase[0],frase[1], time.time())       #calcolo variazioni kstreak (eventuale spam)
        res = option_checker(res0)                      #Separo le opzioni di ritorno
        kz = GSRV.PT[frase[0]].ks                       #n. della frase di kstreak da spammare
        if kz > len(Killz)-1:
            kz = len(Killz)-1                           
        if 1 in res:                                    #spammo ks in bigtext
            say(Killz[kz]%GSRV.PT[frase[0]].nick, 2)
        elif 2 in res:                                  #spammo ks in console
            say(Killz[kz]%GSRV.PT[frase[0]].nick, 0)
        if 4 in res:                                    
            say(Lang["record_personal"]%(GSRV.PT[frase[0]].nick, str(GSRV.PT[frase[0]].ks)), 0)  #spammo personal record in console
        if 8 in res:
            say(Lang["record_alltime"]%(GSRV.PT[frase[0]].nick, str(GSRV.PT[frase[0]].ks)), 2)   #spammo alltime record
        elif 16 in res:
            say(Lang["record_monthly"]%(GSRV.PT[frase[0]].nick, str(GSRV.PT[frase[0]].ks)), 2)   #spammo monthly record
        elif 32 in res:
            say(Lang["record_weekly"]%(GSRV.PT[frase[0]].nick, str(GSRV.PT[frase[0]].ks)), 2)    #spammo weekly record
        elif 64 in res:
            say(Lang["record_daily"]%(GSRV.PT[frase[0]].nick, str(GSRV.PT[frase[0]].ks)), 2)     #spammo daily record
        elif 512 in res:
            say(Lang["record_no_not"]%GSRV.PT[frase[0]].nick, 0)     #notoriety bassa
        elif 1024 in res:
            say(Lang["record_no_ppl"]%(M_CONF.MinPlayers, GSRV.PT[frase[0]].nick), 0)     #poca gente
        if 128 in res:
            say(Killz[0]%(GSRV.PT[frase[0]].nick, GSRV.PT[frase[1]].nick), 2)               #spammo stop ks in bigtext
        elif 256 in res:
            say(Killz[0]%(GSRV.PT[frase[0]].nick, GSRV.PT[frase[1]].nick), 0)               #spammo stop ks in console
        GSRV.PT[frase[0]].kills[frase[2]] += 1          #aggiungo la kill alle statistiche
    elif frase[2] in accident :                                                             #INCIDENTE
        GSRV.PT[frase[1]].deaths += 1                        #aumento di 1 le deaths alla vittima
        say(Lang["accident"]%GSRV.PT[frase[1]].nick, 0)
    elif frase[2] == suicide:                                                               #SUICIDIO
        GSRV.PT[frase[1]].deaths += 1                        #aumento di 1 le deaths alla vittima
        GSRV.PT[frase[1]].skill -= 2 * GSRV.PT[frase[1]].skill_coeff * GSRV.Sk_penalty / GSRV.Sk_Kpp     #penalizzo la skill
        tell(frase[1], Lang["suicide"]%str(round(2 * GSRV.Sk_penalty / GSRV.Sk_Kpp, 2)))
    elif frase[2] == nuked:                                                                 #NUKED
        pass                                            #TODO vedere se si vuole contare

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

def recordErase(tipo):
    """cancella il o i record specificati"""
    GSRV.TopScores[tipo] = [0.0, 0, " "]
    
def saluta(modo, id):
    """si occupa di salutare il player al suo ingresso in game"""
    if GSRV.Server_mode == 2:                               #non attivo in warmode
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
        GSRV.PT[frase[0]].warning += 1      #lo warno
        grace = GSRV.WarnMax - GSRV.PT[frase[0]].warning #warning rimasti
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
    if stringa.isdigit():
        return stringa                                                  #comando chiamato tramite routine interna
    if stringa.startswith("#"):                                         #se inizia con cancelletto sto chiamando un clientnumber
        stringa = stringa.lstrip("#")
        return stringa                                                  #ritorno un clientnumber
    for PL in GSRV.PT:
        if str.lower(GSRV.PT[PL].nick).find(str.lower(str.strip(stringa))) != -1: #porto tutto in minuscole e confronto
            slot.append(GSRV.PT[PL].slot_id)
    if len(slot) == 1:
        return slot[0]                                                  #ritorno lo slot se e' univoco
    else:
        tell(richiedente, Lang["nocleartarget"])                        #lo slot non esiste o ne esiste piu di uno corrispondente al pezzo di nome. Se il nome e' ambiguo avverto ed esco
        return ""                                          

#####################################
## FUNZIONI CHIAMABILI DAL PLAYER  ##
#####################################

def alias(richiedente, parametri):      #FUNZIONA
    """espone gli alias di un player"""
    if GSRV.Server_mode == 0:                               #comando non disponibile in fase di avvio
        tell(richiedente, Lang["noavailcmd"])
        return
    target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():
        if GSRV.PT[target].alias == [['']]:
            GSRV.PT[target].alias = [[str(time.time()), str(GSRV.PT[target].nick)],]  #alias vuoto per errore dovuto a crash
        alias = GSRV.PT[target].alias
        frase = Lang["alias"]%str(GSRV.PT[target].nick)
        i = 0
        while alias:
            al = alias.pop()
            frase += str(al[1]) + ", "
            i += 1
            if i == 3:
                tell(richiedente, frase)
                frase = ""
                i = 0
        if i <> 0:
                tell(richiedente, frase)

def balance(richiedente, parametri):    #FUNZIONA
    """Esegue il bilanciamento dei teams"""
    if GSRV.BalanceMode == 0:                                   #balance non attivo
        tell(richiedente, Lang["balanceoff"])
        return
    elif GSRV.BalanceMode == 1:                                #blanciamento manuale
        tell(richiedente, Lang["balancemanual"])
        GSRV.BalanceRequired = True
        return
    elif GSRV.BalanceMode == 2:                             #bilanciamento automatico
        tell(richiedente, Lang["balanceauto"])
        return

def balancemode(richiedente, parametri): #FUNZIONA
    """setta il balancemode"""
    bmode = { 0:"OFF", 1:"Manual", 2:"Auto", }
    if GSRV.BalanceMode == 0:
        GSRV.BalanceMode = 1
        say(Lang["balancemode"]%bmode[GSRV.BalanceMode], 2)
    elif GSRV.BalanceMode == 1:
        GSRV.BalanceMode = 2
        say(Lang["balancemode"]%bmode[GSRV.BalanceMode], 2)
    else:
        GSRV.BalanceMode = 0
        say(Lang["balancemode"]%bmode[GSRV.BalanceMode], 2)

def ban(richiedente, parametri):
    """banna in maniera definitiva"""
    target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():
        say(Lang["ban"] %GSRV.PT[target].nick, 2)
        time.sleep(1)
        GSRV.PT[target].tempban = time.time() + 63072000   #ban per 2 anni
        #if GSRV.PT[target].ip in GSRV.Banlist...
        #GSRV.Banlist.append([])
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

def info(richiedente, parametri):       #TODO finire    #FUNZIONA
    """parametri vari server:IP admin, nextmap,ecc"""
    versione = "^2RedCap ^5%s " %M_CONF.versione
    autore = "^3by bw|Lebbra! ^2IP/Port: ^5"
    server = "%s:%s" %(M_CONF.SocketPars["ServerIP"], M_CONF.SocketPars["ServerPort"])
    tell(richiedente, versione + autore + server)
    tell(richiedente, "^2Players:^3U:%s ^1R:%s ^5B:%s ^2S:%s ^3Servermode:^5%s"%(str(GSRV.TeamMembers[0]), str(GSRV.TeamMembers[1]), str(GSRV.TeamMembers[2]), str(GSRV.TeamMembers[3]), str(GSRV.Server_mode)))

def kick(richiedente, parametri, reason = ""):  #FUNZIONA
    """Kikka un player dal server"""
    if richiedente == "Redcap":                                 #kick richiesto direttamente dal RedCap
        target = parametri
    else:
        target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():                                                   #se ho trovato lo slot
        if reason <> "":
            say(reason, 0)
            time.sleep(1)
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

def mute(richiedente, parametri, reason = ""):
    """Muta/smuta un player"""
    if richiedente == "Redcap":                                 #mute richiesto direttamente dal RedCap
        target = parametri
    else:
        target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():                                                   #se ho trovato lo slot
        if reason <> "":
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

def nukeall():
    pass #TODO da fare

def ora (richiedente, parametri):   #FUNZIONA
    """dice l'ora"""
    tell(richiedente, Lang["ora"] %(time.strftime("%H.%M.%S", time.localtime())))

def password(richiedente, parametri):  #FUNZIONA
    """Setta una password"""
    SCK.cmd("g_password " + parametri.group("pwd"))
    tell(richiedente, Lang["pwdset"])

def rcrestart(richiedente, parametri):
    """restarta il RedCap"""
    say(Lang["restart"], 2)
    tmp = []
    for pl in GSRV.PT:
        tmp.append(GSRV.PT[pl].slot_id)
    for id in tmp:
        say(Lang["salvoplayer"]%GSRV.PT[id].nick, 1)
        clientdisconnect(id)
    import sys
    scrivilog("RIAVVIO RedCap", M_CONF.crashlog)
    sleep(1)
    sys.exit()

def skill(richiedente, parametri):  #FUNZIONA
    """Comunica la skill del player"""
    if not parametri.group("target"):           #richiesta propria skill
        tell(richiedente, Lang["skill"]%(round(GSRV.PT[richiedente].skill, 1), round(GSRV.PT[richiedente].skill_var, 2), GSRV.PT[richiedente].ksmax))
        return
    target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():                                                   #se ho trovato lo slot
        tell(richiedente, Lang["skill"]%(GSRV.PT[target].skill, GSRV.PT[target].skill_var, GSRV.PT[target].ksmax))                    #Invio al socket il comando kick

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
    if target.isdigit():                                            #se ho trovato lo slot
        if reason <> "":
            say(reason, 0)
        for i in range(int(volte)): #Invio al buffer il comando un numero "param[1]" di volte
            SCK.cmd("slap " + target)

def spam(richiedente, parametri):       
    """inserisce/disinserisce frasi di spam)"""
    if parametri.group("un") == "un":                   #sto cancellando
        if parametri.group("frase").isdigit():
            if GSRV.SpamList[int(parametri.group("frase"))].endswith("#"):  #non posso cancellare un record
                tell(richiedente, Lang["norecorderase"])
                return
            del(GSRV.SpamList[int(parametri.group("frase"))])
            spam = open("spam.txt", "w")
            for frase in GSRV.SpamList:
                if frase.endswith("#"):
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
    '''if GSRV.Server_mode == 0:                               #comando non disponibile in fase di avvio
        tell(richiedente, Lang["noavailcmd"])
        return'''
    if not parametri.group("target"):                     #comando status senza target: do nick e slot di tutti
        for player in GSRV.PT:
            tell(richiedente, "^4%s ^%s%s"%(GSRV.PT[player].slot_id, str(GSRV.PT[player].team), GSRV.PT[player].nick))
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
    #tell(richiedente, Lang["top"]%("HSkill", str(GSRV.TopScores["HSkill"][1]), str(GSRV.TopScores["HSkill"][2]), time.strftime("%d.%b %H.%M.%S", time.localtime(GSRV.TopScores["HSkill"][0])))) #TODO HI e LO skill (da fare)
    #tell(richiedente, Lang["top"]%("LSkill", str(GSRV.TopScores["LSkill"][1]), str(GSRV.TopScores["LSkill"][2]), time.strftime("%d.%b %H.%M.%S", time.localtime(GSRV.TopScores["LSkill"][0]))))

def trust(richiedente, parametri):
    """aumenta o diminuisce la affidabilita"""
    pass #TODO

def unwar(richiedente, parametri):   #FUNZIONA
    """resetta il server in modalita' normale"""
    SCK.cmd("g_matchmode 0")
    say(Lang["warunloaded"]%GSRV.Baseconf, 2)
    SCK.cmd("exec %s" %GSRV.Baseconf)                #eseguo la config di base
    GSRV.Server_mode = 1                             #passo in modalita normale

def war(richiedente, parametri):    #FUNZIONA
    """setta il server in modalita' war"""
    tmp = []
    if parametri.group('cfg'):                      #e' stata indicata una configurazione
        for cfg in GSRV.Q3ut4["cfg"]:
            if str.lower(cfg).find(str.lower(str.strip(parametri.group('cfg')))) != -1: #porto tutto in minuscole e confronto
                tmp.append(cfg)
        if len(tmp) == 1:
            say(Lang["warloaded"] %tmp[0], 2)
            SCK.cmd("exec %s" %tmp[0])              #eseguo la config richiesta
        else:
            tell(richiedente, Lang["noclearcfg"])
            return
    else:
        say(Lang["warbaseloaded"]%GSRV.Basewar , 2)
        SCK.cmd("exec %s" %GSRV.Basewar)            #eseguo la config richiesta
    SCK.cmd("reload")                               #avvio la cfg
    GSRV.Server_mode = 2                            #passo in modalita war

'''def z_profiler(routine ="", tim="", modo=""):       #funzione di debug
    if modo == True:
        if routine not in GSRV.z_profiler:
            GSRV.z_profiler[routine] = 0.0
        GSRV.z_profiler[routine] -=  tim
    elif modo == False:
        GSRV.z_profiler[routine] +=  tim
    else:
        for controllo in GSRV.z_profiler:
            print controllo + str(GSRV.z_profiler[controllo])
            for rout in GSRV.z_profiler:
                GSRV.z_profiler[rout] = 0.0
'''
