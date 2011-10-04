#! /usr/bin/python
# -*- coding: utf-8 -*-

import M_CONF
#TODO siamo sicuri che (?P<rich>\d+) sia ancora necessario?
comandi = [
["balancemode", r"!ab", M_CONF.lev_balancemode],
["ban", r"!ban (?P<target>.*)", M_CONF.lev_ban],
["balance",r"!tm", M_CONF.lev_balance],
["callvote",r"!v$",M_CONF.lev_callvote],
["cyclemap",r"!cy", M_CONF.lev_cycle],
#["deregistra",r": (?P<rich>\d+) .*?: !unreg (?P<target>.*)", RCconf.lev_unreg],
["esegui", r"!cmd (?P<cmd>.*)", M_CONF.lev_esegui],
["forceteam",r"!f(?P<team>[rbs]) (?P<target>.*)",M_CONF.lev_force],
#["info",r": (?P<rich>\d+) .*?: !info", RCconf.lev_info],
#["join",r": (?P<rich>\d+) .*?: !join (?P<target>.*)", RCconf.lev_join],
["kick",r"!k (?P<target>.*)", M_CONF.lev_kick],
["level",r"!lev(?P<num>\d*) (?P<target>.*)",M_CONF.lev_level],
["map", r"!map (?P<map>.*)", M_CONF.lev_map],
["mute",r"!m (?P<target>.*)",M_CONF.lev_mute],
["muteall",r"!mall", M_CONF.lev_muteall],
["nuke",r"!n (?P<target>.*)",M_CONF.lev_nuke],
#["nukeall",r": (?P<rich>\d+) .*?: !nall", RCconf.lev_nukeall],
["ora",r"!ora$",M_CONF.lev_ora],
#["passport",r": (?P<rich>\d+) .*?: !passport", RCconf.lev_passport],
["password",r"!pwd (?P<pwd>\S*)", M_CONF.lev_password],                             #\S = qualsiasi carattere salvo lo spazio.
#["pause",r": (?P<rich>\d+) .*?: !pause", RCconf.lev_pause],
#["rcrestart",r": (?P<rich>\d+) .*?: !restart",RCconf.lev_RCrestart],
#["registra",r": (?P<rich>\d+) .*?: !reg (?P<target>.*)", RCconf.lev_reg],
["skill",r"!sk\s*(?P<target>.*)",M_CONF.lev_skill],
["slap", r"!s(?P<num>\d*) (?P<target>.*)", M_CONF.lev_slap],
["status", r"!z\s*(?P<target>.*)", M_CONF.lev_status],
["tempban",r"!b(?P<num>\d*) (?P<target>.*)",M_CONF.lev_tmpban],       #!b123 pippo
#["top",r": (?P<rich>\d+) .*?: !top", RCconf.lev_top],
["unwar",r"!unwar", M_CONF.lev_unwar],
["war",r"!war\s*(?P<cfg>.*)", M_CONF.lev_war],
]
