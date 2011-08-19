#! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import re
import C_DB         #Classe che rappresenta il DB
import C_GSRV       #Classe che rappresenta il gameserver
import C_PLAYER       #Classe per creare players
import C_SOCKET    #Classe socket per comunicazione con UrT
import M_CMD        #Lista comandi
import M_CONF      #Carico le configurazioni programma
import M_SAYS         #dati ausiliari per gestire i say ed i comandi
exec("import M_%s" %M_CONF.RC_lang)            #importo modulo localizzazione linguaggio

Lang = eval( "M_%s.RC_outputs" %M_CONF.RC_lang)

SCK = C_SOCKET.Sock(M_CONF.SocketPars)        #Istanzio il socket
GSRV = C_GSRV.Server(M_CONF.ServerPars)       #Istanzio il gameserver
DB = C_DB.Database(M_CONF.NomeDB)                      #istanzio il DB

##FUNZIONI INTERNE DEL REDCAP##
def balance():
    """Esegue il bilanciamento dei teams"""
    pass

def censura(frase):
    """controlla se nella frase ci sono parole non ammesse"""
    testo=frase.replace(".","") #tolgo i punti dei furbetti.
    for insulto in M_SAYS.censura:
        if re.search(insulto,testo,re.I):                       #ho trovato un insulto
            return True

def clientconnect(id):
    """Gestisce un nuovo client"""
    if id not in GSRV.PT:                                       #Se e un nuovo player (nel senso di appena entrato in game)
        newplayer = C_PLAYER.Player()             #lo creo
        GSRV.player_NEW(newplayer, id, time.time())          #lo aggiungo alla PlayerTable ed ai TeamMember
    else:
        pass        #il player gi� esiste ed e' semplicemente un initgame #TODO vedere se serve

def clientdisconnect(id):
    #TODO fare altre cose prima di cancellarlo, tipo salvare skill e altro (scaricare tutti i parametri player in DB)

    GSRV.player_DEL(id)

def clientuserinfo(info):                                     #info (0=slot_id, 1=ip, 2=guid)
    if GSRV.PT[info[0]].new:                                 #Se e un nuovo player
        GSRV.player_ADDINFO(info)                   #gli aggiungo GUID e IP
    elif info[2] <> GSRV.PT[info[0]].guid:            #cambio guid durante il gioco #TODO registrare il cambio guid???
        GSRV.PT[info[0]].notoriety += M_CONF.Notoriety["guidchange"]               #gli abbasso la notoriety in proporzione
        kick("Redcap", info[0], Lang["guidchange"]%info[1])

def clientuserinfochanged(info):                    #info (0=id, 1=nick, 2=team)
    if GSRV.PT[info[0]].invalid_guid():                                                          #CONTROLLO VALIDITA GUID (adesso che ho pure il nick!)
        GSRV.PT[info[0]].notoriety += M_CONF.Notoriety["badguid"]               #abbasso la notoriety
        kick("Redcap", info[0], Lang["invalidguid"]%info[1])                              #e lo kikko        #TODO  registrare nick e ip in DB o in log
        return  #inutile andare avanti
    if GSRV.PT[info[0]].invalid_nick(GSRV.Nick_is_length, GSRV.Nick_is_good, info[1]):    #CONTROLLO VALIDITA NICK (non ancora assegnato al player!)
        kick("Redcap", info[0], Lang["invalidnick"]%info[1])
        return   #inutile andare avanti
    res = GSRV.userinfochanged(info)                                                            #Aggiorno NICK e TEAM
    if GSRV.PT[info[0]].new:                                                                         #PLAYER APPENA CONNESSO
        res = False                                                                                            #non ha cambiato nick, inutile controllare gli alias.
        db_datacontrol(GSRV.PT[info[0]].guid, info[0])                                     #controllo se il player esiste nel DB e ne recupero i dati (tb DATA) se no lo registro
        if GSRV.PT[info[0]].tempban <= time.time():                                         #non e pi� bannato (o non lo era)
            GSRV.PT[info[0]].tempban = 0.0
        else:                                                                                                      #e ancora bannato
            ban = time.strftime("%d.%b.%Y %H.%M.%S", time.localtime(GSRV.PT[info[0]].tempban))
            kick("Redcap", info[0], Lang["stillban"]%(GSRV.PT[info[0]].nick, ban))
            return
        if GSRV.PT[info[0]].notoriety < GSRV.MinNotoriety:
            kick("Redcap", info[0], Lang["lownotoriety"]%(info[1],GSRV.PT[info[0]].notoriety,GSRV.MinNotoriety))
            return
            GSRV.PT[info[0]].new = False                                                            #non e piu nuovo
            saluta(M_CONF.saluti)                                                                      #chiamo la funzione che si occupa eventualmente di salutare il player
    if res:                                                                                                     #CONTROLLO ALIAS (solo per player non nuovi)
        esiste = False
        for alias in GSRV.PT[id].alias:
            if nome in alias:
                esiste = True
                alias[0] = str(time.time())                                                             #se esiste aggiorno la data di ultimo utilizzo
        if not esiste:
            GSRV.PT[id].alias.append([str(time.time()), nome])                         #se non esiste lo aggiungo

       # db_loccontrol(GSRV.PT[info[0]].guid)        #controllo il player nel DB (tb LOC)

