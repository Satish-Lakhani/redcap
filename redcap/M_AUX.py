#! /usr/bin/python
# -*- coding: utf-8 -*-

import time          #Funzioni tempo
import M_CONF
import C_DB         #Classe che rappresenta il DB

DB = C_DB.Database(M_CONF.NomeDB)

StandardMaps = [    #mappe standard incluse nello z_pack
"ut4_abbey","ut4_abbeyctf","ut4_algiers",
"ut4_ambush","ut4_austria","ut4_casa",
"ut4_crossing","ut4_dressingroom","ut4_eagle",
"ut4_elgin","ut4_firingrange","ut4_harbortown",
"ut4_kingdom","ut4_mandolin","ut4_maya",
"ut4_oildepot","ut4_paradise","ut4_prague",
"ut4_ramelle","ut4_riyadh","ut4_sanc",
"ut4_snoppis","ut4_suburbs","ut4_subway",
"ut4_swim","ut4_thingley","ut4_tombs",
"ut4_toxic","ut4_tunis","ut4_turnpike","ut4_uptown",
"ut4_company",      #Mappack 4.1.1
"ut4_docks","ut4_herring","ut4_horror","ut4_ricochet",
]


colori = {          #colori per i dialoghi
"0":"#00FF00","1":"#00FFFF","2":"#FFFF00","3":"#FFFFCC","4":"#006600","5":"#0066FF","6":"#330033","7":"#330033",
"8":"#FF6600","9":"#FF66FF","10":"#FF66FF","11":"#969696","12":"#99CC99","13":"#FFCCCC","14":"#6699FF"
}

tabs = [            #tabelle del DB con guid
"DATI", "DEATH", "HIT", "KILL", "LOC"
]

def cr_riavvia(autorestart):
    """restarto RedCap ed eventualmente il server"""
    import os
    import sys
    import M_RC
    if log_backup():    #provo a fare il backup del log
        M_RC.scrivilog("DAILY LOG AND DB BACKUP DONE.", M_CONF.crashlog)
        os.remove(M_CONF.NomeFileLog)
        M_RC.SCK.cmd("exec " + M_CONF.SV_Baseconf)                   #ricarico il config TODO vedere se sufficiente per ricreare il games.log
    if autorestart > 0:
        M_RC.scrivilog("REDCAP and GAMESERVER DAILY RESTART.", M_CONF.crashlog)
        os.system("./S_full_restart.sh")
        sys.exit()
    else:
        M_RC.scrivilog("REDCAP DAILY RESTART.", M_CONF.crashlog)
        sys.exit()

def db_clean_alias():
    """Elimino gli alias in eccedenza"""
    j2 = "  "
    DB.connetti()
    res = DB.esegui(DB.query["cleanalias"]).fetchall()
    for player in res:
        newalias = ""
        aliases = player[1].split(j2)
        aliases.sort()
        aliases.reverse()
        aliases = aliases[0:M_CONF.maxAlias]
        for alias in aliases:
            newalias += (alias + j2)
        newalias = newalias.rstrip()
        DB.esegui(DB.query["cleanedalias"],(newalias, player[0]))
    DB.salva()
    DB.disconnetti()

def db_clean_guid():
    """pulizia periodica DB"""
    DB.connetti()
    res = DB.esegui(DB.query["cleanoldplayers"], (time.time(), float(M_CONF.maxAbsence*86400), time.time())).fetchall()
    for guid in res:
        for tab in tabs:
            DB.esegui(DB.query["delplayer"] % (tab, guid[0]))  #Elimino guid che non frequentano piu' il gameserver da M_CONF.maxAbsence giorni.
    DB.salva()
    DB.disconnetti()

'''
def db_delete_player(guid, tabs):
    """cancella un player dal DB. Presuppone il DB gia connesso."""
    for tab in tabs:
        DB.esegui(DB.query["delplayer"] % (tab, guid))
'''

