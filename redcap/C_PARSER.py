#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import re

class Parser:
    """Classe utilizzata per parsare i file di log di urt."""

    def __init__(self,pathfile):
        """Inizializzo l'oggetto LogParser"""
        self.NomeFile = pathfile #percorso del file da parsare
        self.dim = os.path.getsize(pathfile)            #dimensione del file da parsare 
        self.nuovotesto = []                            #quanto di nuovo letto nel log
        self.outputs = []                               #dati di ritorno

    def novita(self):
        """Ritorna la parte nuova del log"""
        if os.path.getsize(self.NomeFile) > self.dim:        #se il log e' cresciuto
            logfile = open(self.NomeFile, "r")
            logfile.seek(self.dim)                      #mi posiziono all'inizio delle nuove informazioni
            self.nuovotesto = logfile.read()            #leggo le novita
            logfile.close()
            self.dim = os.path.getsize(self.NomeFile)        #aggiorno la dimensione log
            self.parsa()                                #se trovo novita faccio il parsing delle novita'
            return True                                 #e ritorno True
        elif os.path.getsize(self.NomeFile) < self.dim:      #se il log e' diminuito (cancellazione o simili)
            self.dim = os.path.getsize(self.NomeFilepathfile)
        return False                                    #se non trovo novita' ritorno falso

    def parsa(self):
        """Analizzo la parte di log contenuta in "self.nuovotesto" estraendone le informazioni utili"""
        if not self.nuovotesto:                                                                             #gestisco il caso di chiamata a vuoto (non dovrebbe mai succedere)
            return "testovuoto"                                                                             #TODO gestire questa variabile
        self.outputs = []                                                                                   #inizializzo i dati
        self.nuovotesto = self.nuovotesto.split("\n")                                                       #separo le linee del log
        for x in self.nuovotesto:                                                                           #analizzo ciascuna nuova linea del log
            if x.find("Hit: ")!= -1:                                                                        #Trovo tutti gli HITS
                self.outputs.append((re.search(r'Hit: (?P<hit>\d+ \d+ \d+ \d+):', x).group('hit').split(), "Hits"))
            elif x.find("say:") != -1 or x.find("sayteam:") != -1:                                          # *** FRASI DETTE IN CHAT
                res = re.search( r"say(team)?: (?P<id>\d+) .*?: (?P<testo>.*)",x)
                id = res.group("id")
                testo = res.group("testo")
                frase = [id, testo]
                if re.search(r"^!\w",testo):                                                                #Recupero i COMANDI
                    self.outputs.append((frase, "Comandi"))
                else:
                    self.outputs.append((frase, "Says"))
            elif x.find("Radio: ") !=  -1:                                                                  # *** RADIO MESSAGES
                res = re.search( r"Radio: (?P<id>\d+) - (?P<msg>\d+ - \d+)",x)
                id = res.group("id")
                msg = res.group("msg")
                mess = [id, msg]
                self.outputs.append((mess, "Radio"))
            elif x.find("ClientUserinfo:") !=  -1:                                                          # *** CLIENTUSERINFO
                res = re.search(r"ClientUserinfo: (?P<id>\d+)", x)                                          #Recupero l'ID
                res1 = re.search(r"\\ip\\(?P<ip>\d*\.\d*\.\d*\.\d*)",x)                                     #Recupero l'IP
                if not res1:
                    IP = "123.123.123.123"		                                                            #Necessario per i server con bot
                else:
                    IP = res1.group("ip")
                res2 = re.search(r"cl_guid\\(?P<guid>.*?)(\\|$)",x)                                         #Recupero la GUID
                if not res2:                                                                                #se non ha la guid gli assegno una fittizia e verra' kikkato
                    GUID = "NOGUID"
                else:
                    GUID = res2.group("guid")
                res3 = re.search(r"gear\\(?P<gear>.*?)(\\|$)",x)                                            #Recupero le armi
                if not res3:
                    gear = ""
                else:
                    gear = res3.group("gear")
                frase = [res.group("id"), IP, GUID, gear]
                self.outputs.append((frase, "ClientUserinfo"))
            elif x.find("ClientUserinfoChanged:") !=  -1:                                                   # *** CLIENTUSERINFOCHANGED
                res = re.search(r"ClientUserinfoChanged: (?P<id>\d+)", x)
                res1 = re.search(r"n\\(?P<nome>.*?)\\t\\(?P<team>\d)", x)
                frase = [res.group("id"), res1.group("nome"), res1.group("team")]
                self.outputs.append((frase, "ClientUserinfoChanged"))
            elif x.find("ClientConnect:") !=  -1:                                                           # *** CLIENTCONNECT
                res = re.search(r"ClientConnect: (?P<id>\d+)", x)
                self.outputs.append((res.group("id"), "ClientConnect"))
            elif x.find("ClientDisconnect:") !=  -1:                                                        # *** CLIENTDISCONNECT
                res = re.search(r"ClientDisconnect: (?P<id>\d+)", x)
                self.outputs.append((res.group("id"), "ClientDisconnect"))
            elif x.find("Kill: ")!= -1:                                                                     # *** KILL
                self.outputs.append((re.search(r'Kill: (?P<kill>\d+ \d+ \d+):', x).group('kill').split(), "Kills"))
            elif x.find("InitRound:")!= -1:                                                                 # *** INITROUND
                self.outputs.append((x, "InitRound"))
            elif x.find("SurvivorWinner:")!= -1:                                                            # *** ENDROUND
                self.outputs.append((x, "EndRound"))
            elif x.find("InitGame:")!= -1:                                                                  # *** INITMAP
                res = re.search(r"g_matchmode\\(?P<matchmode>\d)\\g_gametype\\(?P<gametype>\d)\\sv_maxclients\\(?P<maxclients>\d+)\\.*\\mapname\\(?P<mapname>.*?)\\", x)
                frase = [res.group("matchmode"), res.group("gametype"), res.group("maxclients"), res.group("mapname")]
                self.outputs.append((frase, "InitGame"))
            elif x.find("Exit:")!= -1:                                                                      # *** ENDMAP
                self.outputs.append((x, "EndMap"))

    def q3ut4_check(self, path, info, cycle):
        """recupero informazioni dalla directory q3ut4"""
        lista = os.listdir(path)
        for element in lista:
            if element.rfind(".cfg") != -1:
                info["cfg"].append(element)                                                         #recupero i cfg
            elif element.rfind(".pk3") != -1:
                mapname = element.rstrip(".pk3")
                info["map"].append(mapname)                                                         #recupero le mappe disponibili
        tag = False
        for line in open(path +"/" + cycle, "r"):
            if  "{" in line:
                tag = True
                continue
            elif "}" in line:
                tag = False
                continue
            elif not tag and len(line) > 2:                                                         #un nome mappa non puo essere < 2
                info["mapcycle"].append(line)                                                       #parso il cyclemap
        

