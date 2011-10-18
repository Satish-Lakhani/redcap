#! /usr/bin/python
# -*- coding: utf-8 -*-

import time                     #Funzioni tempo
'''
def web_rank():
    """crea la classifica in formato tabella a partire dal DB e la invia ad un altro server"""
    DB.connetti()
    dati1 = DB.esegui(DB.query["getallorderedbyguid"]%"DATI").fetchall()
    dati2 = DB.esegui(DB.query["getallorderedbyguid"]%"HIT").fetchall()
    dati3 = DB.esegui(DB.query["getallorderedbyguid"]%"LOC").fetchall()
    dati4 = DB.esegui(DB.query["getallorderedbyguid"]%"KILL").fetchall()
    i=0
    cicli = len(dati1)
    tmp = []
    while i < cicli:
        tmp.append(dati1[i] + dati2[i][1:len(dati2[i])] + dati3[i][1:len(dati3[i])] + dati4[i][1:len(dati4[i])])
        i+=1
    DBdump = sorted(tmp, key=lambda dato: dato[2], reverse=True)    #record ordinati per skill decrescente
    # 0: GUID
    # 1: Nick
    # 2: Skill
    # 3: Round
    # 4: Lastconnection
    # 5: Level
    # 6: Tempban
    # 7: Reputation
    # 8: Firstconnect
    # 9: streak
    # 10: alias
    # 11: varie
    # 12: head
    # 13: torso
    # 14: arms
    # 15: legs
    # 16: body
    # 17: IP
    # 18: provider
    # 19: location
    # 20: oldguids
    # 21-39: kills

    #creo la tabella
    def cella(c_stile, contenuto):
        return "<td style='%s'>%s</td>"%(c_stile, contenuto)
    
    def tablerow(r_stile, riga):
        return "<tr style='%s'>%s</tr>"%(r_stile, riga)

   # "<a href='#'>testo <span>Testo tooltip</span></a>"
    
    table = "<table class=\"sortable\"><tbody><tr><th>POS.</th><th>NICK</th><th>ROUNDS</th><th>SKILL</th><th>STREAK</th><th>ULTIMA VISITA</th></tr>%s</tbody></table>"%corpo

    res = DB.esegui(DB.statement["classifica"]) #eseguo il select da DB
    row = res.fetchall()
    i=0
    for riga in row:
        i+=1
        last = time.strftime("%y/%m/%d %H:%M",time.localtime(riga[5])) #trasformo il lastseen in data
        riga0 = str(riga[0]).replace("<", "&lt;") #strippo l'html
        riga0 = riga0.replace(">", "&gt;") #strippo l'html
        if riga[2]<0:
            colore ="<td style='color:#f00'>"
        else:
            colore ="<td style='color:#0f0'>"
        table += "<tr><td>" + str(i) + "</td><td>" + riga0 + "</td><td>" + str(riga[1]) + "</td>"  + colore + str(round(riga[2]*100, 1))  + "</td><td>" + str(riga[3]) + "</td><td>" + last + "</td></tr>" #RIGHE
    table += "</tbody></table>"
    #salvo in locale
    htmlfile = open(RCconf.NomeArchivi + "/" + RCconf.tabella, "w")
    htmlfile.write(table)
    htmlfile.close()
    #trasferisco in remoto
    if RCconf.Website_ON:
        trasferisci(RCconf.NomeArchivi + "/" + RCconf.tabella, RCconf.tabella)
'''

def cr_riavvia(autorestart):
    """restarto RedCap ed eventualmente il server"""
    import os
    import sys
    import M_RC
    if autorestart:
        M_RC.scrivilog("RIAVVIO PROGRAMMATO REDCAP e GAMESERVER", M_CONF.crashlog)
        os.system("./S_full_restart.sh")
        sys.exit()
    else:
        M_RC.scrivilog("RIAVVIO PROGRAMMATO REDCAP", M_CONF.crashlog)
        sys.exit()

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