def log_backup():
    """Esegue funzioni di backup sul file di log. Utilizzata da cr_riavvia()"""
    import shutil
    import re
    timestamp = time.strftime("%Y_%b_%d", time.localtime())
    #leggo il log
    logfile = open(M_CONF.NomeFileLog, "r")
    contenuto = logfile.read()
    logfile.close()
    contenuto=re.sub(r"Item: .* ","",contenuto) #elimino le voci Item
    #creo il file di log in Archivi
    logfile = open(M_CONF.NomeArchivi + "/" + timestamp + ".log", "w")
    logfile.write(contenuto)
    logfile.close()
    #Copio il DB in Archivi
    shutil.copy2(M_CONF.NomeDB, M_CONF.NomeArchivi + "/" + timestamp + "_" + M_CONF.NomeDB)
    DB.connetti()
    res = DB.esegui("""VACUUM""")   #DOPO che l'ho backuppato, lo comprimo.
    DB.salva()
    DB.disconnetti()
    #Estraggo i dialoghi
    logfile = open(M_CONF.NomeFileLog, "r")
    dialoghi = logfile.read()
    logfile.close()
    dialoghi = dialoghi.replace("<", "&lt;")
    dialoghi = dialoghi.replace(">", "&gt;")
    says=re.findall(r"say: (?P<colore>\d+) (?P<nick>.*): (?P<frase>.*)", dialoghi)
    #creo il file dei dialoghi
    html = "<table class='dialoghi'>" #preparo la tabella e inserisco i dialoghi
    for say in says:
        if say[2].find("!sk") != -1 or say[2].find("!z") != -1 or say[2].find("!al") != -1:
            continue #elimino comandi inutili
        html +="<tr><td>"
        html += "<span style='color:" + colori[say[0]] + "'>" +say[1] + "</span></td><td style='color:#bbbbbb'>" + say[2]
        html +="</td></tr>\n"
    html +="</table>"
    #salvo il tutto in un file
    logfile = open(M_CONF.NomeArchivi + "/" + timestamp + "_saylog.log", "w")
    logfile.write(html)
    logfile.close()
    #crea la classifica se attivato
    if web_FTPtransfer(M_CONF.NomeArchivi + "/" + timestamp + "_saylog.log", M_CONF.w_dialoghi):
        return "CHATFILE TRANSFER OK"
    else:
        return "CHATFILE TRANSFER FAILED"
    return True