def comandi (frase):                                 # frase [id, testo] (es: "2:31 say: 3 Nero: !slap Cobr4" diventa: ["3", "!slap Cobr4"]
    """processo il comando prima di inviarlo alla finzione specializzata"""
    if frase[0]not in GSRV.PT:   #potrebbero partire dei say prima del ClientBegin, dando errore "KeyError: '0'
        return
    for comando in M_CMD.comandi:                           #comando ["nomecomando","regex", livello]
        res = re.search(comando[1], frase[1], re.I)          #Individuo il tipo di comando
        if res:                                                              #Ho trovato un comando
            if GSRV.PT[frase[0]].level < comando[2]:
                tell(frase[0], Lang["nolevel"] %(str(comando[2]), GSRV.PT[frase[0]].level))        #player non autorizzato
            else:
                risp = eval("%s(frase[0],res)" %comando[0]) #eseguo il comando e gli passo richiedente e parametri
            break
        else:
             tell(frase[0], Lang["wrongcmd"] )  #comando non riconosciuto

def cr_floodcontrol():
    """verifica (periodica) che nessun player abbia fatto flood"""
    for PL in GSRV.PT:
        if GSRV.PT[PL].flood >= GSRV.MaxFlood:
            #TODO gli abbasso la notoriety
            kick("Redcap", GSRV.PT[PL].slot_id, Lang["flood"]%GSRV.PT[PL].nick)
        else:
            GSRV.PT[PL].flood = 0        #Se non e kikkato lo rimetto a zero

def cr_full():
    """verifica se il server � pieno"""
    pass #TODO fare

def cr_nickrotation():
    """verifica (periodica) che nessun player abbia fatto nickrotation"""
    for PL in GSRV.PT:
        if GSRV.PT[PL].nickchanges > GSRV.MaxNickChanges:
            #TODO gli abbasso la notoriety
            kick("Redcap", GSRV.PT[PL].slot_id, Lang["nickchanges"]%(GSRV.PT[PL].nick, GSRV.PT[PL].nickchanges))
        else:
            GSRV.PT[PL].nickchanges = 0        #Se non e' kikkato lo rimetto a zero

def cr_unvote():
    """verifica (periodica) che il voto non sia rimasto attivo dopo il comando !v"""
    if GSRV.VoteMode and ((time.time() - GSRV.LastVote) > M_CONF.voteTime):
        GSRV.VoteMode = False

def cr_warning():
    """verifica se qualche player ha troppi warning"""
    for PL in GSRV.PT:
        if GSRV.PT[PL].warning >= M_CONF.max_warns:
            #TODO gli abbasso la notoriety
            kick("Redcap", GSRV.PT[PL].slot_id, Lang["warning"]%GSRV.PT[PL].nick)

