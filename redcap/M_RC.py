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
Saluti = eval( "M_%s.RC_saluti" %M_CONF.RC_lang)
Logs = eval("M_%s.RC_logoutputs" %M_CONF.RC_lang)
Killz = eval("M_%s.RC_kills" %M_CONF.RC_lang)

SCK = C_SOCKET.Sock(M_CONF.SocketPars)                          #Istanzio il socket
GSRV = C_GSRV.Server(M_CONF.ServerPars, M_CONF.sv_SkillPars, M_CONF.sv_WarnPars)       #Istanzio il gameserver
DB = C_DB.Database(M_CONF.NomeDB)                               #Istanzio il DB

##Parametri per le kill
normalKills = ['12', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '25', '28', '30', '35', '38', '40' ]
accident = ['6', '9', '31']
suicide = '7'
kick = '24'
nuked = '34'

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
        pass        #il player gia' esiste ed e' semplicemente un initgame #TODO vedere se serve

def clientdisconnect(id):
    """Operazioni da fare alla disconnessione"""
    if id not in GSRV.PT:
        return                              #nel log raramente capitano anche 2 clientdisconnect dello stesso player di seguito
    if GSRV.PT[id].justconnected:
        GSRV.player_DEL(id)                 #se e' un justconnected non accettato per badnick o badguid non salvo nulla in db
        return
    alias = GSRV.PT[id].alias_to_db()
    DB.connetti()
    DB.esegui(DB.query["salvadati"], (GSRV.PT[id].DBnick, GSRV.PT[id].skill, GSRV.PT[id].rounds, GSRV.PT[id].lastconnect, GSRV.PT[id].level, GSRV.PT[id].tempban, GSRV.PT[id].reputation, GSRV.PT[id].ksmax, alias, GSRV.PT[id].guid ))    #salvo in tabella DATI
    #TODO salvare altre tabelle
    DB.salva()
    DB.disconnetti()
    GSRV.player_DEL(id)

def clientuserinfo(info):                       #info (0=slot_id, 1=ip, 2=guid)
    if GSRV.PT[info[0]].justconnected:                     #Se e un nuovo player
        GSRV.player_ADDINFO(info)                   #gli aggiungo GUID e IP
    elif info[2] <> GSRV.PT[info[0]].guid:            #cambio guid durante il gioco #TODO registrare il cambio guid???
        GSRV.PT[info[0]].notoriety += M_CONF.Notoriety["guidchange"]            #gli abbasso la notoriety in proporzione
        kick("Redcap", info[0], Lang["guidchange"]%info[1])

def clientuserinfochanged(info):                #info (0=id, 1=nick, 2=team)
    if GSRV.PT[info[0]].invalid_guid():                                                             #CONTROLLO VALIDITA GUID (adesso che ho pure il nick!)
        GSRV.PT[info[0]].notoriety += M_CONF.Notoriety["badguid"]               #abbasso la notoriety
        kick("Redcap", info[0], Lang["invalidguid"]%info[1])                    #e lo kikko         #TODO  registrare nick e ip in DB o in log
        return  #inutile andare avanti
    if GSRV.PT[info[0]].invalid_nick(GSRV.Nick_is_length, GSRV.Nick_is_good, info[1]):              #CONTROLLO VALIDITA NICK (non ancora assegnato al player!)
        kick("Redcap", info[0], Lang["invalidnick"]%info[1])
        return   #inutile andare avanti
    res = GSRV.player_USERINFOCHANGED(info)                                     #Aggiorno NICK e TEAM (se res True, il player ha cambiato nick (o e' nuovo)
    if GSRV.PT[info[0]].justconnected:                                                              #PLAYER APPENA CONNESSO
        res = False                                                             #non ha cambiato nick, inutile controllare gli alias. TODO da togliere se justconnect sparisce alla disconnessione
        db_datacontrol(GSRV.PT[info[0]].guid, info[0])                          #controllo se il player esiste nel DB e ne recupero i dati (tb DATA) se no lo registro
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
        GSRV.PT[info[0]].lastconnect = time.time()                              #aggiorno il lastconnect
        GSRV.PT[info[0]].skill_coeff_update()                                   #aggiorno il coefficiente skill
        GSRV.PT[info[0]].justconnected = False                                  #non e piu nuovo
        saluta(M_CONF.saluti, info[0])                                          #chiamo la funzione che si occupa eventualmente di salutare il player
    if res:                                                                     #CONTROLLO ALIAS (solo per player NON nuovi)
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
                #TODO inserire il controllo di bot in pausa
                eval("%s(frase[0],res)" %comando[0])    #eseguo il comando e gli passo richiedente e parametri
            break
        else:
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
    """verifica se il server e' pieno"""
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
        if GSRV.PT[PL].warning >= M_CONF.Warning["max_warns"]:
            #TODO gli abbasso la notoriety?
            kick("Redcap", GSRV.PT[PL].slot_id, Lang["warning"]%GSRV.PT[PL].nick)

