#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys                      #Necessaria per intercettare l'output di crash
import time                     #Funzioni tempo
import M_CONF

'''def avvio():
    #controllo esistenza log
    try:
        f = open("logs/crash.log", "a")
    except:'''

def crashlog(t, v, tra):
    """gestisce i crash del programma, scrivendo l'errore nel file di log"""
    import traceback
    evento = "\r\n REDCAP CRASH:: "
    for stringa in traceback.format_tb(tra):
        evento = evento + str(stringa)
    for stringa in traceback.format_exception_only(sys.last_type, sys.last_value):
        evento = evento + str(stringa)
    scriviLog(evento, M_CONF.ServerPars["Logfolder"] + "/" + M_CONF.crashlog)
    sys.exit()

def scrivilog(evento, nomelog):          #TODO separare i log per argomenti e fare log di debug
    """scrive il messaggio "evento" nel file di log di RedCap"""
    evento = (time.strftime("%d.%b %H.%M.%S", time.localtime()) + ": " + evento + "\r\n")
    f = open(nomelog, "a")
    f.write(evento)
    f.close()

def sleep(tempo):
    time.sleep(tempo)

class Cronometro:
    """classe per controlli a tempo"""
    def __init__(self, periodo):
        self.ultima_volta = time.time() #memorizzo l'ultima esecuzione
        self.periodo = periodo

    def is_time(self):
        if time.time() - self.ultima_volta > self.periodo:
            self.ultima_volta = time.time() #reinizializzo il timer
            return True
        else:
            return False