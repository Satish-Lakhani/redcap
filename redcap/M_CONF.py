#! /usr/bin/python
# -*- coding: utf-8 -*-

### =======================================================================  ###
### THESE PARAMETERS ***MUST*** BE CONFIGURED OR REDCAP WILL NOT RUN PROPERLY!!!   ###
### =======================================================================  ###

NomeFileLog = "../games.log" #2011_Sep_01_log.log" #" # DEBUG"../games.log" #(OBBLIGATORIO!) Percorso relativo del file di log da controllare
AdminGuids = ["****************************"] #guid automaticamente abilitata al max liv di autorizzazione
SV_Baseconf = "server.cfg"  #nome della configurazione standard del gameserver
SV_UrtPath = "../../../q3ut4"    #path relativo della cartella q3ut4 di urt #DEBUG
SV_MapCycle =  "********"    #nome del file di cyclemap
Sck_ServerRcon = "********"   #(OBBLIGATORIO!) rconpassword (inserire la password di rcon fra le virgolette)
Sck_ServerIP =  "***.***.***.***"      #(OBBLIGATORIO!) IP del gameserver
Sck_ServerPort = 27960 #(OBBLIGATORIO!) Porta del gameserver
27960
### =============================================================================================  ###
### THESE PARAMETERS **MUST** BE CONFIGURED IF  *** Website_ON = True *** OR REDCAP WILL NOT RUN PROPERLY!!!   ###
### =============================================================================================  ###

Website_ON = False #(OBBLIGATORIO!) True se esiste un website di appoggio, se no False
w_url = 'www.yoursite.com'      #URL FTP
w_login = '*******' #FTP login
w_password = '********' #FTP password
w_ftp_directory = '/httpdocs/serverstats', #directory utilizzata da RedCap (formato FTP)
w_directory = '/serverstats' #directory utilizzata da RedCap (formato web)

### ==================================================================  ###
### THESE PARAMETERS *CAN* BE CONFIGURED IN ORDER TO CUSTOMIZE YOUR REDCAP   ###
### ==================================================================  ###
#PLAYER
KickForSpace = True #se true kikka uno spect (se c'e') quando il server e' pieno
maxSlap = 10 #massimo numero di slap che posso dare ad un player

#RECORD
MinPlayers = 4 #numero minimo di players per considerare valido un record
MinNotoriety = 0 #notoriety minima per segnare un record

#CONSOLE SPAMS
RecordSpam = True #Se True, Redcap spamma periodicamente i record, se False non spamma
CustomSpam = True #Se True, Redcap spamma periodicamente le frasi scritte in RT_SPAM.txt, se False non spamma
Spamtime = 140 #Tempo in secondi tra due spam

#REDCAP
botname = "^8RC| " #prefisso degli output del Redcap (lasciare vuoto "" se non si vuole prefisso) #TODO non utilizzato
RC_lang = "ITA" #Localizzazione linguaggio ITA #TODO (ENG FRA e altre, da fare)
gameserver_autorestart = 2 #0: non riavvia 1: riavvio giornaliero 2: riavvia tutte le volte che e' vuoto

##SERVER
SV_AliasDuration = 90,      #tempo di memorizzazione in giorni di un vecchio alias prima che sia cancellato per inutilizzo
SV_AntiReconInterval = 0    #Tempo di antireconnect in sec (se 0 = Disattivato)
SV_BalanceMode = 2          #0=disattivato 1=attivato 2=automatico
SV_FloodControl = True,     #Flood control abilitato = True, disabilitato = false (TODO comando per abilitare disabilitare da chat?)
SV_goodNick = r"[a-zA-Z]"   #Regex minima che il nick deve soddisfare.
SV_MaxFlood = 6    #massimo numero di say in un tempo fissato (CRON1)
SV_MaxNickChanges = 3    #massimi change nick in un tempo fissato (CRON1)
SV_minNick = 3   #Lunghezza minima nick
SV_ShowHeadshots = True  #Se True mostra gli headshot

#LIVELLI COMANDI (Max lev = 100):
lev_alias = 1 #mostra gli alias di un player
lev_admin = 1 #livello a partire dal quale un player e' considerato admin (riceve piu' info in risposta a certi comandi, ed il fatto che sia presente abilita o disabilita alcune funzionalita del bot)
lev_balancemode = 2 #inserisce/disinserisce l'autobalance
lev_balance = 0 #bilanciare team
lev_ban = 3 #ban
lev_callvote = 1 #chiama voto
lev_cycle = 2 #cyclemap
lev_dbnick = 3 #assegna il nick corrente come nick in DB
lev_esegui = 4 #esegue un qualsiasi comando rcon
lev_force = 2 #forceteam
lev_info = 0 #mostra server IP e versione redcap
lev_kick = 1 #kick
lev_level = 4 #assegno level
lev_map = 1 #cambio mappa
lev_maplist = 1 #lista mappe
lev_mute = 1 #mute
lev_muteall = 2 #mute all
lev_notoriety = 2 #cambia livello notoriety minima per giocare sul server
lev_nuke = 2 #nuke #DEBUG
lev_ora = 0 #dice l'ora
lev_password = 1 #setta una password
lev_RCrestart = 4 #restart
lev_skill = 0 #mostra skill del player
lev_slap = 1 #slap
lev_spam = 2 #inserisce/disinserisce frasi spam
lev_spamlist = 0 #lista le frasi spam
lev_status = 0 #status (informazioni varie sul player)
lev_tmpban = 1 #ban temporaneo
lev_top = 0 #mostra i top record
lev_trust = 3 #aggiunge/leva notoriety ad un player
lev_war = 1 #configurazione per war
lev_unwar = 1 #eliminare configurazione war

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
saluti = 1 + 2048 #informazioni di saluto
status = 1 + 32 + 128 + 1024 + 2048 #informazioni date ai non admin
status_adm = 1 + 8 + 16 + 32 + 64 + 128 + 256 + 512 + 2048 + 1024 #info date agli admin

