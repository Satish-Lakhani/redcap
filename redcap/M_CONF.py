#! /usr/bin/python
# -*- coding: utf-8 -*-

versione = "1.00 Alpha"         #RedCap Version. !!! PLEASE ADD "-MOD by YOURNAME" TO THE VERSION NUMBER IF YOU MODIFY SOMETHING OF THE SCRIPT OUTSIDE OF THIS CONFIGURATION FILE. !!!

'''########## (OBBLIGATORIO!) = CONFIGURAZIONE OBBLIGATORIA ###########'''

##SERVER
ServerPars = {
"AliasDuration": 90,                #tempo di memorizzazione in giorni di un vecchio alias prima che sia cancellato per inutilizzo
"AntiReconInterval" : 200,         #Tempo di antireconnect in sec (se 0  = Disattivato)
"AutoBalance" : 2,                 #0=disattivato 1=attivato 2=automatico
"Baseconf" : "server.cfg",        #nome della configurazione standard del gameserver
"FloodControl" : True,             #Flood control abilitato = True, disabilitato = false (TODO comando per abilitare disabilitare da chat?)
"goodNick":r"[a-zA-Z]",          #Regex minima che il nick deve soddisfare.
"Logfolder": "logs",                #cartella di registrazione dei log
"MaxFlood" : 6,                     #massimo numero di say in un tempo fissato (CRON1)
"MaxNickChanges" : 3,              #massimi change nick in un tempo fissato (CRON1)
"MinNotoriety": -999,            #valore notoriety per giocare nel server. La notoriety di un nuovo player � 0
"minNick":3,                            #Lunghezza minima nick
"Passport" : False,                #True=passport attivo gia' all'avvio, False=passport inattivo all'avvio.
"UrtPath" : "../../../q3ut4",      #path relativo della cartella q3ut4 di urt
}

#NOTA LOGS: i log sono reperibili nella cartella logs e sono i seguenti
crashlog = "crash.log"       #eventi di crash del server
socketlog = "socket.log"  #comandi non inviati
commandlog = "command.log"  #comandi bot inviati dai giocatori
commandlogMinLevel = 0      #livello minimo del comando affinche sia registrato nel log (settare piu alto del pi� alto dei livelli di comando se non si vuole registrare nulla)

#REDCAP
botname = "^8RC| "                 #prefisso degli output del Redcap (lasciare vuoto "" se non si vuole prefisso) #TODO non utilizzato
RC_lang = "ITA"                    #Localizzazione linguaggio ITA #TODO (ENG FRA e altre, da fare)
maxSlap = 10                        #massimo numero di slap che posso dare ad un player
max_warns = 5                   #massimo numero di warning dopo di che vieni kikkato  (si azzerano al reconnect). Uno slap o un nuke dati da Redcap comportano automaticamente un warning.

## SOCKET
SocketPars = {
"ServerRcon" : "xxxxxx",          #(OBBLIGATORIO!) rconpassword (inserire la password di rcon fra le virgolette)
"ServerIP" : "217.199.3.245",      #(OBBLIGATORIO!) IP del gameserver
"ServerPort" : 27960,              #(OBBLIGATORIO!) Porta del gameserver
"ServerTimeout" : 1,               #(OBBLIGATORIO!) Secondi di attesa risposta server a comando rcon (NON CAMBIARE!)
"Tsleep" : 0.8,                     #(OBBLIGATORIO!) Tempo di attesa tra due comandi rcon successivi  (NON CAMBIARE!)
"ServerLog":  ServerPars["Logfolder"] + "/" + socketlog   #nome del log dove il socket registra i suoi errori.
}
## PARSER
NomeFileLog = "AUXILIARY/prova.log" #prova.log" # DEBUG"../games.log"    #(OBBLIGATORIO!) Percorso relativo del file di log da controllare

##TEMPI
TempoCiclo = 0.5                #Frequenza in sec del controllo del log
CRON1 = 15                      #Frequenza in sec del cron1 (cronometro veloce)

##DATABASE
NomeDB = "Rc_DB.sqlite"          #nome DB (se si cambia rinominare anche il file corrispondente)
#minRounds = 60                  #numero minimo di round giocati per apparire nelle statistiche
#maxAbsence = 25                 # giorni di assenza prima di essere cancellati dal server

##VOTO
voteTime = 30,                        #tempo di abilitazione del voto
voteType =536870986            #modalita' di voto temporanea (see http://www.urbanterror.info/docs/texts/123/#2.2)
unvoteType = 0                       #modalita' di voto permanente (0 esclude qualsiasi tipo di voto)
timeBetweenVote = 3            #tempo in minuti che deve intercorrere tra due voti

##CYCLEMAP
Tcyclemap = 12                  #tempo in minuti che deve intercorrere tra due cyclemap

