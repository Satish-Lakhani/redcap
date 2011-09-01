#! /usr/bin/python
# -*- coding: utf-8 -*-

#Modulo  ausiliario per analizzare le kill e le hit"""
from M_CONF import Warning
from M_CONF import Skill

normalKills = ['12', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '25', '28', '30', '35', '38', '40' ]
accident = ['6', '9', '31']
suicide = '7'
kick = '24'
nuked = '34'

def kill( frase, GSRV):                          #del tipo ['0', '0', '10'] (K,V,M)
    """analizza una singola kill (il changeteam e' gia' escluso)"""
    if frase[2] in normalKills :                                                        #KILL NORMALI
        tk = is_tkill(GSRV.PT[frase[0]], GSRV.PT[frase[1]])                     #TEAMKILL
        if tk:
            return "tk"
        GSRV.skill_variation(frase[0],frase[1])                                           #funzione che calcola ed assegna la variazione skill ai due players
        #TODO: calcolo variazione kstreak (eventuale spam)
        #TODO: verifica eventuali record (eventuale spam)
        pass
    elif frase[2] in accident :                                                        #INCIDENTE
        pass
    elif frase[2] == suicide:                                                           #SUICIDIO
        pass
    elif frase[2] == kick:                                                               #KICKED
        pass
    elif frase[2] == nuked:                                                            #NUKED
        pass

def is_tkill(K, V):
    """verifica se e stato fatto un tkill e procede di conseguenza"""
    if K.team == V.team:
        K.warning += Warning["tk_warn"]                         #aumento il warning
        K.skill -= Skill["Sk_penalty"] /  Skill["Sk_Kpp"]     #penalizzo la skill
        return True

 

