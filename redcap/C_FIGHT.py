#! /usr/bin/python
# -*- coding: utf-8 -*-

import math

#TODO decidere se e' meglio classe o modulo

class Kills:
    """Classe ausiliaria per analizzare le kill"""
    def __init__(self):
        self.normalKills = ['12', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '25', '28', '30', '35', '38', '40' ]
        self.accident = ['6', '9', '31']
        self.suicide = '7'
        self.kick = '24'
        self.nuked = '34'

    def kill(self, frase, GSRV):                          #del tipo ['0', '0', '10'] (K,V,M)
        """analizza una singola kill (il changeteam e' gia' escluso)"""
        if frase[2] in self.normalKills :                                                        #KILL NORMALI
            if self.is_tkill(GSRV.PT[frase[0]], GSRV.PT[frase[1]]):                      #TEAMKILL
                return
            GSRV.skill_variation(frase[0],frase[1])                                           #funzione che calcola ed assegna la variazione skill ai due players
            #TODO: calcolo variazione kstreak (eventuale spam)
            #TODO: verifica eventuali record (eventuale spam)
            pass
        elif frase[2] in self.accident :                                                          #INCIDENTE
            pass
        elif frase[2] == self.suicide:                                                           #SUICIDIO
            pass
        elif frase[2] == self.kick:                                                               #KICKED
            pass
        elif frase[2] == self.nuked:                                                            #NUKED
            pass

    def is_tkill(self, K, V):
        """verifica se e stato fatto un tkill e procede di conseguenza"""
        if K.team == V.team:
            pass    #TODO decidere cosa fare in caso di TK



class Hits:
    """Classe ausiliaria per analizzare le hit"""
    def __init__(self):
        pass
    