##LIVELLI COMANDI:
#lev_autobalance = 2             #inserisce/disinserisce l'autobalance
#lev_balance = 0                 #bilanciare team
#lev_ban = 4                     #ban
#lev_cycle = 2                   #cyclemap
lev_force = 2                   #forceteam
#lev_info = 0                    #mostra server IP e versione redcap
#lev_isk =0                      #mostra instant skill del player
lev_kick = 2                    #kick
lev_level = 4                   #assegno level
lev_mute = 1                    #mute
#lev_nick = 2                    #trova il nick ufficiale
lev_nuke = 0                    #nuke #DEBUG
lev_ora = 0                     #dice l'ora
#lev_passport = 3                #attiva/disattiva il passport
lev_password = 3            #setta una password
#lev_pause = 3                   #mette il bot in pausa
#lev_RCrestart = 4               #restart
#lev_reg = 3                     #registrazione in DB ed assegnazione passport
#lev_skill = 0                   #mostra skill del player
lev_slap = 2                    #slap
#lev_status = 3                  #status
#lev_tmpban = 2                  #ban temporaneo
#lev_top = 0                     #mostra i top record
#lev_unreg = 3                   #toglie il passport
lev_callvote = 0                    #chiama voto
#lev_war = 1                     #configurazione per war

##NOTORIETY
# valore di notoriety aggiunto a quella del player in caso di alcuni avvenimenti. Quando la notoriety scende al di sotto di ServerPars["MinNotoriety"] il player non pu� piu accedere al server.
Notoriety = {
"guidchange" : -5,          #penalizzazione punti per cambio guid al volo (probabile cheat)
"badguid" : -20,            #penalizzazione punti per guid non corretta (probabile cheat)
"roundXpoint": 100,       #num. di round da giocare per guadagnare un punto notoriety
"dayXpoint": 5               #giorni di anzianit� della guid per guadagnare un punto notoriety
}

##SALUTI
#Opzioni di saluto player all'entrata in game (da sommare): 0 = nessun saluto 1 = nome attuale 2 = nome di registrazione in DB 4 = skill 8 = affidabilit� 16 = ultima visita
saluti = 31

#SKILL (parametri per la formula skill)
Sk_team_impact = 0.3    #percentuale della skill calcolata in base alla teamskill avversaria (il resto e' calcolato in base alla skill dell'avversario diretto)
Sk_Kpp = 50          #numero di kill (a delta skill 0) necessarie per guadagnare un punto skill.
Sk_range = 800     #piu grande e il valore, piu alti sono i valori di skill che si possono raggiungere.
                        #Numero di player a skill 0 che un giocatore a skill 1000 deve uccidere per compensare una sola uccisione da parte di un player a skill 0:
                        #ES. range=300: kill 785; range=500: kill 55;  range=600: kill 28; range=700: kill 17; range=800: kill 12; range=900: kill 9; range=1000: kill 7; range=3000: kill 2;





#PLAYER

banned = -5                     #Valore di notoriety per essere bannato
#CONSOLE SPAMS
RecordSpam = True               #Se True, Redcap spamma periodicamente i record, se False non spamma
CustomSpam = True               #Se True, Redcap spamma periodicamente le frasi scritte in RT_SPAM.txt, se False non spamma
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
DailyControl = 6                #ora alla quale vengono eseguite le operazioni periodiche giornaliere
WeekControl = 1                 #giorno della settimana per operazioni settimanali (0=Domenica, 1=lunedi, ecc.)
MonthControl = 28               #giorno del mese (da 1 a 28) per operazioni mensili (cancellazione record mensile)
max_Tban = 48                   #durata massima del ban temporaneo in ore


TempoControllo2 = 100           #Frequenza in sec per: messaggi di spam e disabilitazione automatica passport e war mode a server vuoto.


##KILLSTREAK
reg_only = True                 #If True only trusted player can save a record
minKS = 4                       #minima stream affinche' il bot segnali la killstreak
maxKS = 25                      #Lunghezza del dizionario in RCwords.py
#messaggi di killstreak
KS04 = '^2 4 noobs? you can do better!'
KS05 = '^2 is warming up: ^15 ^2kills!'
KS06 = '^2 killed 6 enemies in a row'
KS07 = '^2 7 scalps? not bad!'
KS08 = '^2 are you camping? ^1(8 kills!)'
KS09 = '^2 9 kills. You are on fire!!'
KS10 = '^2 1^40 ^3K^4I^5L^6L^8S^9!! '
KS11 = '^2 11 kills! You sure ain\'t a noob...'
KS12 = '^2 12 kills...aimbot or wallhack?'
KS13 = '^2 13 kills? ^1You are a PRO!'
KS14 = '^2 14 kills? kills? someone kill him!'
KS15 = '^2 15 kills? are you Kabal?!'
KS16 = '^2 16 kills? 16 kills? one more and i\'ll kick you!!'
KS17 = '^2 17 kills? I was kidding!'
KS18 = '^2 18 ^1You are more pro than before!'
KS19 = '^2 19 kills! Are you playing against fools!?!?'
KS20 = '^2 20 ^3KILLS^4!^5!^6!'
KS21 = '^1 21 kills...i can\'t believe it! :-('
KS22 = '^1 22 kills? 1337!'
KS23 = '^2 23 kill? ^4ok guys, John Rambo is here'
KS24 = '^2 24 corpses... ^4bigger massacre than waco!'
KS25 = '^2Kill counter is OVER! ^3U^4N^6B^1E^7L^8I^9E^0V^1A^3B^5L^2E^6!'


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

'''########## NON CAMBIARE I PARAMETRI QUI SOTTO ###########'''
"""Do NOT MODIFY below this line or RedCap could hung up."""









        