#! /usr/bin/python
# -*- coding: utf-8 -*-

import M_CONF

comandi = [
["alias", r"!al (?P<target>.*)", M_CONF.lev_alias, "al"],
["balancemode", r"!ab", M_CONF.lev_balancemode, "ab"],
["ban", r"!(?P<un>(un)*)ban (?P<target>.*)", M_CONF.lev_ban, "ban"],
["balance",r"!tm|!teams", M_CONF.lev_balance, "tm"],
["callvote",r"!v$",M_CONF.lev_callvote, "v"],
["cyclemap",r"!cy", M_CONF.lev_cycle, "cy"],
["dbfind",r"!find (?P<target>.*)", M_CONF.lev_dbfind, "find"],
["dbnick",r"!dbnick (?P<target>.*)", M_CONF.lev_dbnick, "dbnick"],
["esegui", r"!cmd (?P<cmd>.*)", M_CONF.lev_esegui, "cmd"],
["forceteam",r"!f(?P<team>[rbs]) (?P<target>.*)",M_CONF.lev_force, "f"],
["forgive",r"^!fp\s*(?P<target>.*)", M_CONF.lev_forgive, "fp"],
["forgiveall",r"!fall (?P<target>.*)", M_CONF.lev_forgiveall, "fall"],
["gears",r"!gears\s*(?P<gears>.*)",M_CONF.lev_gears, "gears"]
["help", r"!help\s*(?P<cmd>.*)", M_CONF.lev_help, "help"],
["info",r"!info", M_CONF.lev_info, "info"],
#["join",r": (?P<rich>\d+) .*?: !join (?P<target>.*)", RCconf.lev_join],
["kick",r"!kk (?P<target>.*)", M_CONF.lev_kick, "kk"],
["level",r"!lev(?P<num>\d*) (?P<target>.*)",M_CONF.lev_level, "lev"],
["map", r"!map\s+(?P<map>.*)", M_CONF.lev_map, "map"],
["maplist", r"!maplist", M_CONF.lev_maplist, "maplist"],
["mute",r"!m (?P<target>.*)",M_CONF.lev_mute, "m"],
["muteall",r"!mall", M_CONF.lev_muteall, "mall"],
["notlev",r"!notoriety\s+(?P<num>\d*)",M_CONF.lev_notoriety, "notoriety"],
["nuke",r"!n\s+(?P<target>.*)",M_CONF.lev_nuke, "n"],
#["nukeall",r": (?P<rich>\d+) .*?: !nall", RCconf.lev_nukeall],
["ora",r"!ora$",M_CONF.lev_ora, "ora"],
["password",r"!pwd\s+(?P<pwd>\S*)", M_CONF.lev_password, "pwd"],                             #\S = qualsiasi carattere salvo lo spazio.
["rcrestart",r"!restart",M_CONF.lev_RCrestart, "restart"],
["recordreset",r"!rere (?P<target>.*)",M_CONF.lev_recordreset, "rere"],
["silent", r"!silent", M_CONF.lev_silent, "silent"],
["skill",r"!sk\s*(?P<target>.*)",M_CONF.lev_skill, "sk"],
["slap", r"!s(?P<num>\d*) (?P<target>.*)", M_CONF.lev_slap, "s"],
["smite", r"!sm (?P<target>.*)", M_CONF.lev_smite, "sm"],
["spam",r"!(?P<un>(un)*)spam (?P<frase>.*)", M_CONF.lev_spam, "spam"],
["spamlist", r"!spamlist", M_CONF.lev_spamlist, "spamlist"],
["status", r"!z\s*(?P<target>.*)", M_CONF.lev_status, "status"],
["tempban",r"!tban(?P<num>\d*)\s+(?P<target>.*)",M_CONF.lev_tmpban, "tban"],
["top",r"!top", M_CONF.lev_top, "top"],
["trust",r"!(?P<un>(un)*)trust(?P<num>\d*) (?P<target>.*)", M_CONF.lev_trust, "trust"],
["unwar",r"!unwar", M_CONF.lev_unwar, "unwar"],
["war",r"!war\s*(?P<cfg>.*)", M_CONF.lev_war, "war"],
]
