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
"ut4_company", "ut4_docks","ut4_herring",
"ut4_horror","ut4_ricochet",
]

colori = {          #colori per i dialoghi
"0":"#00FF00","1":"#00FFFF","2":"#FFFF00","3":"#FFFFCC","4":"#006600","5":"#0066FF","6":"#330033","7":"#330033",
"8":"#FF6600","9":"#FF66FF","10":"#FF66FF","11":"#969696","12":"#99CC99","13":"#FFCCCC","14":"#6699FF"
}

tabs = [            #tabelle del DB con guid
"DATI", "DEATH", "HIT", "KILL", "LOC"
]

def automaintenance():
    """Esegue le operazioni di manutenzione giornaliera"""
    timestamp = time.strftime("%Y_%b_%d", time.localtime())
    db_clean_guid()                 #elimino le guid vecchie
    db_clean_alias()                #elimino gli alias vecchi in eccesso
    db_backup(timestamp)            #faccio backup del database
    log_chat_backup(timestamp)      #creo il log di chat
    log_backup(timestamp)           #faccio il backup del log
    web_rank()                      #creo una classifica aggiornata
    if M_CONF.Website_ON:           #se esiste un sito web di appoggio
        web_FTPtransfer(M_CONF.NomeArchivi + "/" + timestamp + "_saylog.log", M_CONF.w_dialoghi)
        web_FTPtransfer("HTML" + "/" + M_CONF.w_tabella, M_CONF.w_tabella)
    cr_riavvia()


def cr_riavvia():
    """restarto RedCap ed eventualmente il server"""
    import os
    import sys
    import M_RC
    if M_CONF.gameserver_autorestart > 0:
        M_RC.scrivilog(" Redcap and UrT Server restarted.", M_CONF.activity)
        os.system("./S_full_restart.sh")
        time.sleep(5)       #aspetto che il gameserver riparta
        sys.exit()
    else:
        M_RC.scrivilog("Redcap restarted.", M_CONF.activity)
        M_RC.SCK.cmd("exec " + M_CONF.SV_Baseconf)                   #ricarico il config TODO vedere se sufficiente per ricreare il games.log
        time.sleep(5)       #aspetto che il gameserver riparta
        sys.exit()

def db_backup(timestamp):
    import shutil
    import M_RC
    shutil.copy2(M_CONF.NomeDB, M_CONF.NomeArchivi + "/" + timestamp + "_" + M_CONF.NomeDB)         #Copio il DB in Archivi
    DB.connetti()
    DB.esegui("""VACUUM""")   #DOPO che l'ho backuppato, lo comprimo.
    DB.salva()
    DB.disconnetti()
    M_RC.scrivilog("DB backup done.", M_CONF.activity)

def db_clean_alias():
    """Elimino gli alias in eccedenza"""
    import M_RC
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
    M_RC.scrivilog("DB alias cleaned.", M_CONF.activity)

def db_clean_guid():
    """pulizia periodica DB dai record non piu utilizzati"""
    import M_RC
    DB.connetti()
    res = DB.esegui(DB.query["cleanoldplayers"], (time.time(), float(M_CONF.maxAbsence*86400), time.time())).fetchall()
    for guid in res:
        for tab in tabs:
            DB.esegui(DB.query["delplayer"] % (tab, guid[0]))  #Elimino guid che non frequentano piu' il gameserver da M_CONF.maxAbsence giorni.
    DB.salva()
    DB.disconnetti()
    M_RC.scrivilog("DB old record cleaned.", M_CONF.activity)

'''
def db_delete_player(guid, tabs):
    """cancella un player dal DB. Presuppone il DB gia connesso."""
    for tab in tabs:
        DB.esegui(DB.query["delplayer"] % (tab, guid))
'''

def log_backup(timestamp):
    """Esegue il backup del file di log."""
    import os
    import re
    import M_RC
    logfile = open(M_CONF.NomeFileLog, "r")
    contenuto = logfile.read()          #leggo il log
    logfile.close()
    contenuto=re.sub(r"Item: .* ","",contenuto) #elimino le voci Item
    logfile = open(M_CONF.NomeArchivi + "/" + timestamp + ".log", "w")
    logfile.write(contenuto)              #creo il file di log in Archivi
    logfile.close()
    M_RC.scrivilog("UrT Log backup done.", M_CONF.activity)
    os.remove(M_CONF.NomeFileLog)   #cancello il vecchio file

def log_chat_backup(timestamp):
    """crea un file di chat"""
    import re
    import M_RC
    logfile = open(M_CONF.NomeFileLog, "r")
    dialoghi = logfile.read()   #Estraggo i dialoghi
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
    logfile = open(M_CONF.NomeArchivi + "/" + timestamp + "_saylog.log", "w")       #salvo il tutto in un file
    logfile.write(html)
    logfile.close()
    M_RC.scrivilog("UrT Chatlog backup done.", M_CONF.activity)

