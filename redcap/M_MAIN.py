#! /usr/bin/python
# -*- coding: utf-8 -*-

#TODO fare controllo armi ammesse per team
#TODO comando !bonus n per gestire la notoriety
#TODO aggiungere gestione del ritorno dei comandi (chi, riusciti, non riusciti)
#TODO inserire controllo eliminazione vecchi alias
#TODO fare anche ban per nick
#TODO e' effettivamente necessario recuperare gli alias alla connection o si fa su richiesta?
#TODO eliminare gli alias piu vecchi di n giorni
#TODO alla connessione di un player mandargli un tell con le sue info
#TODO note per warmode: no kick, warn o richiami per badguid o badnick, tkill o thit o censura (registrare variazione skill?), non registrare ne spammare record. no spam vari.
#TODO prevedere silentmode.
#TODO fare comando hit che dice le hit eseguite in percentuale
#TODO verificare tutto quello che c'e' da bloccare quando si e' in modalita'� war.
#TODO vedere come assegnare il livello
#TODO vedere perchè da sempre comando non riconosciuto
#TODO se crashlog non esiste deve venire creato
#TODO verificare come mai status non viene detto tutto (limite lunghezza frase?)

import sys
import C_PARSER         #Classe che rappresenta il parser
import M_AUX            #Modulo funzioni ausiliarie
import M_CONF           #Modulo configurazioni programma
import M_RC             #Modulo che gestisce le azioni del Redcap

def crashlog(t, v, tra):
    """gestisce i crash del programma, scrivendo l'errore nel file di log"""
    import traceback
    evento = "\r\n REDCAP CRASH:: "
    for stringa in traceback.format_tb(tra):
        evento = evento + str(stringa)
    for stringa in traceback.format_exception_only(sys.last_type, sys.last_value):
        evento = evento + str(stringa)
    M_RC.scrivilog(evento, M_CONF.crashlog)
    sys.exit()

sys.excepthook = crashlog                                       #abilito il log dei crash

PARSER = C_PARSER.Parser(M_CONF.NomeFileLog)    #Istanzio il Parser
CRON1 = M_AUX.Cronometro(M_CONF.CRON1)          #Istanzio il cron1
CRON2 = M_AUX.Cronometro(M_CONF.CRON2)          #Istanzio il cron2

def init_jobs():
    """attivita' da fare all'avvio di redcap"""
    q3ut4_parse()
    #TODO gserver_is_active() #Controllo che il gameserver sia attivo, se no IL REDCAP SI FERMA QUI IN LOOP finche' il server non torna attivo.
    redcap_main()                               #LANCIO LA PROCEDURA PRINCIPALE

def q3ut4_parse():
    """parsa la directory q3ut4"""
    M_RC.GSRV.Q3ut4["map"] = M_CONF.StandardMaps                       #carico solo mappe di base
    M_RC.GSRV.Q3ut4["cfg"] = []
    PARSER.q3ut4_check(M_CONF.ServerPars["UrtPath"], M_RC.GSRV.Q3ut4)   #recupero mappe e cfg.

def redcap_main():
    while 1:
        M_RC.sleep(M_CONF.TempoCiclo)             #wait for a cycletime
        if PARSER.novita():                                           #log check
            for frase in PARSER.outputs:                          #frase[0]=contenuto, frase[1]=tipo di frase (assigned from PARSER)
                if frase[1] == "InitGame":
                    M_RC.initGame(frase[0])                        #aggiorno le cvars del server CVARS = [matchmode, gametype,maxclients,mapname]
                    continue
                elif frase[1].find("Client") !=  -1:            #gestisco le frasi Client indirizzando alla funzione appropriata (i comandi li parso anche in fase di startup)
                    exec("M_RC.%s(frase[0])"%frase[1].lower())
                    continue
                elif frase[1] == "Comandi":                   #COMANDI frase[0] (0,0=id, 0,1=comando)
                    M_RC.comandi(frase[0])                    #passo richiedente e parametri alla funzione comandi del modulo M_RC
                    continue
                if M_RC.GSRV.Server_mode == 1:             #ALTRI EVENTI da processare solo a startup finito e non in war
                    if frase[1] == "Hits":
                        M_RC.hits(frase[0])                         #del tipo (['1', '0', '3', '5'], 'Hits') Vittima, Killer, Zona, Arma
                        continue
                    elif frase[1] == "Says":                         #SAY frase[0] (0,0=id, 0,1=testo)
                        M_RC.says(frase[0])
                        continue
                    elif frase[1] == "Kills":                           #del tipo (['0', '0', '10'], 'Kills')
                        M_RC.kills(frase[0])
                        continue
                    elif frase[1] == "InitRound":
                        M_RC.initRound(frase[0])    
                        continue
                    elif frase[1] == "EndRound":
                        M_RC.endRound(frase[0])
                        continue
                    elif frase[1] == "EndMap":                    
                        M_RC.endMap(frase[0])
                        continue
        if CRON1.is_time():                     #eseguo operazioni a cron1
            if M_RC.GSRV.Server_mode == 1:
                M_RC.cr_floodcontrol()              #controllo se qualcuno ha floodato
                M_RC.cr_full()                      #controllo se il server e' pieno o vuoto
                M_RC.cr_nickrotation()              #controllo se qualcuno fa nickrotation
                M_RC.cr_unvote()                    #controllo se c'e' un voto speciale attivo
                M_RC.cr_warning()                   #controllo se qualcuno ha troppi warning
            if CRON1.ticks == 240:              #E' passata 1 ora circa
                q3ut4_parse()
                CRON1.reset()
        if CRON2.is_time():
            pass                                #eseguire operazioni giornaliere (pulizia DB, riavvio server, etc)

#AVVIO IL REDCAP
init_jobs()
