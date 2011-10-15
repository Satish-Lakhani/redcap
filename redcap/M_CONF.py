#! /usr/bin/python
# -*- coding: utf-8 -*-

versione = "1.00 Alpha"         #RedCap Version. !!! PLEASE ADD "-MOD by YOURNAME" TO THE VERSION NUMBER IF YOU MODIFY SOMETHING OF THE SCRIPT OUTSIDE OF THIS CONFIGURATION FILE. !!!

'''########## (OBBLIGATORIO!) = CONFIGURAZIONE OBBLIGATORIA ###########'''

##DATABASE
NomeDB = "Rc_DB.sqlite"          #nome DB (se si cambia rinominare anche il file corrispondente)
#minRounds = 60                  #numero minimo di round giocati per apparire nelle statistiche
#maxAbsence = 25                 # giorni di assenza prima di essere cancellati dal server

##LIVELLI COMANDI (Max lev = 100):
lev_alias = 2                   #mostra gli alias di un player
lev_admin = 2                   #livello a partire dal quale un player e' considerato admin (riceve piu' info in risposta a certi comandi, ed il fatto che sia presente abilita o disabilita alcune funzionalita del bot)
lev_balancemode = 2             #inserisce/disinserisce l'autobalance
lev_balance = 0                 #bilanciare team
lev_ban = 4                     #ban
lev_callvote = 0                #chiama voto
lev_cycle = 2                   #cyclemap
lev_dbnick = 3                  #assegna il nick corrente come nick in DB
lev_esegui = 4                  #esegue un qualsiasi comando rcon
lev_force = 2                   #forceteam
lev_info = 0                    #mostra server IP e versione redcap
lev_kick = 2                    #kick
lev_level = 4                   #assegno level
lev_map = 2                     #cambio mappa
lev_mute = 1                    #mute
lev_muteall = 2                 #mute all
lev_nuke = 0                    #nuke #DEBUG
lev_ora = 0                     #dice l'ora
#lev_passport = 3               #attiva/disattiva il passport
lev_password = 3                #setta una password
#lev_pause = 3                  #mette il bot in pausa
lev_RCrestart = 4               #restart
#lev_reg = 3                    #registrazione in DB ed assegnazione passport
lev_skill = 0                   #mostra skill del player
lev_slap = 2                    #slap
lev_spam = 2                    #inserisce/disinserisce frasi spam
lev_spamlist = 0                #lista le frasi spam
lev_status = 0                  #status (informazioni varie sul player)
lev_tmpban = 2                  #ban temporaneo
lev_top = 0                     #mostra i top record
lev_trust = 3                   #aggiunge/leva notoriety ad un player
#lev_unreg = 3                  #toglie il passport
lev_war = 0                     #configurazione per war
lev_unwar = 0                   #eliminare configurazione war

##LOGS: i log sono reperibili nella cartella logs e sono i seguenti
crashlog = "crash.log"              #eventi di crash del server
socketlog = "socket.log"            #comandi non inviati
commandlog = "command.log"          #comandi bot inviati dai giocatori
commandlogMinLevel = 0              #livello minimo del comando affinche sia registrato nel log (settare piu alto del piu alto dei livelli di comando se non si vuole registrare nulla)

##NOTORIETY
# valore di notoriety aggiunto a quella del player in caso di alcuni avvenimenti. Quando la notoriety scende al di sotto di ServerPars["MinNotoriety"] il player non puo' piu accedere al server.
Notoriety = {
"guidchange" : -5,          #penalizzazione punti per cambio guid al volo (probabile cheat)
"badguid" : -20,            #penalizzazione punti per guid non corretta (probabile cheat)
"roundXpoint": 100,         #num. di round da giocare per guadagnare un punto notoriety
"dayXpoint": 10             #giorni di anzianita della guid per guadagnare un punto notoriety
}

##FILE TESTO
NomeFileLog = "AUXILIARY/prova.log"   #2011_Sep_01_log.log" #" # DEBUG"../games.log"    #(OBBLIGATORIO!) Percorso relativo del file di log da controllare
SpamFile = "spam.txt"

##PLAYER
KickForSpace = True         #se true kikka uno spect (se c'e') quando il server e' pieno
maxSlap = 10                        #massimo numero di slap che posso dare ad un player

##RECORD
MinPlayers = 6              #numero minimo di players per considerare valido un record
MinNotoriety = 0            #notoriety minima per segnare un record

#CONSOLE SPAMS
RecordSpam = True       #Se True, Redcap spamma periodicamente i record, se False non spamma
CustomSpam = True       #Se True, Redcap spamma periodicamente le frasi scritte in RT_SPAM.txt, se False non spamma
Spamtime = 140          #Tempo in secondi tra due spam

