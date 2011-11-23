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
        "cercadati":"""SELECT * FROM DATI WHERE GUID = ?""",                    #cerca nella tab DATI in base alla GUID
        "cercaloc":"""SELECT * FROM LOC WHERE GUID = ?""",                      #cerca nella tab LOC in base alla GUID
        "getallorderedbyguid": """SELECT * FROM %s ORDER BY GUID DESC""", #recupera una tabella ordinata per guid
        "getrecords":"SELECT * FROM REC""",                                     #recupera la tabella records
        "newdati" : """INSERT INTO DATI VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",    #inserisce un player  (guid, DBnick, skill, rounds, lastconnect, level, tempban, notoriety, firstconn, streak, alias, varie)
        "newdeath": """INSERT INTO DEATH (GUID) VALUES (?)""",
        "newhit": """INSERT INTO HIT (GUID) VALUES (?)""",
        "newkill": """INSERT INTO KILL (GUID) VALUES (?)""",
        "newloc": """INSERT INTO LOC (GUID, IP, OLD_IP) VALUES (?, ?, ?)""",
        "salvadati":"""UPDATE DATI SET NICK=?, SKILL=?, ROUND=?, LASTCONN=?, LEVEL=?, TEMPBAN=?, REPUTATION=?, STREAK=?, ALIAS=?, VARIE=? WHERE GUID=?""",
        "salvahit":"""UPDATE HIT SET HEAD=HEAD+?, TORSO=TORSO+?, ARMS=ARMS+?, LEGS=LEGS+?, BODY=BODY+? WHERE GUID=?""",
        "salvakills":"""UPDATE KILL SET KNIFE=KNIFE+?, BERETTA=BERETTA+?, DE=DE+?, SPAS=SPAS+?, UMP45=UMP45+?, MP5K=MP5K+?, LR300=LR300 +?, G36=G36+?, PSG1=PSG1+?, HK69=HK69+?, BLED=BLED+?, KICKED=KICKED+?, NADE=NADE+?, SR8=SR8+?, AK103=AK103+?, NEGEV=NEGEV+?, M4=M4+?, GOOMBA=GOOMBA+?, DEATHS=DEATHS+? WHERE GUID=?""",
        "salvaloc":"""UPDATE LOC SET IP=?, PROVIDER=?, LOCATION=?, OLD_IP=? WHERE GUID=?""",
        "saverecords":"""UPDATE REC SET TIME=?, VAL=?, OWNER=? WHERE TIPO=? """,
        "tempban":"""UPDATE DATI SET TEMPBAN=? WHERE GUID=?""",
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

    def esegui(self,statement,params=""):
        """esegue un comando SQL"""
        self.cur.execute(statement,params)
        return self.cur

    def salva(self):
        """fa il commit di quanto in sospeso"""
        self.conn.commit()
    
    '''statement = {
    "aggiornaskill":"""UPDATE TBskill SET TOTSKILL = TOTSKILL+?,ROUND = ROUND+1 WHERE GUID = ?""", #aggiorna la skill nel DB
    "aggiornanick1":"""SELECT TBgiocatori.GUID,TBgiocatori.NICK FROM TBgiocatori""", #aggiorna i nick in TBskill in base a TBgiocatori 1 parte
    "aggiornanick2":"""UPDATE  TBskill SET NICK=? WHERE GUID =?""", #aggiorna i nick in TBskill in base a TBgiocatori 2 parte
    "ban":"""UPDATE TBgiocatori SET BANNED = 5 WHERE GUID = ?""",     #banna una GUID
    "cercaskill" : """SELECT ROUND,SKILL,STREAK FROM TBskill WHERE GUID = ?""",           #cerca in base a una GUID
    "classifica":"""SELECT TBskill.NICK, ROUND, SKILL, STREAK, BANNED, LASTSEEN FROM TBskill, TBgiocatori WHERE TBskill.GUID=TBgiocatori.GUID AND ROUND>60 AND BANNED = 1 ORDER BY SKILL DESC""", #crea la classifica
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
    "tmpban" : """UPDATE TBgiocatori SET TMPBAN = ? WHERE GUID = ?""",  #banna una GUID temporaneamente
    "trovazeroround":"""SELECT TBgiocatori.GUID FROM TBskill, TBgiocatori WHERE TBskill.GUID=TBgiocatori.GUID AND TBskill.ROUND < 2 AND TBgiocatori.BANNED < 5""" #trova i player che non hanno giocato nemmeno due round completi.
    }
    '''