def db_datacontrol(guid,id):
    """Applicato ai player appena connessi: recupera i valori della tabella DATA, o se il player non � registrato lo registra"""
    DB.connetti()
    res = DB.esegui(DB.query["cercadati"], (guid,)).fetchone()
    if res:                                                                     # ESISTE IN DB (guid, DBnick, skill, rounds, lastconn, level, tempban, notoriety, firstconn, streak, alias)
        GSRV.PT[id].DBnick = res[1]
        GSRV.PT[id].skill = res[2]
        GSRV.PT[id].rounds = res[3]
        GSRV.PT[id].lastconnect = res[4]                                   #data dell'ultima connessione
        GSRV.PT[id].level = res[5]
        GSRV.PT[id].tempban = res[6]
        GSRV.PT[id].guidage = (time.time() - res[8])/87400      #eta' della guid in giorni
        GSRV.PT[id].notoriety = res[3] / M_CONF.Notoriety["roundXpoint"] + GSRV.PT[id].guidage / M_CONF.Notoriety["dayXpoint"] + res[7]    #calcolo della notoriety (basata su round, guid age, e bonus/malus)
        GSRV.PT[id].ksmax = res[9]
        aliases = res[10].split(u'\xa7')                                            #formatto gli alias in maniera leggibile
        for al in aliases:
            al=al.split("#")
            if time.time() - float(al[0])/87400 < GSRV.AliasDuration:       #l'alias e' ancora valido
                GSRV.PT[id].alias.append(al)
    else:                                                                       #NON ESISTE IN DB: gli assegno i valori non ancora assegnati e lo registro inserendo guid e nick #TODO vedere per aggiunta IP
        alias = str(time.time())+"#"+GSRV.PT[id].nick               #gli assegno il suo primo alias
        GSRV.PT[id].alias = alias.split("#")
        DB.esegui(DB.query["newdati"], (GSRV.PT[id].guid, GSRV.PT[id].nick, 0, 0, GSRV.PT[id].lastconnect, 0, 0.0, 0, time.time(), 0, alias))
        DB.esegui(DB.query["newdeath"], (GSRV.PT[id].guid,))
        DB.esegui(DB.query["newhit"], (GSRV.PT[id].guid,))
        DB.esegui(DB.query["newkill"], (GSRV.PT[id].guid,))
        DB.esegui(DB.query["newloc"], (GSRV.PT[id].guid,)) 
    DB.salva()
    #TODO recuperare anche gli altri dati dalle altre tabelle?
    DB.disconnetti()

def db_loccontrol(guid):
    DB.connetti()
    res = DB.esegui(DB.query["cercaloc"], (guid,)).fetchone()
    if res:                                                             # esiste in db (guid, IP, provider, location, old_guids)
        pass #TODO recuperare IP ,provider location, old_guids


def endMap(frase):
    pass        #TODO

def endRound(frase):
    pass        #TODO

def hits():
    pass        #TODO

def initGame(frase):    # frase (0=matchmode, 1=gametype, 2=maxclients,3=mapname)
    """Operazioni da fare a inizio mappa"""
    GSRV.MatchMode = frase[0]
    GSRV.Gametype = frase[1]
    GSRV.MaxClients = frase[2]
    GSRV.MapName = frase[3]
    GSRV.Startup_end = True            #Finisce la fase di startup (se non era gia finita)

def initRound(frase):
    GSRV.teamskill_eval()                                # aggiorno le teamskill
    pass        #TODO

def kills(frase):
    pass        #TODO

def saluta(modo):
    """si occupa di salutare il player al suo ingresso in game"""
    if modo == 0:
        return
    elif modo == 1:          #se saluti <> 0 allora saluto.
        say(Lang["saluti1"]%info[1])
    elif modo == 2:
        say(Lang["saluti2"]%(info[1], GSRV.PT[info[0]].nick))
    elif modo == 3:
        say(Lang["saluti3"]%(info[1], GSRV.PT[info[0]].nick, GSRV.PT[info[0]].skill, GSRV.PT[info[0]].notoriety))

def says(frase):                                                       #frase (0=id, 1=testo)
    if frase[0]not in GSRV.PT:   #potrebbero partire dei say prima del ClientBegin, dando errore "KeyError: '0'
        return
    GSRV.PT[frase[0]].flood += 1
    if censura(frase[1]):                              #ho trovato un insulto
        GSRV.PT[frase[0]].warning += 1      #lo warno
        grace = M_CONF.max_warns - GSRV.PT[frase[0]].warning #warning rimasti
        slap("Redcap", (1, frase[0]), Lang["insults"]%grace)   #lo slappo
            
def trovaslotdastringa(richiedente, stringa):
    """recupera lo slot del target dalla stringa"""
    slot = []
    if stringa.isdigit():
        return stringa                                                    #comando chiamato tramite routine interna
    if stringa.startswith("#"):                                       #se inizia con cancelletto sto chiamando un clientnumber
        stringa = stringa.lstrip("#")
        return stringa                                                        #ritorno un clientnumber
    for PL in GSRV.PT:
        if str.lower(GSRV.PT[PL].nick).find(str.lower(str.strip(stringa))) != -1: #porto tutto in minuscole e confronto
            slot.append(GSRV.PT[PL].slot_id)
    if len(slot) == 1:
        return slot[0]                                                    #ritorno lo slot se e' univoco
    else:
        tell(richiedente, Lang["nocleartarget"])                #lo slot non esiste o ne esiste piu di uno corrispondente al pezzo di nome. Se il nome e' ambiguo avverto ed esco
        return ""                                          