def db_datacontrol(guid,id):
    """Applicato ai player appena connessi: recupera i valori della tabella DATA, o se il player non e' registrato lo registra"""
    DB.connetti()
    dati = DB.esegui(DB.query["cercadati"], (guid,)).fetchone()    # PROVO A CARICARE da TABELLA DATI
    if dati:                                                                    #se ESISTE IN DB recupero i dati (guid, DBnick, skill, rounds, lastconn, level, tempban, notoriety, firstconn, streak, alias)
        GSRV.PT[id].isinDB = True                                               #esiste gia nel DB
        GSRV.PT[id].dati_load(dati, M_CONF.Notoriety["roundXpoint"], M_CONF.Notoriety["dayXpoint"], time.time())
        #TODO caricare i dati anche dalle altre tables?
    else:                                                                                  #se NON ESISTE IN DB: gli assegno i valori non ancora assegnati e lo registro inserendo guid e nick
        GSRV.PT[id].DBnick = GSRV.PT[id].nick                           #gli assegno il DBnick (potra' essere cambiato in seguito con il comando !nick)
        GSRV.PT[id].alias = [[str(time.time()), GSRV.PT[id].nick]]    #gli assegno il suo primo alias
        alias = str(time.time()) + " " + GSRV.PT[id].nick               #alias scritto nella forma per database
        DB.esegui(DB.query["newdati"], (GSRV.PT[id].guid, GSRV.PT[id].nick, 0, 0, GSRV.PT[id].lastconnect, 0, 0.0, 0, time.time(), 0, alias))
        DB.esegui(DB.query["newdeath"], (GSRV.PT[id].guid,))
        DB.esegui(DB.query["newhit"], (GSRV.PT[id].guid,))
        DB.esegui(DB.query["newkill"], (GSRV.PT[id].guid,))
        DB.esegui(DB.query["newloc"], (GSRV.PT[id].guid, GSRV.PT[id].ip))    #gli salvo il suo primo IP
        DB.salva()
    DB.disconnetti()

def db_loccontrol(guid):    #TODO unused
    DB.connetti()
    res = DB.esegui(DB.query["cercaloc"], (guid,)).fetchone()
    if res:                                                             # esiste in db (guid, IP, provider, location, old_guids)
        pass #TODO recuperare IP ,provider location, old_guids


def endMap(frase):
    pass        #TODO salvare i record

def endRound(frase):
    pass        #TODO

def hits():
    pass        #TODO

def initGame(frase):    # frase (0=matchmode, 1=gametype, 2=maxclients, 3=mapname)
    """Operazioni da fare a inizio mappa"""
    #recupero le modalita' server
    GSRV.MatchMode = frase[0]
    GSRV.Gametype = frase[1]
    GSRV.MaxClients = frase[2]
    GSRV.MapName = frase[3]
    GSRV.Startup_end = True            #Finisce la fase di startup (se non era gia finita)

