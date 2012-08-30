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
        "cleanalias":"""SELECT GUID,ALIAS FROM DATI""",                         #recupera tutti i player ed i loro alias
        "cleanedalias":"""UPDATE DATI SET ALIAS=? WHERE GUID=?""",              #sostituisce i vecchi alias con quelli puliti
        "cleanIP":"""SELECT GUID,OLD_IP FROM LOC""",                            #recupera tutti i player ed i loro IP
        "cleanedIP":"""UPDATE LOC SET OLD_IP=? WHERE GUID=?""",                 #sostituisce i vecchi IP con quelli puliti
        "cleanoldplayers":"""SELECT GUID FROM DATI WHERE ? - LASTCONN > ? AND TEMPBAN < ?""",   #elimina i player con guid inutilizzate
        "delplayer":"""DELETE FROM %s WHERE GUID = '%s'""",                     #elimina una guid da una tabella
        "findplayer":"""SELECT rowid,NICK,ALIAS FROM DATI WHERE ALIAS LIKE ?""", #trova i player con il nick richiesto
        "getallorderedbyguid":"""SELECT * FROM %s ORDER BY GUID DESC""",        #recupera una tabella ordinata per guid
        "getIPs": """SELECT OLD_IP FROM LOC WHERE rowid = ?""",                 #recupero gli IP di un player
        "getrecords":"""SELECT * FROM REC""",                                   #recupera la tabella records
        "newdati" : """INSERT INTO DATI VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",    #inserisce un player  (guid, DBnick, skill, rounds, lastconnect, level, tempban, notoriety, firstconn, streak, alias, varie)
        "newdeath": """INSERT INTO DEATH (GUID) VALUES (?)""",
        "newhit": """INSERT INTO HIT (GUID) VALUES (?)""",
        "newkill": """INSERT INTO KILL (GUID) VALUES (?)""",
        "newloc": """INSERT INTO LOC (GUID, IP, OLD_IP) VALUES (?, ?, ?)""",
        "salvadati":"""UPDATE DATI SET NICK=?, SKILL=?, ROUND=?, LASTCONN=?, LEVEL=?, TEMPBAN=?, REPUTATION=?, STREAK=?, ALIAS=?, VARIE=? WHERE GUID=?""",
        "salvahit":"""UPDATE HIT SET HEAD=HEAD+?, TORSO=TORSO+?, ARMS=ARMS+?, LEGS=LEGS+? WHERE GUID=?""",
        "salvakills":"""UPDATE KILL SET KNIFE=KNIFE+?, BERETTA=BERETTA+?, DE=DE+?, SPAS=SPAS+?, UMP45=UMP45+?, MP5K=MP5K+?, LR300=LR300 +?, G36=G36+?, PSG1=PSG1+?, HK69=HK69+?, BLED=BLED+?, KICKED=KICKED+?, NADE=NADE+?, SR8=SR8+?, AK103=AK103+?, NEGEV=NEGEV+?, M4=M4+?, GOOMBA=GOOMBA+?, DEATHS=DEATHS+? WHERE GUID=?""",
        "salvaloc":"""UPDATE LOC SET IP=?, PROVIDER=?, LOCATION=?, OLD_IP=? WHERE GUID=?""",
        "saverecords":"""UPDATE REC SET TIME=?, VAL=?, OWNER=? WHERE TIPO=? """,
        "tempban":"""UPDATE DATI SET TEMPBAN=? WHERE GUID=?""",
        "unban":"""UPDATE DATI SET TEMPBAN=0.0 WHERE rowid=?""",
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



