#! /usr/bin/python
# -*- coding: utf-8 -*-

#TODO fare controllo armi ammesse per team
#TODO fare l'automute che muta il player non appena entra (serve campo nel DB)
#TODO comando !bonus n per gestire la notoriety
#TODO aggiungere gestione del ritorno dei comandi (chi, riusciti, non riusciti)


import C_PARSER       #Classe che rappresenta il parser
import M_AUX             #Modulo funzioni ausiliarie
import M_CONF          #Modulo configurazioni programma
import M_RC               #Modulo che gestisce le azioni del Redcap

#res = M_AUX.avvio()                                                             #attività di avvio del gameserver
sys.excepthook = M_AUX.crashlog                                       #abilito il log dei crash
#TODO gserver_is_active() #Controllo che il gameserver sia attivo, se no IL REDCAP SI FERMA QUI IN LOOP finche' il server non torna attivo.


PARSER = C_PARSER.Parser(M_CONF.NomeFileLog)          #Istanzio il Parser
CRON1 = M_AUX.Cronometro(M_CONF.CRON1)                    #Istanzio il cron1

def redcap_main():
    while 1:
        M_AUX.sleep(M_CONF.TempoCiclo)             #wait for a cycletime
        if PARSER.novita():                                           #log check
            for frase in PARSER.outputs:                          #frase[0]=contenuto, frase[1]=tipo di frase (assigned from PARSER)
                if frase[1] == "InitGame":
                    M_RC.initGame(frase[0])                        #aggiorno le cvars del server CVARS = [matchmode, gametype,maxclients,mapname]
                    testo = " ^7U " + str(M_RC.GSRV.TeamMembers[0]) + "^1R " + str(M_RC.GSRV.TeamMembers[1]) + "^4B " + str(M_RC.GSRV.TeamMembers[2]) + "^2S " + str(M_RC.GSRV.TeamMembers[3]) #DEBUG
                    print testo #DEBUG
                    M_RC.say(testo, 1) #DEBUG
                    pass    #TODO (altre cose da fare a initgame)
                    continue
                elif frase[1].find("Client") !=  -1:            #gestisco le frasi Client indirizzando alla funzione appropriata
                    exec("M_RC.%s(frase[0])"%frase[1].lower())
                    continue
                if M_RC.GSRV.Startup_end:                           #ALTRI EVENTI da processare solo a startup finito
                    if frase[1] == "Hits":
                        pass    #TODO
                        continue
                    elif frase[1] == "Says":                         #SAY frase[0] (0,0=id, 0,1=testo)
                        M_RC.says(frase[0])
                        continue
                    elif frase[1] == "Kills":
                        pass    #TODO
                        continue
                    elif frase[1] == "Comandi":                   #COMANDI frase[0] (0,0=id, 0,1=comando)
                        M_RC.comandi(frase[0])                    #passo richiedente e parametri alla funzione comandi del modulo M_RC
                        continue
                    elif frase[1] == "InitRound":
                        pass    #TODO
                        continue
                    elif frase[1] == "EndRound":
                        pass    #TODO
                        continue
                    elif frase[1] == "EndMap":                    
                        pass    #TODO
                        continue
        print "FINITO!" #DEBUG
        if CRON1.is_time():                         #eseguo operazioni a cron1
            M_RC.cr_floodcontrol()              #controllo se qualcuno ha floodato
            M_RC.cr_full()                             #controllo se il server è pieno
            M_RC.cr_nickrotation()              #controllo se qualcuno fa nickrotation
            M_RC.cr_unvote()                       #controllo se c'è un voto speciale attivo
            M_RC.cr_warning()                     #controllo se qualcuno ha troppi warning

#AVVIO LA PROCEDURA PRINCIPALE
redcap_main()
