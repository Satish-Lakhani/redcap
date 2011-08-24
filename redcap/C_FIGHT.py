#! /usr/bin/python
# -*- coding: utf-8 -*-

#TODO decidere se e' meglio classe o modulo

# 0:40 Kill: 0 4 30: Nagisa killed PicchioFumatore by UT_MOD_AK103

class Kills:
    """Classe ausiliaria per analizzare le kill"""
    def __init__(self):
        pass

    def kill(self, frase, GSRV):                          #del tipo ['0', '0', '10'] (K,V,M)
        """analizza una singola kill (il changeteam ed il kick sono gia' esclusi)"""
        if frase[2] in ['12', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '25', '28', '30', '35', '38', '40' ]:      #KILL NORMALI 
            #TODO: verifica tkill
            #TODO: calcolo variazione skill
            #TODO: calcolo variazione kstreak (eventuale spam)
            #TODO: verifica eventuali record (eventuale spam)
            #TODO: chiamo la funzione death per gestire il morto
            pass
        elif frase[2] in ['6', '9', '31']:                                                                                                                #INCIDENTE
            pass
        elif frase[2] == '7':                                                                                                                              #SUICIDIO
            pass
        elif frase[2] == '24':                                                                                                                            #KICKED
            pass
        elif frase[2] == '34':                                                                                                                            #NUKED
            pass

    def is_tkill(self, K, V):
        """verifica se è stato fatto un tkill"""
        if K.team == V.team:
            pass    #TODO decidere cosa fare in caso di TK



class Hits:
    """Classe ausiliaria per analizzare le hit"""
    def __init__(self):
        pass
    

