#! /usr/bin/python
# -*- coding: utf-8 -*-

import socket
import time
import M_CONF

class Sock:
    """gestisce l'invio dei comandi al gameserver e le rispettive risposte"""

    def __init__(self):
        """inizializzo il lanciatore di comandi utilizzando i parametri di config"""
        self.rcon = M_CONF.Sck_ServerRcon                                                               #Rcon del gamenserver
        self.server = M_CONF.Sck_ServerIP                                                               #IP del gameserver
        self.port = M_CONF.Sck_ServerPort                                                               #porta del gameserver
        self.sleeptime = M_CONF.Sck_Tsleep                                                              #tempo di attesa tra 2 comandi
        self.log = M_CONF.Sck_ServerLog                                                                 #path del log di RedCap
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                                       #creo il socket
        self.s.settimeout(M_CONF.Sck_ServerTimeout)                                                     #timeout del socket
        self.Header = chr(255) + chr(255) + chr(255) + chr(255) + "rcon " + self.rcon + " "             #creo l'header del comando rcon
        self.sv_resp = ""                                                                               #Risposta del gameserver
        try:
            self.s.connect((self.server, self.port))                                                    #connetto il socket
            self.connected = True
        except:
            self.connected = False

    def cmd(self,comando):
        """gestisce il lancio comandi al server attraverso la routine protetta __invia"""
        self.sv_resp = ""
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
            return [self.sv_resp, True]

    def __invia (self,comando): #metodo protetto
        """invia un comando rcon al gameserver da eseguirsi immediatamente"""
        comando = self.Header + comando
        try:
            self.s.send(comando)
            return self.s.recv(4096)
        except:
            return False

    def __cmd_error(self,cmd):
        """scrive il comando non inviato nel file di log di RedCap"""
        import M_RC
        if M_RC.GSRV.Attivo:
            M_RC.scrivilog("NOT SENT: %s"%cmd, M_CONF.socketlog)




   