#SKILL
Sk_penalty = 4   #Teamkill penalty: it represents the number of additional kill you should gain in order to nullify the penalty.
Sk_Ks_min = 5    #(not used)
Sk_Ks_not = 0    #Kill streaks made by players with lower notoriety than this are not spammed.
Sk_Ks_show = 5   #Kill streaks shorter than this are not spammed by RedCap.
Sk_Ks_showbig = 9 #Kill streaks longer than this are spammed by RedCap in bigtext.

##VOTO
voteTime = 30 #tempo di abilitazione del voto
voteType =536870986 #modalita' di voto temporanea (see http://www.urbanterror.info/docs/texts/123/#2.2)
unvoteType = 0 #modalita' di voto permanente (0 esclude qualsiasi tipo di voto)
timeBetweenVote = 3 #tempo in minuti che deve intercorrere tra due voti

##WARNING
W_max_warns = 5.0   #Warning level to be kicked. (warning can be assigned by RedCap or Admins)
W_adm_warn = 1.0    #Value of a warning assigned by a Admin (TODO: Not used yet)
W_tk_warn = 1.0        #Value of a warning caused by a teamkill
W_hit_warn = 0.3       #Value of a warning caused by a teamhit

##MISCELLANEOUS
commandlogMinLevel = 2 #livello minimo del comando affinche sia registrato nel log (settare piu alto del piu alto dei livelli di comando se non si vuole registrare nulla)
Control_Daily = 6 #ora alla quale vengono eseguite le operazioni periodiche giornaliere
Nt_MinNot_toplay = 0.55 #Min. notoriety  to play in the gameserver. New player's notoriety is 0
w_minRounds = 60 #round to play before a player is included in webstats



#maxAbsence = 25 # giorni di assenza prima di essere cancellati dal server

### ================================================================================================================  ###
### THESE PARAMETERS ***MUST NOT*** BE CHANGED UNLESS YOU EXACTLY KNOW WHAT ARE YOU DOING OR REDCAP WILL NOT RUN PROPERLY!!!   ###
### ================================================================================================================  ###

versione = "1.00 Beta" #RedCap Version. !!! PLEASE ADD "-MOD by YOURNAME" TO THE VERSION NUMBER IF YOU MODIFY SOMETHING OF THE SCRIPT OUTSIDE OF THIS CONFIGURATION FILE. !!!

##AUXILIARY FILES and LOGS
badguid = "badguid.log" #Bad guids record file
crashlog = "crash.log" #RedCap activity and crashes logfile
commandlog = "command.log" #RedCap commands record file (commandlogMinLevel value specify which command should be recorded into the file)
NomeArchivi = "Archivi" #Gamelogs and database backup folder
NomeDB = "Rc_DB.sqlite" #name of DB file
socketlog = "socket.log" #Not sent command logfile
SpamFile = "spam.txt"   #Custom spams here
SV_Basewar = "basewar.cfg"  #Basic CW config that RedCap loads if nothing else is specified
SV_Logfolder = "logs"   #Log folder
w_tabella = "skilltable.htm" #Ranking table (html format)
w_dialoghi = "dialoghi.htm" #Chat log table (html format)

##NOTORIETY:  If player notoriety is lower than Nt_MinNot_toplay, the player is immediately kicked from gameserver.
Nt_badguid = -20    #Notoriety penalty for bad formatted guid
Nt_dayXpoint = 5    #Guid age (days) giving 1 notoriety point
Nt_floodpenalty = -0.2  #Notoriety penalty for flooding
Nt_guidchange = -50 #Notoriety penalty for guid change in game
Nt_roundXpoint = 200    #N. of round to be played giving 1 notoriety point
Nt_warnpenalty = -1 #Notoriety penalty for a kick from RedCap

##SKILL parameters
#EXAMPLE: appoximative score that a 1000 skill player should obtain to keep his skill unchanged:
#Sk_range=300: score: 785-1;
#Sk_range=500: score 55-1;
#Sk_range=600: score 28-1;
#Sk_range=700: score 17-1;
#Sk_range=800: score 12-1;
#Sk_range=900: score 9-1;
#Sk_range=1000: score 7-1;
#Sk_range=3000: score 2-1;

Sk_team_impact = 0.3     #Part of skill variation based on opponent team mean skill. (Remaining is based on direct opponent's skill)
Sk_Kpp = 5   #N. of times you should kill an equivalent skilled opponent to gain 1 skill point.
Sk_range = 800   #Theoric skill ceil value.

## SOCKET
Sck_ServerTimeout = 1   #Waiting time for an answer from gameserver (sec)
Sck_Tsleep = 0.8     #Delay between two consecutive rcon commands (sec)
Sck_ServerLog =  SV_Logfolder + "/" + socketlog #Path to socketlog

##TEMPI
CRON1 = 15 #Frequenza in sec del cron1 (cronometro veloce)
CRON2 = 3600 #Frequenza in sec del cron1 (cronometro lento)
Tcyclemap = 12 #tempo in minuti che deve intercorrere tra due cyclemap
TempoCiclo = 0.5 #Frequenza in sec del controllo del log
Ttempban = 96 #durata massima tempban

#SERVIZIO
GameServerDown = 20 #Secondi di attesa prima di ritentare, quando RedCap trova il gameserver down

