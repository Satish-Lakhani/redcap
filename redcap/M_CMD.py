#! /usr/bin/python
# -*- coding: utf-8 -*-

import M_CONF

comandi = [
#["autobalance",r": (?P<rich>\d+) .*?: !ab",RCconf.lev_autobalance],
#["ban",r": (?P<rich>\d+) .*?: !ban (?P<target>.*)",RCconf.lev_ban],
#["bilancia",r": (?P<rich>\d+) .*?: !tm",RCconf.lev_balance],
["callvote",r"!v$",M_CONF.lev_callvote],
#["cyclemap",r": (?P<rich>\d+) .*?: !cy",RCconf.lev_cycle],
#["deregistra",r": (?P<rich>\d+) .*?: !unreg (?P<target>.*)", RCconf.lev_unreg],
["forceteam",r"!f(?P<team>[rbs]) (?P<target>.*)",M_CONF.lev_force],
#["info",r": (?P<rich>\d+) .*?: !info", RCconf.lev_info],
#["isk",r": (?P<rich>\d+) .*?: !isk", RCconf.lev_isk],
#["join",r": (?P<rich>\d+) .*?: !join (?P<target>.*)", RCconf.lev_join],
["kick",r"!k (?P<target>.*)", M_CONF.lev_kick],
["level",r"!lev(?P<num>\d*) (?P<target>.*)",M_CONF.lev_level],
["mute",r"!m (?P<target>.*)",M_CONF.lev_mute],
#["nick",r": (?P<rich>\d+) .*?: !z (?P<target>.*)", RCconf.lev_nick],
["nuke",r"!n (?P<target>.*)",M_CONF.lev_nuke],
#["nukeall",r": (?P<rich>\d+) .*?: !nall", RCconf.lev_nukeall],
["ora",r"!ora$",M_CONF.lev_ora],
#["passport",r": (?P<rich>\d+) .*?: !passport", RCconf.lev_passport],
["password",r": (?P<rich>\d+) .*?: !pwd (?P<pwd>\S*)", M_CONF.lev_password],                             #\S = qualsiasi carattere salvo lo spazio.
#["pause",r": (?P<rich>\d+) .*?: !pause", RCconf.lev_pause],
#["rcrestart",r": (?P<rich>\d+) .*?: !restart",RCconf.lev_RCrestart],
#["registra",r": (?P<rich>\d+) .*?: !reg (?P<target>.*)", RCconf.lev_reg],
#["skill",r": (?P<rich>\d+) .*?: !sk\s*(?P<target>.*)",RCconf.lev_skill],
["slap", r"!s(?P<num>\d*) (?P<target>.*)",M_CONF.lev_slap],
#["status",r": (?P<rich>\d+) .*?: !status",RCconf.lev_status],
#["tmpban",r": (?P<rich>\d+) .*?: !b(?P<num>\d*) (?P<target>.*)",RCconf.lev_tmpban],
#["top",r": (?P<rich>\d+) .*?: !top", RCconf.lev_top],
#["war",r": (?P<rich>\d+) .*?: !!war \\(?P<pass>.*)", RCconf.lev_war],
]
