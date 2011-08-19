#! /usr/bin/python 
# -*- coding: utf-8 -*-

import sqlite3

class Database:
    """Fa da tramite col database sqlite"""
    def __init__(self, nome):
        """Inizializzo le proprieta"""
        self.nome = nome
        self.conn = None
        self.cur = None
        self.query = {
        "cercadati":"""SELECT * FROM DATI WHERE GUID = ?""",           #cerca nella tab DATI in base alla GUID
        "cercaloc":"""SELECT * FROM LOC WHERE GUID = ?""",           #cerca nella tab LOC in base alla GUID
        #inserisce un player  (guid, DBnick, skill, rounds, lastconnect, level, tempban, notoriety, firstconn, streak,alias,)
        "newdati" : """INSERT INTO DATI VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        "newdeath": """INSERT INTO DEATH (GUID) VALUES (?)""",
        "newhit": """INSERT INTO HIT (GUID) VALUES (?)""",
        "newkill": """INSERT INTO KILL (GUID) VALUES (?)""",
        "newloc": """INSERT INTO LOC (GUID) VALUES (?)""",
        }

    def connetti (self): 
        """connette al DB path e crea un cursore"""
        self.conn = sqlite3.connect(self.nome)
        if self.conn:
            self.cur = self.conn.cursor()
        else:
            raise Exception, "Connessione al DB fallita"

    def disconnetti(self):
        """disconnette il DB path"""
        self.conn.close()

    def salva(self):
        """fa il commit di quanto in sospeso"""
        self.conn.commit()

    def esegui(self,statement,params=""):
        """esegue un comando SQL"""
        self.cur.execute(statement,params)
        return self.cur
    
    '''statement = {
    "aggiornaskill":"""UPDATE TBskill SET TOTSKILL = TOTSKILL+?,ROUND = ROUND+1 WHERE GUID = ?""", #aggiorna la skill nel DB
    "aggiornanick1":"""SELECT TBgiocatori.GUID,TBgiocatori.NICK FROM TBgiocatori""", #aggiorna i nick in TBskill in base a TBgiocatori 1 parte
    "aggiornanick2":"""UPDATE  TBskill SET NICK=? WHERE GUID =?""", #aggiorna i nick in TBskill in base a TBgiocatori 2 parte
    "ban":"""UPDATE TBgiocatori SET BANNED = 5 WHERE GUID = ?""",     #banna una GUID
    "cercaskill" : """SELECT ROUND,SKILL,STREAK FROM TBskill WHERE GUID = ?""",           #cerca in base a una GUID
    "classifica":"""SELECT TBskill.NICK, ROUND, SKILL, STREAK, BANNED, LASTSEEN FROM TBskill, TBgiocatori WHERE TBskill.GUID=TBgiocatori.GUID AND ROUND>60 AND BANNED = 1 ORDER BY SKILL DESC""", #crea la classifica
    "deregistra":"""UPDATE TBgiocatori SET BANNED = 0,NICK = ? WHERE GUID = ?""" ,#aggiorna il nick nel DB e gli toglie il passport
    "eliminaguid":"""DELETE FROM TBgiocatori WHERE GUID = ? AND BANNED < 5""", #elimina una GUID se non bannata
    "eliminavecchi":"""DELETE FROM TBgiocatori WHERE LASTSEEN < ? AND BANNED < 5""",#elimina dal DB le guid non piu utilizzate da parecchio tempo se non bannate
    "endban" : """UPDATE TBgiocatori SET TMPBAN = 0 WHERE GUID = ?""",  #termina un ban temporaneo
    "getlevel":"""UPDATE TBgiocatori SET LEVEL = ? WHERE GUID = ?""", #aggiorna la data di ultima visita
    "inserisci" : """INSERT INTO TBgiocatori VALUES (?,?,?,?,?,?)""",   #inserisce un player  (GUID,NICK,BANNED,LASTSEEN,LEVEL,TMPBAN)
    "joina1" : """SELECT * FROM TBgiocatori WHERE NICK = ? ORDER BY LASTSEEN DESC""", #cerco se c'è un'altro player con lo stesso nick
    "joina2":"""UPDATE TBgiocatori SET GUID = ?, LASTSEEN = ? WHERE GUID = ?""", #cambio la guid e lastseen in TBgiocatori
    "joina3":"""UPDATE TBskill SET GUID = ? WHERE GUID = ?""", #cambio la guid in TBskill
    "kstreak" : """SELECT * FROM TBrecords""",   #recupera la tabella records
    "kstreakupd" : """UPDATE TBrecords SET NICK = ?, RECORD = ?, DATA = ? WHERE TIPO = ?""", #aggiorno la tabella records
    "kstreakupdpers" : """UPDATE TBskill SET STREAK = ? WHERE GUID = ?""", #aggiorno la kstreak personale
    "lastseen":"""UPDATE TBgiocatori SET LASTSEEN = ? WHERE GUID = ?""", #aggiorna la data di ultima visita
    "nick" : """SELECT NICK, BANNED FROM TBgiocatori WHERE GUID = ?""", #data una guid recupera il nick e la registrazione
    "registra":"""UPDATE TBgiocatori SET BANNED = 1, NICK = ? WHERE GUID = ?""" ,#aggiorna il nick nel DB e gli assegna il passport
    "tmpban" : """UPDATE TBgiocatori SET TMPBAN = ? WHERE GUID = ?""",  #banna una GUID temporaneamente
    "trovazeroround":"""SELECT TBgiocatori.GUID FROM TBskill, TBgiocatori WHERE TBskill.GUID=TBgiocatori.GUID AND TBskill.ROUND < 2 AND TBgiocatori.BANNED < 5""" #trova i player che non hanno giocato nemmeno due round completi.
    }
    '''
