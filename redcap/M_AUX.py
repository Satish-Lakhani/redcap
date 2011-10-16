#! /usr/bin/python
# -*- coding: utf-8 -*-

import time                     #Funzioni tempo

def ini_gen():  #Tempi di controllo del server
    """inizializzazioni generali"""
    Ticks = {
    "Sec": int(time.strftime("%S", time.localtime())),
    "Min": int(time.strftime("%M", time.localtime())),
    "Ora": int(time.strftime("%H", time.localtime())),
    "Day": int(time.strftime("%j", time.localtime())),
    "Week": int(time.strftime("%U", time.localtime())),
    "Month": int(time.strftime("%m", time.localtime())),
    }
    return Ticks

def cr_riavvia():
    """restarto RedCap ed eventualmente il server"""
    import os
    import sys
    import M_RC
    if M_CONF.gameserver_autorestart:
        M_RC.scrivilog("RIAVVIO PROGRAMMATO REDCAP e GAMESERVER", M_CONF.crashlog)
        os.system("./S_full_restart.sh")
        sys.exit()
    else:
        M_RC.scrivilog("RIAVVIO PROGRAMMATO REDCAP", M_CONF.crashlog)
        sys.exit()

class Cronometro:
    """classe per controlli a tempo"""
    def __init__(self, periodo):
        self.ultima_volta = time.time() #memorizzo l'ultima esecuzione
        self.periodo = periodo
        self.ticks = 0                  #cicli del cronometro

    def is_time(self):
        """scatto del cronometro"""
        if time.time() - self.ultima_volta > self.periodo:
            self.ultima_volta = time.time() #reinizializzo il timer
            self.ticks += 1
            return True
        else:
            return False

    def get_time(self, mode):
        "ritorna l'ora"
        modo = {
        "Sec": "%S",    #0-61
        "Min": "%M",    #0-59
        "Ora": "%H",    #0-24
        "Day": "%j",    #0-366
        "Week": "%U",   #0-53
        "Month": "%m",  #0-12
        }
        return int(time.strftime(modo[mode], time.localtime()))

    def reset(self):
        self.ultima_volta = time.time() #memorizzo l'ultima esecuzione
        self.ticks = 0                  #cicli del cronometro