###############
##COMANDI RCON ##
###############

def callvote(richiedente, parametri):
    """Chiama il voto di vario tipo"""
    past = (time.time() - GSRV.LastVote)/60
    if  past < M_CONF.timeBetweenVote:               #controllo se e' passato tempo sufficiente
        say(Lang["notimetocmd"] %(int(M_CONF.timeBetweenVote - past)), 0)   #se non e' trascorso il tempo informo di aspettare
    else:
        SCK.cmd(" g_allowVote " + str(M_CONF.voteType))     # abilito il voto
        say(Lang["voteON"] %(M_CONF.voteTime), 0)
        GSRV.LastVote = time.time()                          #aggiorno il time di ultima votazione
        GSRV.VoteMode = True                                       #il voto e' abilitato

def cyclemap(richiedente, parametri):
    """esegue un cyclemap. Non si puo' dare piu spesso di RCconf.Tcyclemap"""
    past = (time.time() - GSRV.LastMapChange)/60
    if  past < M_CONF.Tcyclemap:
        say(Lang["notimetocmd"] %(int(M_CONF.Tcyclemap - past)), 0)   #se non e' trascorso il tempo informo di aspettare
    else:
        GSRV.LastMapChange = time.time()
        SCK.cmd(" cyclemap")

def forceteam(richiedente, parametri): #param richiedente target colore
    """forza il player target in un team o spect"""
    if richiedente == "Redcap":                                 #force richiesto direttamente dal RedCap
        target = parametri[0]
        team = parametri[1]
    else:
        team = {"r":"red","b":"blue","s":"spectator"}[parametri.group("target").lower()]
        target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():
        SCK.cmd("forceteam " + target + " " + team)

def kick(richiedente, parametri, reason = ""):
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

def mute(richiedente, parametri, reason = ""):
    """Muta/smuta un player"""
    if richiedente == "Redcap":                                 #mute richiesto direttamente dal RedCap
        target = parametri
    else:
        target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():                                                   #se ho trovato lo slot
        if reason <> "":
            say(reason, 0)
        SCK.cmd("mute " + target)                                 #Invio al socket il comando mute
        
def nuke(richiedente, parametri):
    """equivalente a "nuke" da console"""                   #TODO fare il nuke a morte
    if richiedente == "Redcap":                                 #mute richiesto direttamente dal RedCap
        target = parametri
    else:
        target = trovaslotdastringa(richiedente, parametri.group("target"))
    if target.isdigit():                                                   #se ho trovato lo slot
         SCK.cmd("nuke " + target)
         say(Lang["nuked"]%(GSRV.PT[target].nick),0)

def nukeall():
    pass #TODO da fare

def ora (richiedente, parametri):
    """dice l'ora"""
    tell(richiedente, Lang["ora"] %(time.strftime("%H.%M.%S", time.localtime())))

def password (richiedente, parametri):
    """Setta una password"""
    SCK.cmd("password " + parametri.group("pwd"))
    tell(richiedente, Lang["pwdset"])


def level (richiedente, parametri):
    """assegna il livello ad un player"""
    pass #TODO

def say(testo,modo):
    """Manda messaggi pubblici da console. 0=say, 1=console, 2=bigtext"""
    modi= {
    0 : 'say ',
    1 : '',
    2 : 'bigtext '}
    SCK.cmd(modi[modo] + testo)

def slap(richiedente, parametri, reason=""):
    """equivalente a "slap" da console, ma puo' essere chiamato piu' volte di fila"""
    if richiedente == "Redcap":                                 #force richiesto direttamente dal RedCap
        target = parametri[1]
        volte = parametri[0]
    else:
        target = trovaslotdastringa(richiedente, parametri.group("target"))
        if parametri.group("num").isdigit():
            volte = parametri.group("num")
            if volte > M_CONF.maxSlap:
                volte = M_CONF.maxSlap
        else:
            volte = 1
    if target.isdigit():                                            #se ho trovato lo slot
        if reason <> "":
            say(reason, 0)
        for i in range(int(volte)): #Invio al buffer il comando un numero "param[1]" di volte
            SCK.cmd("slap " + target)

def tell(target,testo):
    """Invia un messaggio privato a target. Equivalente a "tell" da console. """
    SCK.cmd("tell " + target + " " + testo)