#REDCAP
botname = "^8RC| "             #prefisso degli output del Redcap (lasciare vuoto "" se non si vuole prefisso) #TODO non utilizzato
RC_lang = "ITA"                    #Localizzazione linguaggio ITA #TODO (ENG FRA e altre, da fare)
AdminGuids = ["0606EE61D6F696AAE452385F765D78CF"]                  #guid automaticamente abilitata al max liv di autorizzazione

##SERVER
ServerPars = {
"AliasDuration": 90,                #tempo di memorizzazione in giorni di un vecchio alias prima che sia cancellato per inutilizzo
"AntiReconInterval" : 0,            #Tempo di antireconnect in sec (se 0  = Disattivato)
"BalanceMode" : 2,                  #0=disattivato 1=attivato 2=automatico
"Baseconf" : "server.cfg",          #nome della configurazione standard del gameserver
"Basewar" : "basewar.cfg",          #nome della config minima per cw che viene caricata se non ce ne sono altre
"FloodControl" : True,              #Flood control abilitato = True, disabilitato = false (TODO comando per abilitare disabilitare da chat?)
"goodNick":r"[a-zA-Z]",             #Regex minima che il nick deve soddisfare.
"Logfolder": "logs",                #cartella di registrazione dei log
"MaxFlood" : 6,                     #massimo numero di say in un tempo fissato (CRON1)
"MaxNickChanges" : 3,               #massimi change nick in un tempo fissato (CRON1)
"MinNotoriety": -999,               #valore notoriety per giocare nel server. La notoriety di un nuovo player e' 0
"minNick":3,                        #Lunghezza minima nick
"Passport" : False,                 #True=passport attivo gia' all'avvio, False=passport inattivo all'avvio.
"ShowHeadshots": True,              #Se True mostra gli headshot
"UrtPath" : "../../../../home/ale/UT/q3ut4",            #path relativo della cartella q3ut4 di urt  #DEBUG
"MapCycle": "mycycle.txt"           #path del file di cyclemap
}

StandardMaps = [                    #mappe standard incluse nello z_pack
"ut4_abbey",
"ut4_algiers",
"ut4_ambush",
"ut4_austria",
"ut4_casa",
"ut4_crossing",
"ut4_eagle",
"ut4_elgin",
"ut4_harbortown",
"ut4_kingdom",
"ut4_mandolin",
"ut4_maya",
"ut4_oildepot",
"ut4_prague",
"ut4_ramelle",
"ut4_riyadh",
"ut4_sanctuary",
"ut4_suburbs",
"ut4_subway",
"ut4_swim",
"ut4_thingley",
"ut4_tombs",
"ut4_toxic",
"ut4_tunis",
"ut4_turnpike",
"ut4_uptown",
]

##SKILL (parametri per la formula skill)
#NOTA: punteggio approssimativo di mappa che un giocatore a skill 1000 deve ottenere per mantenere la skill invariata:
#ES. range=300: score: 785-1; range=500: 55-1;  range=600: 28-1; range=700: 17-1; range=800: 12-1; range=900: 9-1; range=1000: 7-1; range=3000: 2-1;
sv_SkillPars = {
"Sk_team_impact" : 0.3,              #percentuale della skill calcolata in base alla teamskill avversaria (il resto e' calcolato in base alla skill dell'avversario diretto)
"Sk_Kpp" : 5,                        #numero di kill (a delta skill 0) necessarie per guadagnare un punto skill.
"Sk_range" : 800,                    #piu grande e il valore, piu alti sono i valori di skill che si possono raggiungere.
"Sk_penalty" : 4,                    #penalita' per teamkill (espressa come n. di kill da fare per bilanciare una penalty)
"Ks_min" : 5,                        #minima streak affinche' il bot segnali la killstreak
"Ks_not" : 0,                        #minima notoriety per segnalazione killstreak
"Ks_show": 5,                       #minima ks per segnalazione in chat
"Ks_showbig": 9,                    #minima ks per segnalazione in bigtext
}

## SOCKET
SocketPars = {
"ServerRcon" : "xxxxxx",          #(OBBLIGATORIO!) rconpassword (inserire la password di rcon fra le virgolette)
"ServerIP" : "217.199.3.245",      #(OBBLIGATORIO!) IP del gameserver
"ServerPort" : 27960,              #(OBBLIGATORIO!) Porta del gameserver
"ServerTimeout" : 1,               #(OBBLIGATORIO!) Secondi di attesa risposta server a comando rcon (NON CAMBIARE!)
"Tsleep" : 0.8,                     #(OBBLIGATORIO!) Tempo di attesa tra due comandi rcon successivi  (NON CAMBIARE!)
"ServerLog":  ServerPars["Logfolder"] + "/" + socketlog   #nome del log dove il socket registra i suoi errori.
}

