#! /usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time

class Sock:
    """gestisce l'invio dei comandi al gameserver e le rispettive risposte"""

    def __init__(self,parametri):
        """inizializzo il lanciatore di comandi utilizzando i parametri di config"""
        self.rcon = parametri["ServerRcon"]                                                     #Rcon del gamenserver
        self.server = parametri["ServerIP"]                                                     #IP del gameserver
        self.port = parametri["ServerPort"]                                                     #porta del gameserver
        self.sleeptime = parametri["Tsleep"]                                                    #tempo di attesa tra 2 comandi
        self.log = parametri["ServerLog"]                                                                        #path del log di RedCap
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                               #creo il socket
        self.s.settimeout(parametri["ServerTimeout"])                                           #timeout del socket
        self.Header = chr(255) + chr(255) + chr(255) + chr(255) + "rcon " + self.rcon + " "     #creo l'header del comando rcon
        self.sv_resp = ""                                                                       #Risposta del gameserver
        try:
            self.s.connect((self.server, self.port))                                                #connetto il socket
            self.connected = True
        except:
            self.connected = False

    def cmd(self,comando):
        """gestisce il lancio comandi al server attraverso la routine protetta __invia"""
        pass    #DEBUG
        """self.sv_resp = ""
        self.sv_resp = self.__invia(comando)
        time.sleep(self.sleeptime)
        if self.sv_resp == False:                       #se il server non risponde provo a riconnettere il socket e ritento una volta il comando.
            self.s.connect((self.server, self.port))     
            self.sv_resp = self.__invia(comando)
            time.sleep(self.sleeptime / 2)
            if self.sv_resp == False:                   #se non riesco ad eseguire ritorno stringa vuota piu' il flag False
                self.__cmd_error(comando)
                return [comando, False]
        else:                                           #se riesco ad eseguire ritorno la risposta piu' il flag True
            return [self.sv_resp, True]"""

    def __invia (self,comando): #metodo protetto
        """invia un comando rcon al gameserver da eseguirsi immediatamente"""
        comando = self.Header + comando
        try:
            self.s.send(comando)
            return self.s.recv(4096)
        except:
            return False

    def __cmd_error(self,cmd): #TODO vedere se portare fuori da socket
        """scrive il comando non inviato nel file di log di RedCap"""
        cmd = (time.strftime("%d.%b %H.%M.%S", time.localtime()) + " NOT SENT: " + cmd + "\r\n")
        f = open(self.log, "a")
        f.write(cmd)
        f.close()



   