#! /usr/bin/python
# -*- coding: utf-8 -*-

import time                     #Funzioni tempo

'''def avvio():
    #controllo esistenza log
    try:
        f = open("logs/crash.log", "a")
    except:'''

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