##STATUS Sommare i parametri desiderati
'''
1: Benvenuto %nome
2: Skill
4: Istskill
8: Streak
16: Rounds
32: Affidabilita
64: Slot
128: Nick ufficiale
256: IP
512: Level
1024: Warning
2048: Ultima visita
4096: Alias
'''
saluti = 1 + 2048                                                           #informazioni di saluto
status = 1 + 32 + 128 + 4096 + 2048                                         #informazioni date ai non admin
status_adm = 1 + 8 + 16 + 32 + 64 + 128 + 256 + 512 + 2048 + 1024           #info date agli admin

##TEMPI
Control_Daily = 6       #ora alla quale vengono eseguite le operazioni periodiche giornaliere
CRON1 = 15              #Frequenza in sec del cron1 (cronometro veloce)
CRON2 = 3600            #Frequenza in sec del cron1 (cronometro lento)
Tcyclemap = 12          #tempo in minuti che deve intercorrere tra due cyclemap
TempoCiclo = 0.5        #Frequenza in sec del controllo del log
Ttempban = 96           #durata massima tempban

##VOTO
voteTime = 30,                        #tempo di abilitazione del voto
voteType =536870986            #modalita' di voto temporanea (see http://www.urbanterror.info/docs/texts/123/#2.2)
unvoteType = 0                       #modalita' di voto permanente (0 esclude qualsiasi tipo di voto)
timeBetweenVote = 3            #tempo in minuti che deve intercorrere tra due voti

##WARNING
sv_WarnPars = {
"max_warns" : 5.0,                   #valore di warning dopo di che vieni kikkato  (si azzerano al reconnect). Uno slap dati da Redcap o un tk o un hit comportano automaticamente un warning.
"adm_warn" : 1.0,                    #valore di uno warn dato da un admin
"tk_warn" : 1.0,                     #valore di uno warn causato da un tk (in realta' un tk vale circa tk_warn + 3 hit_warn
"hit_warn" : 0.3,                    #valore di uno warn dato da un team hit
}









banned = -5                     #Valore di notoriety per essere bannato
#SERVIZIO
GameServerDown = 20             #Secondi di attesa prima di ritentare, quando RedCap trova il gameserver down

##VARIE
Website_ON = True               #(OBBLIGATORIO!) True se esiste un website di appoggio, se no  False
NomeArchivi = "Archivi"         #cartella per archiviazione vecchi log
joinmessage = "^4-= Welcome on ^2BW ^4UrT Server =-"

##SERVER remoto (parte facoltativa da specificare se Website_ON = True)
url = 'www.bravewarriors.eu'    #URL FTP
login = 'xxxxxx'             #FTP login
password = 'xxxxxx'          #FTP password
directory = '/httpdocs/serverstats' #directory FTP utilizzata da RedCap
tabella = "skilltable.htm"      #tabella skills
dialoghi = "dialoghi.htm"       #file dialoghi

## CRON e TEMPI
WeekControl = 1                 #giorno della settimana per operazioni settimanali (0=Domenica, 1=lunedi, ecc.)
MonthControl = 28               #giorno del mese (da 1 a 28) per operazioni mensili (cancellazione record mensile)

##KILLSTREAK
reg_only = True                 #If True only trusted player can save a record

##MESSAGGI
#messaggi
SP01 = " ^2To be registered as trusted player ^1always use the same nick"
SP02 = " ^2RedCap ^1faq ^2at : ^4www.bravewarriors.eu/index.php/redcap"
SP03 = " ^2Rule#1: ^1get under Lebbra's skin leads to a rapid kick"
SP04 = " ^2Only ^1trusted players ^2can play with With Passport ON, registration is needed."
SP05 = " ^1RedCap " + versione + " ^2bot is testing here. Weird behaviour may happen!"
SP06 = " ^2Go spect if you are ^1afk"
SP07 = " ^2Server BW 1: ^1195.43.185.235^3:27961"
SP08 = " ^2Join BW on IRC: ^6#bravewarriors"
SP09 = " ^2Camping not allowed if you are the ^1last one ^2of your team"
SP10 = " ^2Skill level classification at: ^6www.bravewarriors.eu"
SP11 = " ^2Server rules at: ^4www.bravewarriors.eu/index.php/regolamento-server"
SP12 = " ^2flood = kick"
SP13 = " ^2Write ^1!tm ^2to balance the teams"
SP14 = " ^2Write ^1!isk ^2to know your instant skill level"
SP15 = " ^2Write ^1!!sk ^2to know your global skill level"
SP16 = " ^2Write ^1!ora ^2to know the time"
SP17 = " ^2Write ^1!top ^2to know the records"
SP18 = " ^2To be registered as trusted player ^1put your clan tag"

        