def web_rank():
    """crea la classifica in formato tabella a partire dal DB"""

    def cella(contenuto,  toltip = "",  cls = "",  st = ""):          #sottofunzione che crea le celle
        return "<td title='%s' class='%s' style='%s'>%s</td>" %(toltip, cls, st, contenuto)

    def striphtml(testo):   #strippo l'html
        testo = testo.replace("<", "&lt;")
        testo = testo.replace(">", "&gt;")
        return testo

    DB.connetti()
    dati1 = DB.esegui(DB.query["getallorderedbyguid"]%"DATI").fetchall()
    dati2 = DB.esegui(DB.query["getallorderedbyguid"]%"HIT").fetchall()
    dati3 = DB.esegui(DB.query["getallorderedbyguid"]%"LOC").fetchall()
    dati4 = DB.esegui(DB.query["getallorderedbyguid"]%"KILL").fetchall()
    i=0
    cicli = len(dati1)
    tmp = []
    while i < cicli:
        if dati1[i][3] > M_CONF.w_minRounds:
            tmp.append(dati1[i] + dati2[i][1:len(dati2[i])] + dati3[i][1:len(dati3[i])] + dati4[i][1:len(dati4[i])])
        i+=1
    Dump = sorted(tmp, key=lambda dato: dato[2], reverse=True)    #record ordinati per skill decrescente

    #DATI: #0: GUID    # 1: Nick    # 2: Skill    # 3: Round    # 4: Lastconnection    # 5: Level    # 6: Tempban    # 7: Reputation    # 8: Firstconnect    # 9: streak    # 10: alias    # 11: varie
    #HIT: #12: head    # 13: torso    # 14: arms    # 15: legs    # 16: body    #LOC: #17: IP    # 18: provider    # 19: location    # 20: oldip    #KILL: #21-38: kills #39: deaths
    lasttableupdate = str(time.strftime("%d.%b&nbsp;%H:%M",time.localtime()))
    table_ini = ""
    table_end = "</tbody></table>"              #parte finale della table
    wz_tooltip_path = "http://" +M_CONF.w_url + M_CONF.w_directory + "/"
    if M_CONF.w_fullpage:                       #richiedo una pagina html completa
        table_ini = "<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'><html><head><link href='rank.css' rel='stylesheet' type='text/css' /><script src='%s/sorttable.js'></script></head><body><div class=\"redcap\">" %M_CONF.w_script_url
        table_end += "</div></body></html>"
        wz_tooltip_path = ""
    table_ini += "<script type='text/javascript' src='%swz_tooltip.js'></script><table class=\"sortable\"><tbody>" %(wz_tooltip_path) #parte iniziale della table
    header = "<tr title=\"Last update: %s\"><th>ID</th><th>NICK</th><th>SKILL</th><th>STREAK</th><th>ROUNDS</th><th title='Headshots'>HS</th><th>LAST IP</th><th>LAST VISIT</th></tr>" %lasttableupdate #Header (SKILL, NICK, STREAK, ROUNDS, HIT, IP, LASTVISIT)
    TABLE = table_ini + header                  #contenuto della table
    i_id = 1
    for guid in Dump:                           #CREO LA RIGA ed i suoi span. RIGHE CON TOOLTIP: <a href="#" onmouseover="TagToTip('Span2')" onmouseout="UnTip()">Homepage </a>
        #*** Cella ID ***************
        ID = cella(str(i_id), "", "", "")
        i_id += 1
        #*** Cella SKILL ************
        if guid[39] <> 0:   #evito divisione per 0
            tooltip_SKILL = "K/D:"+ str(round(sum(guid[21:38]) / float(guid[39]),2))
        if guid[2] < 0:
            colore = "color:red"
        else:
            colore = "color:green"
        SKILL = cella(str(round(guid[2],1)), tooltip_SKILL, "", colore)
        #*** Cella NICK ************
        #_________ TOOLTIP
        rc_nick = "<div class='rc_nick'>%s</div>" %striphtml(str(guid[1]))  #nick
        masked_guid = guid[0][0:6] + "***"
        aff = round(guid[3] / M_CONF.Nt_roundXpoint + ((guid[4]-guid[8])/87400) / M_CONF.Nt_dayXpoint + guid[7], 1)
        affid = aff
        stx=""
        if affid < M_CONF.Nt_MinNot_toplay:
            stx="color:red"
            giorni = (M_CONF.Nt_MinNot_toplay - affid) * M_CONF.Nt_dayXpoint
            affid = str(affid) + " <span style='color:red;'>Non affidabile per %s giorni</span>" %str(giorni)
        f_conn = time.strftime("%d/%m/%Y&nbsp;%H:%M",time.localtime(guid[8]))
        #colonna1
        rc_col1_txt = "Guid: <b>%s</b><br />Level: <b>%s</b><br />Affidabilit&agrave;: <b>%s</b><br />First Visit: <b>%s</b>" %(masked_guid, str(guid[5]), str(affid), f_conn)
        rc_col1 = "<div class='rc_col1'>%s</div>" %rc_col1_txt
        #colonna2
        aliases = guid[10].split("  ")
        rc_col2_txt = "<b>ALIAS:</b><br />"
        for al in aliases:
            al=al.split(" ")
            if len(al) == 2:
                rc_col2_txt += (time.strftime("%d/%m/%Y&nbsp;%H:%M",time.localtime(float(al[0]))) + "&nbsp;<span class=rc_al>" + striphtml (str(al[1]) )+ "</span><br />")
        rc_col2 = "<div class='rc_col2'>%s</div>" %rc_col2_txt
        #colonna3
        rc_col3_txt = "<b>IP:</b><br />"
        if guid[20]:
            ips = guid[20].split(" ")
            for ip in ips:
                b = ip.split(".")
                masked_ip = ".".join([b[0],b[1],b[2],"***"])
                rc_col3_txt += (masked_ip + "<br />")
        else:
            rc_col3_txt += ("UNKNOWN<br />")
        rc_col3 = "<div class='rc_col3'>%s</div>" %rc_col3_txt
        rc_tip = rc_nick + rc_col1 + rc_col2 + rc_col3
        NICK_tooltip ="<div class='rc_tip'>%s</div>" %rc_tip
        #_________ CELLA
        id = "sp%s" %guid[0][0:8]
        txt = '<span onmouseover="TagToTip(\'%s\')" onmouseout="UnTip()">%s</span>' %(id , striphtml(str(guid[1])))
        cls = ""
        if guid[5] >= M_CONF.lev_admin:
            cls = "rc_cNICK_g"
        elif aff < M_CONF.MinNotoriety:
            cls = "rc_cNICK_r"
        NICK = cella(txt, "", cls, stx)
        NICK_SPAN = "<span id='%s'>%s</span>" %(id, NICK_tooltip)
        #*** Cella STREAK ************
        STREAK = cella(str(guid[9]), "", "", "")
        #*** Cella ROUNDS ************
        ROUNDS = cella(str(guid[3]), "", "", "")
        #*** Cella HSHOTS ************
        hits = float(guid[12] + guid[13] +guid[14] + guid[15] + guid[16])
        hs = round((guid[12]/hits)*100, 1)
        tr = round((guid[13]/hits)*100, 1)
        ar = round((guid[14]/hits)*100, 1)
        lg = round((guid[15]/hits)*100, 1)
        bo = round((guid[16]/hits)*100, 1)
        tooltip_HS = "Torso:%s Arms:%s Legs:%s Body:%s" %(str(tr), str(ar), str(lg), str(bo))
        hs1 = "%s&#37;" %str(hs)
        if hs > 16:
            colore = "color:red"
        else:
            colore = ""
        HSHOTS = cella(hs1, tooltip_HS, "", colore)
        #*** Cella IP ****************
        if guid[17]:
            b = guid[17].split(".")
            masked_ip = ".".join([b[0],b[1],b[2],"***"])
        else:
            masked_ip = "UNKNOWN"
        IP = cella(masked_ip, "", "", "")
        #*** Cella LAST VISIT ********
        hrs = (int(time.time() - guid[4]) // 60) // 60
        day = hrs // 24
        l_conn = "%d g. : %d h." % (day, hrs % 24)
        LASTVISIT = cella(l_conn, "", "", "")
        #*** CREO LA RIGA ************
        riga_txt = ID + NICK + SKILL + STREAK + ROUNDS + HSHOTS + IP + LASTVISIT
        riga = "<tr>%s</tr>" %riga_txt
        #_________ AGGIUNGO I TOOLTIPS
        riga += NICK_SPAN

        #*** AGGIUNGO LA RIGA ALLA TABELLA ************
        TABLE += riga

    TABLE += table_end  #Completo la table
    #Salvo in locale
    htmlfile = open("HTML" + "/" + M_CONF.w_tabella, "w")
    htmlfile.write(TABLE)
    htmlfile.close()
    #trasferisco
    if web_FTPtransfer("HTML" + "/" + M_CONF.w_tabella, M_CONF.w_tabella):
        return True
    else:
        return False

#web_rank()

def web_FTPtransfer(filefrom, fileto):
    """trasferisce un file sul webserver ausiliario"""
    esito = True
    from ftplib import FTP
    htmlfile = open(filefrom, "rb")
    try:
        connessione = FTP(M_CONF.w_url)
        connessione.login(M_CONF.w_login, M_CONF.w_password)   # connect to host, default port
        connessione.cwd(M_CONF.w_ftp_directory)
        connessione.storbinary('STOR ' + fileto, htmlfile)
        connessione.quit()
    except:
        htmlfile.close()
        esito = False
        #return esito
    finally:
        htmlfile.close()
        return esito

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