def initRound(frase):
    if GSRV.Startup_end:
        GSRV.teamskill_eval()                           #aggiorno le teamskill e il coefficiente di sbilanciamento skill
        GSRV.players_alive()                            #setto i player non spect a vivo, gli aggiungo un round e updato il coeff skill.
    #TODO settare i player non spect a vivo
    testo = " ^7U " + str(GSRV.TeamMembers[0]) + "^1R " + str(GSRV.TeamMembers[1]) + "^4B " + str(GSRV.TeamMembers[2]) + "^2S " + str(GSRV.TeamMembers[3]) #DEBUG
    print testo
    say(testo, 1) #DEBUG

def kills(frase):                                       #frase del tipo ['0', '0', '10'] (K,V,M)
    if frase[1] not in GSRV.PT:                         #in rari casi il player può essere hittato dopo clientdisconnect
        return
    GSRV.PT[frase[1]].vivo = 2                          #in ogni caso setto la vittima a "morto"
    if frase[2] == '10':                                #CHANGETEAM  #TODO gestire il changeteam  se necessario
        return
    if frase[2] in normalKills :                                                            #KILL DA ARMA
        if GSRV.is_tkill(frase[0], frase[1]):
            tell(GSRV.PT[frase[0]].slot_id, Lang["tkill"] %str(GSRV.PT[frase[0]].warning))  #TEAMKILL
            return
        GSRV.skill_variation(frase[0],frase[1])         #funzione che calcola ed assegna la variazione skill ai due players
        res0 = GSRV.is_kstreak(frase[0],frase[1])       #calcolo variazioni kstreak (eventuale spam)
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
        if 128 in res:
            say(Killz[0]%(GSRV.PT[frase[0]].nick, GSRV.PT[frase[1]].nick), 2)               #spammo stop ks in bigtext
        elif 256 in res:
            say(Killz[0]%(GSRV.PT[frase[0]].nick, GSRV.PT[frase[1]].nick), 0)               #spammo stop ks in console
        GSRV.PT[frase[0]].kills[frase[2]] += 1          #aggiungo la kill alle statistiche
    elif frase[2] in accident :                                                             #INCIDENTE
        pass                                            #TODO vedere se si vuole contare
    elif frase[2] == suicide:                                                               #SUICIDIO
        GSRV.PT[frase[1]].skill -= GSRV.Sk_penalty / GSRV.Sk_Kpp     #penalizzo la skill
    elif frase[2] == kick:                                                                  #KICKED
        pass                                            #TODO vedere se si vuole contare
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

def saluta(modo, id):
    """si occupa di salutare il player al suo ingresso in game"""
    X = {
    1: GSRV.PT[id].nick,
    2: GSRV.PT[id].DBnick,
    4: GSRV.PT[id].skill,
    8: GSRV.PT[id].notoriety,
    16: time.strftime("%d %b", time.localtime(GSRV.PT[id].lastconnect)),
    }
    opzioni = option_checker(modo)
    saluto = ""
    while opzioni:
        opz = opzioni.pop()
        saluto += Saluti[opz]%X[opz]
    if saluto <> "":
        say(saluto, 0)
    #print saluto #DEBUG
   
def says(frase):                 #frase (0=id, 1=testo)
    #print frase[1] #DEBUG
    if frase[0]not in GSRV.PT:   #potrebbero partire dei say prima del ClientBegin, dando errore "KeyError: '0'
        return
    GSRV.PT[frase[0]].flood += 1
    if censura(frase[1]):                              #ho trovato un insulto
        GSRV.PT[frase[0]].warning += 1      #lo warno
        grace = GSRV.WarnMax - GSRV.PT[frase[0]].warning #warning rimasti
        slap("Redcap", (1, frase[0]), Lang["insults"]%grace)   #lo slappo

def scrivilog(evento, nomelog):          #TODO separare i log per argomenti e fare log di debug
    """scrive il messaggio "evento" nel file di log di RedCap"""
    evento = (time.strftime("%d.%b %H.%M.%S", time.localtime()) + ": " + evento + "\r\n")
    f = open(GSRV.Logfolder + "/" + nomelog, "a")
    f.write(evento)
    f.close()
            
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
