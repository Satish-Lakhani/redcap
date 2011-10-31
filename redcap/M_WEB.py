#! /usr/bin/python
# -*- coding: utf-8 -*-

import time          #Funzioni tempo
import C_DB         #Classe che rappresenta il DB
import M_CONF

DB = C_DB.Database(M_CONF.NomeDB)
#'''
def web_rank():
    """crea la classifica in formato tabella a partire dal DB e la invia ad un altro server"""

    def add(x,y):
        return x+y

    def cella(contenuto, toltip = "", st = ""):          #sottofunzione che crea le celle
        #return "<td><a href='#'>%(contenuto)s<span>%(tooltip)s</span></a></td>" %{"contenuto": contenuto, "tooltip": toltip}
        return "<td title='%s' style='%s'>%s</td>" %(toltip, st, contenuto)

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
        if dati1[i][3] > M_CONF.minRounds:
            tmp.append(dati1[i] + dati2[i][1:len(dati2[i])] + dati3[i][1:len(dati3[i])] + dati4[i][1:len(dati4[i])])
        i+=1
    Dump = sorted(tmp, key=lambda dato: dato[2], reverse=True)    #record ordinati per skill decrescente

    #DATI: #0: GUID    # 1: Nick    # 2: Skill    # 3: Round    # 4: Lastconnection    # 5: Level    # 6: Tempban    # 7: Reputation    # 8: Firstconnect    # 9: streak    # 10: alias    # 11: varie
    #HIT: #12: head    # 13: torso    # 14: arms    # 15: legs    # 16: body    #LOC: #17: IP    # 18: provider    # 19: location    # 20: oldguids    #KILL: #21-38: kills #39: deaths

    table_ini = "<script type='text/javascript' src='wz_tooltip.js'></script><table class=\"sortable\"><tbody>" #parte iniziale della table
    header = "<tr><th>SKILL</th><th>NICK</th><th>STREAK</th><th>ROUNDS</th><th title='Headshots'>HS</th><th>IP</th><th>LAST VISIT</th></tr>" #Header (SKILL, NICK, ROUNDS, HIT, IP, LASTVISIT
    table_end = "</tbody></table>"                  #parte finale della table
    TABLE = table_ini + header                  #contenuto della table

    for guid in Dump:                               #CREO LA RIGA ed i suoi span. RIGHE CON TOOLTIP: <a href="#" onmouseover="TagToTip('Span2')" onmouseout="UnTip()">Homepage </a>
        #*** Cella SKILL ************
        if guid[39] <> 0:   #evito divisione per 0
            tooltip_SKILL = "K/D:"+ str(round(sum(guid[21:38]) / float(guid[39]),2))
        SKILL = cella(str(round(guid[2],1)), tooltip_SKILL, "")
        #*** Cella NICK ************
        #_________ TOOLTIP
        rc_nick = "<div class='rc_nick'>%s</div>" %striphtml(str(guid[1]))  #nick
        masked_guid = guid[0][0:6] + "***"
        aff = round(guid[3] / M_CONF.Notoriety["roundXpoint"] + ((guid[4]-guid[8])/87400) / M_CONF.Notoriety["dayXpoint"] + guid[7], 1)
        affid = aff
        if affid < M_CONF.MinNotoriety:
            giorni = (M_CONF.MinNotoriety - affid) * M_CONF.Notoriety["dayXpoint"]
            affid = str(affid) + " <span style='color:red;'>Non affidabile per %s giorni</span>" %str(giorni)
        f_conn = time.strftime("%d/%m/%Y&nbsp;%H:%M",time.localtime(guid[8]))
        rc_col1_txt = "Guid: <b>%s</b><br />Level: <b>%s</b><br />Affidabilit&agrave;: <b>%s</b><br />First Visit: <b>%s</b>" %(masked_guid, str(guid[5]), str(affid), f_conn)
        rc_col1 = "<div class='rc_col1'>%s</div>" %rc_col1_txt
        aliases = guid[10].split("  ")
        rc_col2_txt = "<b>ALIAS:</b><br />"
        for al in aliases:
            al=al.split(" ")
            if len(al) == 2:
                rc_col2_txt += (time.strftime("%d/%m/%Y&nbsp;%H:%M",time.localtime(float(al[0]))) + "&nbsp;<span class=rc_al>" + striphtml (str(al[1]) )+ "</span><br />")
        rc_col2 = "<div class='rc_col2'>%s</div>" %rc_col2_txt
        rc_col3_txt = "Under Construction"
        rc_col3 = "<div class='rc_col3'>%s</div>" %rc_col3_txt
        rc_tip = rc_nick + rc_col1 + rc_col2 + rc_col3
        NICK_tooltip ="<div class='rc_tip'>%s</div>" %rc_tip
        #_________ CELLA 
        id = "span1%s" %guid[0]
        txt = '<span onmouseover="TagToTip(\'%s\')" onmouseout="UnTip()">%s</span>' %(id ,  striphtml(str(guid[1])))
        stile = ""
        if guid[5] >= M_CONF.lev_admin:
            stile = "color:green;"
        elif aff < M_CONF.MinNotoriety:
            stile = "color:red;"
        NICK = cella(txt, "", stile)
        NICK_SPAN = "<span id='%s'>%s</span>"%(id, NICK_tooltip)

        #*** CREO LA RIGA ************
        riga_txt = SKILL + NICK
        riga = "<tr>%s</tr>" %riga_txt
        riga += NICK_SPAN

        #*** AGGIUNGO LA RIGA ALLA TABELLA ************
        TABLE += riga
    TABLE += table_end
    return TABLE
'''
        tooltip_SKILL = "K" + str(sum(guid[21:38])) + "&nbsp;D" + str(guid[39])
        if guid[39] <> 0:   #evito divisione per 0
            tooltip_SKILL += "&nbsp;K/D"+ str(round(sum(guid[21:38]) / float(guid[39]),2))
        riga += cella(striphtml(str(round(guid[2],1))), tooltip_SKILL)                      #Aggiungo cella SKILL
        riga += cella(striphtml(str(guid[9])))                                              #Aggiungo cella STREAK
        riga += cella(striphtml(str(guid[3])))                                              #Aggiungo cella ROUND
        if (guid[12] + guid[13] + guid[14] + guid[15] + guid[16]) <> 0:
            tot_hits = 100.0 / (guid[12] + guid[13] + guid[14] + guid[15] + guid[16])
            hits = "H:%s&nbsp;T:%s&nbsp;A:%s&nbsp;L:%s&nbsp;B:%s" %(str(round(guid[12] * tot_hits , 1)), str(round(guid[13] * tot_hits , 1)), str(round(guid[14] * tot_hits , 1)), str(round(guid[15] * tot_hits , 1)), str(round(guid[16] * tot_hits , 1)))
        else:
            hits = "N.D."
        riga += cella(striphtml(hits))                                                      #Aggiungo cella HITS
        ip = str(guid[17])
        try:
            b = ip.split(".")
            masked_IP = ".".join([b[0],b[1],b[2],"***"])
        except:
            masked_IP = "unknown"
        riga += cella(masked_IP)                                                            #Aggiungo cella IP
        last = time.strftime("%y/%m/%d %H:%M",time.localtime(guid[4]))
        riga += cella(last)                                                                 #Aggiungo cella lastseen
        riga = "<tr>%s</tr>"%(riga)

        corpo += riga
    return "<table class=\"sortable\"><tbody>%s</tbody></table>" %corpo
'''
table = web_rank()
print table
'''
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