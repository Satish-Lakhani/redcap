#! /usr/bin/python
# -*- coding: utf-8 -*-

#TODO fare controllo armi ammesse per team
#TODO fare anche ban per nick
#TODO evitare che un crash durante cw cancelli la config war
#TODO fare comando shuffle
#TODO fare comando join
#TODO fare comando admin che mostra gli admin in game e/o la adminlist
#TODO eliminazione automatica password a server vuoto non va (ma va con !unwar) (fatto da verificare)
#TODO verificare che località sia updatata ogni volta con nuovo IP
#TODO aggiustare classifica html (non c'è più body hit) (fatto, da verificare)
#TODO comando help che mostra i comandi utilizzabili e separarlo da !info
#TODO vedere come mai da ancora messaggio record a record=0 (fatto da provare)
#TODO utilizzare g_blueteamlist and g_redteamlist
#TODO caricare la config basewar leggendola da un file py, perchè se no l'utente deve spostarla a mano in q3ut4
#TODO skill variation attiva solo con min players

import sys
import C_PARSER                                                                             #Classe che rappresenta il parser
import M_AUX                                                                                #Modulo funzioni ausiliarie
import M_CONF                                                                               #Modulo configurazioni programma
import M_RC                                                                                 #Modulo che gestisce le azioni del Redcap

def crashlog(t, v, tra):
    """gestisce i crash del programma, scrivendo l'errore nel file di log"""
    import traceback
    evento = "\r\n REDCAP CRASH:: "
    for stringa in traceback.format_tb(tra):
        evento += str(stringa)
    for stringa in traceback.format_exception_only(sys.last_type, sys.last_value):
        evento += str(stringa)
    M_RC.scrivilog(evento, M_CONF.crashlog)
    sys.exit()

sys.excepthook = crashlog                                                                   #Abilito il log dei crash

PARSER = C_PARSER.Parser(M_CONF.NomeFileLog)                                                #Istanzio il Parser
CRON1 = M_AUX.Cronometro(M_CONF.CRON1)                                                      #Istanzio il cron1
CRON2 = M_AUX.Cronometro(M_CONF.CRON2)                                                      #Istanzio il cron2

def init_jobs():
    """attivita' da fare all'avvio di redcap"""
    M_RC.say("^2Starting RedCap...", 2)
    lista = M_RC.ini_clientlist()                                                           #recupero i client gia presenti sul server
    M_RC.ini_clientadd(lista)                                                               #li aggiungo
    M_RC.ini_recordlist()                                                                   #recupero i record dal server
    M_RC.ini_spamlist()                                                                     #carico la spamlist
    if M_CONF.Website_ON:                                                                   #Se esiste un website di appoggio aggiorno la classifica, la trasferisco al server remoto e salvo il risultato dell'operazione nel log
        M_RC.say("^4Webrank updating...", 2)
        res = M_AUX.web_rank()
        if res == False:
            M_RC.scrivilog("WEBRANK TRANSFER FAILED", M_CONF.crashlog)
    M_RC.say("^4Q3ut4 parsing...", 2)
    q3ut4_parse()
    M_RC.say("^2Main routine started. Waiting for players identification...", 2)
    M_RC.ini_addcfg(M_CONF.SV_Basewar)                                                      #scrivo la basewar cfg in q3ut4
    redcap_main()                                                                           #LANCIO LA PROCEDURA PRINCIPALE

def q3ut4_parse():
    """parsa la directory q3ut4"""
    M_RC.GSRV.Q3ut4["map"] = M_AUX.StandardMaps                                             #carico solo mappe di base
    M_RC.GSRV.Q3ut4["cfg"] = []
    PARSER.q3ut4_check(M_CONF.SV_UrtPath, M_RC.GSRV.Q3ut4, M_RC.GSRV.MapCycle)              #recupero mappe e cfg.

