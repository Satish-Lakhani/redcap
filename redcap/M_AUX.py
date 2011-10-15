#! /usr/bin/python
# -*- coding: utf-8 -*-

import time                     #Funzioni tempo

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
        if time.time() - self.ultima_volta > self.periodo:
            self.ultima_volta = time.time() #reinizializzo il timer
            self.ticks += 1
            return True
        else:
            return False

    def reset(self):
        self.ultima_volta = time.time() #memorizzo l'ultima esecuzione
        self.ticks = 0                  #cicli del cronometro