def web_rank():
    """crea la classifica in formato tabella a partire dal DB"""
    def cella(contenuto,  toltip = "",  cls = "",  st = ""):            #sottofunzione che crea le celle
        return "<td title='%s' class='%s' style='%s'>%s</td>" %(toltip, cls, st, contenuto)
    def striphtml(testo):                                                       #strippo l'html
        testo = testo.replace("<", "&lt;")
        testo = testo.replace(">", "&gt;")
        return testo

    ## RECUPERO DATI DAL DB
    DB.connetti()                                                                   #recupero i dati dal DB
    dati1 = DB.esegui(DB.query["getallorderedbyguid"]%"DATI").fetchall()
    dati2 = DB.esegui(DB.query["getallorderedbyguid"]%"HIT").fetchall()
    try:                    #inserito per ovviare crash da caratteri non ASCII introdotti in DB da versioni precedenti
        dati3 = DB.esegui(DB.query["getallorderedbyguid"]%"LOC").fetchall()
    except:
        DB.esegui("""UPDATE LOC SET LOCATION=''""")
        DB.salva()
        dati3 = DB.esegui(DB.query["getallorderedbyguid"]%"LOC").fetchall()
    dati4 = DB.esegui(DB.query["getallorderedbyguid"]%"KILL").fetchall()
    DB.disconnetti()
    i=0
    cicli = len(dati1)
    tmp = []
    while i < cicli:
        if dati1[i][3] > M_CONF.w_minRounds:
            tmp.append(dati1[i] + dati2[i][1:len(dati2[i])] + dati3[i][1:len(dati3[i])] + dati4[i][1:len(dati4[i])])
        i+=1
    Dump = sorted(tmp, key=lambda dato: dato[2], reverse=True)    #record ordinati per skill decrescente

    #DATI: #0: GUID    # 1: Nick    # 2: Skill    # 3: Round    # 4: Lastconnection    # 5: Level    # 6: Tempban    # 7: Reputation    # 8: Firstconnect    # 9: streak    # 10: alias    # 11: varie
    #HIT: #12: head    # 13: torso    # 14: arms    # 15: legs    #LOC: #16: IP    # 17: provider    # 18: location    # 19: oldip    #KILL: #20-37: kills #38: deaths

    ## PREPARO LA PAGINA HTML
    lasttableupdate = str(time.strftime("%d.%b&nbsp;%H:%M",time.localtime()))
    table_ini = "<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.01 Transitional//EN'><html><head><link href='rank.css' rel='stylesheet' type='text/css' />" +\
    "<script src='%s/sorttable.js'></script></head><body><div class=\"redcap\"><script type='text/javascript' src='wz_tooltip.js'></script><table class=\"sortable\"><tbody>" %M_CONF.w_script_url
    table_end = "</tbody></table></div></body></html>"
    header = "<tr title=\"Last update: %s\">" %lasttableupdate +\
    "<th>ID</th>"+\
    "<th>NICK</th>"+\
    "<th>SKILL</th>"+\
    "<th>STREAK</th>"+\
    "<th>ROUNDS</th>"+\
    "<th title='Headshots'>HS</th>"+\
    "<th>LR</th>"+"<th>SR</th>"+"<th>M4</th>"+"<th>g36</th>"+"<th>AK</th>"+"<th>NG</th>"+"<th>PS</th>"+"<th>HK</th>"+"<th>BL</th>"+"<th>MP</th>"+\
    "<th>UM</th>"+"<th>SP</th>"+"<th>DE</th>"+"<th>BE</th>"+"<th>NA</th>"+"<th>KN</th>"+\
    "<th>LAST IP</th>"+\
    "<th>LAST VISIT</th>"+\
    "</tr>"  
    TABLE = table_ini + header                  #contenuto della table
    i_id = 1
    for guid in Dump:                           #CREO LA RIGA ed i suoi span. RIGHE CON TOOLTIP: <a href="#" onmouseover="TagToTip('Span2')" onmouseout="UnTip()">Homepage </a>
        tot_kills = sum(guid[20:37])         #kill totali fatte dal player
        #*** Cella ID ***************
        ID = cella(str(i_id), "", "", "")
        i_id += 1
        #*** Cella SKILL ************
        if guid[38] <> 0:   #evito divisione per 0
            tooltip_SKILL = "K/D:"+ str(round(tot_kills / float(guid[38]),2))
        if guid[2] < 0:
            colore = "color:red"
        else:
            colore = "color:green"
        SKILL = cella(str(round(guid[2],1)), tooltip_SKILL, "", colore)
        #*** Cella NICK ************
        #_________ TOOLTIP_____________
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
        if guid[19]:
            ips = guid[19].split(" ")
            for ip in ips:
                b = ip.split(".")
                masked_ip = ".".join([b[0],b[1],b[2],"***"])
                rc_col3_txt += (masked_ip + "<br />")
        else:
            rc_col3_txt += ("UNKNOWN<br />")
        rc_col3 = "<div class='rc_col3'>%s</div>" %rc_col3_txt
        rc_tip = rc_nick + rc_col1 + rc_col2 + rc_col3
        NICK_tooltip ="<div class='rc_tip'>%s</div>" %rc_tip
        #_________ CELLA___________
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
        hits = float(guid[12] + guid[13] +guid[14] + guid[15])
        hs = round((guid[12]/hits)*100, 1)
        tr = round((guid[13]/hits)*100, 1)
        ar = round((guid[14]/hits)*100, 1)
        lg = round((guid[15]/hits)*100, 1)
        #bo = round((guid[16]/hits)*100, 1)
        tooltip_HS = "Torso:%s Arms:%s Legs:%s" %(str(tr), str(ar), str(lg))
        hs1 = "%s&#37;" %str(hs)
        if hs > 16:
            colore = "color:red"
        else:
            colore = ""
        HSHOTS = cella(hs1, tooltip_HS, "", colore)
        #*** Celle WEAPONS ************
        Lr = cella(str(round(float(guid[26])*100/tot_kills,1)), "Lr300", "", "color:#EEE8AA")
        Sr8 = cella(str(round(float(guid[33])*100/tot_kills,1)), "SR8", "", "color:#EEE8AA")
        M4 = cella(str(round(float(guid[36])*100/tot_kills,1)), "M4", "", "color:#EEE8AA")
        G36 = cella(str(round(float(guid[27])*100/tot_kills,1)), "G36", "", "color:#EEE8AA")
        Ak = cella(str(round(float(guid[34])*100/tot_kills,1)), "AK103", "", "color:#EEE8AA")
        Neg = cella(str(round(float(guid[35])*100/tot_kills,1)), "Negev", "", "color:#EEE8AA")
        Psg = cella(str(round(float(guid[28])*100/tot_kills,1)), "Psg1", "", "color:#EEE8AA")
        Hk = cella(str(round(float(guid[29])*100/tot_kills,1)), "H&K69", "", "color:#EEE8AA")
        Bled = cella(str(round(float(guid[30])*100/tot_kills,1)), "Bleeding", "", "color:#FFA500")
        Mp5 = cella(str(round(float(guid[25])*100/tot_kills,1)), "Mp5K", "", "color:#87CEEB")
        Ump = cella(str(round(float(guid[24])*100/tot_kills,1)), "Ump45", "", "color:#87CEEB")
        Spas = cella(str(round(float(guid[23])*100/tot_kills,1)), "Spas", "", "color:#87CEEB")
        De = cella(str(round(float(guid[22])*100/tot_kills,1)), "DE", "", "color:#88CC88")
        Ber = cella(str(round(float(guid[21])*100/tot_kills,1)), "Beretta", "", "color:#88CC88")
        Nade = cella(str(round(float(guid[32])*100/tot_kills,1)), "Nade", "", "color:#FFA500")
        Knife = cella(str(round(float(guid[20])*100/tot_kills,1)), "Knife", "", "color:#88CC88")
        ARMI = Lr + Sr8 + M4 + G36 + Ak + Neg + Psg + Hk + Bled + Mp5 + Ump + Spas + De + Ber + Nade + Knife
        #*** Cella IP ****************
        if guid[17]:
            b = guid[16].split(".")
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
        riga_txt = ID + NICK + SKILL + STREAK + ROUNDS + HSHOTS + ARMI + IP + LASTVISIT
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

#web_rank()

def web_FTPtransfer(filefrom, fileto):
    """trasferisce un file sul webserver ausiliario"""
    esito = True
    import M_RC
    from ftplib import FTP
    htmlfile = open(filefrom, "rb")
    try:
        connessione = FTP(M_CONF.w_url)
        connessione.login(M_CONF.w_login, M_CONF.w_password)   # connect to host, default port
        connessione.cwd(M_CONF.w_ftp_directory)
        connessione.storbinary('STOR ' + fileto, htmlfile)
        connessione.quit()
    except:
        esito = False
    finally:
        htmlfile.close()
        if esito:
            M_RC.scrivilog("File %s transfer OK." %filefrom, M_CONF.activity)
        else:
           M_RC.scrivilog("File %s transfer not achieved." %filefrom, M_CONF.activity)

#automaintenance()

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