def redcap_main():
    """

    """
    no_news = 0                                                                             #sensore di inattività serve
    while 1:
        M_RC.sleep(M_CONF.TempoCiclo)                                                       #wait for a cycletime
        no_news += M_CONF.TempoCiclo                                                        #nessuna news dal log
        if PARSER.novita():                                                                 #log check
            no_news = 0                                                                     #se ho parsato qualcosa azzero il sensore
            for frase in PARSER.outputs:                                                    #frase[0]=contenuto, frase[1]=tipo di frase (assigned from PARSER)
                if frase[1] == "InitGame":
                    M_RC.initGame(frase[0])                                                 #aggiorno le cvars del server CVARS = [matchmode, gametype,maxclients,mapname]
                    continue
                elif frase[1].find("Client") !=  -1:                                        #gestisco le frasi Client indirizzando alla funzione appropriata (i comandi li parso anche in fase di startup)
                    exec("M_RC.%s(frase[0])"%frase[1].lower())
                    continue
                elif frase[1] == "Comandi":                                                 #COMANDI frase[0] (0,0=id, 0,1=comando)
                    M_RC.comandi(frase[0])                                                  #passo richiedente e parametri alla funzione comandi del modulo M_RC
                    continue
                elif frase[1] == "InitRound":
                    M_RC.initRound(frase[0])
                    continue
                if M_RC.GSRV.Server_mode > 2:                                               #ALTRI EVENTI da processare solo a startup finito e non in war (0 = fase avvio 2 = warmode  3 = silentmode 5 = normale)
                    if frase[1] == "Hits":
                        M_RC.hits(frase[0])                                                 #del tipo (['1', '0', '3', '5'], 'Hits') Vittima, Killer, Zona, Arma
                        continue
                    elif frase[1] == "Says":                                                #SAY frase[0] (0,0=id, 0,1=testo)
                        M_RC.says(frase[0])
                        continue
                    elif frase[1] == "Kills":                                               #del tipo (['0', '0', '10'], 'Kills')
                        M_RC.kills(frase[0])
                        continue
                    elif frase[1] == "EndRound":
                        M_RC.endRound(frase[0])
                        continue
                    elif frase[1] == "EndMap":                    
                        M_RC.endMap(frase[0])
                        continue
        if CRON1.is_time():                                                                             #ESEGUO OPERAZIONI A CRON1
            if M_RC.GSRV.Server_mode > 2:                                                               #controlli fatti solo in modalita' normale o silent.
                M_RC.cr_tbkicked()                                                                      #da fare sempre per primo
                M_RC.cr_floodcontrol()                                                                  #controllo se qualcuno ha floodato
                M_RC.cr_nickrotation()                                                                  #controllo se qualcuno fa nickrotation
                M_RC.cr_unvote()                                                                        #controllo se c'e' un voto speciale attivo
                M_RC.cr_warning()                                                                       #controllo se qualcuno ha troppi warning
                M_RC.cr_notorietycheck()                                                                #controllo notoriety bassa da fare per ultimo
            M_RC.cr_full()                                                                              #controllo se il server e' pieno o vuoto (questo controllo va fatto sempre)
            if int(CRON1.ticks % (M_CONF.Spamtime // M_CONF.CRON1)) == 0:                               #divisione modulo per intervallo di spam
                M_RC.cr_spam()                                                                          #spammo
            if CRON1.ticks == 240:                                                                      #E' passata 1 ora circa
                q3ut4_parse()                                                                           #aggiorno maplist e configs (non si sa mai...)
                CRON1.reset()
        if CRON2.is_time():                                                                             #ESEGUO OPERAZIONI A CRON2
            if int(CRON2.ticks % ((M_CONF.w_webranktime*3600) // M_CONF.CRON2)) == 0:                   #divisione modulo per intervallo di aggiornamento classifica
                if M_CONF.Website_ON:                                                                   #Se esiste un website di appoggio aggiorno la classifica, la trasferisco al server remoto e salvo il risultato dell'operazione nel log
                    M_AUX.web_rank()
                    M_AUX.web_FTPtransfer("HTML" + "/" + M_CONF.w_tabella, M_CONF.w_tabella)
            if CRON2.get_time("Ora") == M_CONF.Control_Daily:                                           #all'ora prefissata eseguo operazioni giornaliere (pulizia DB, riavvio server, etc)
                M_RC.cr_recordErase()                                                                   #Pulisco i record se del giorno (settimana, mese) prima.
                M_AUX.automaintenance()                                                                 #automanutenzione e riavvio
                # -= Non puo' leggere istruzioni oltre qui (riavvio server e redcap!) =-
        if no_news > M_CONF.GameServerDown:                                                             #il gameserver non da notizie da circa 60 sec
            M_AUX.check_coherence()                                                                     #DEBUG per vedere se a volte il server è considerato vuoto e non lo è o viceversa
            no_news = 0

#AVVIO IL REDCAP
init_jobs()
