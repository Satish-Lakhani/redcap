#! /usr/bin/python
# -*- coding: utf-8 -*-

#IMPORTANT!: TRANSLATION TO OTHER LANGUAGE
#1) MAKE A COPY OF THIS FILE AND RENAME IT "M_YOURLANGUAGE.PY"
#2)TRANSLATE INTO YOUR LANGUAGE THE SENTENCE ON THE RIGHT SIDE OF COLON (:) - USE ASCII 128 ONLY.
#3)DO NOT MODIFY OR CANCEL THE %s VARIABLES!! DO NOT MODIFY ANYTHING OUTSIDE OF SENTENCES " " !!
#4)IN "M_CONF.PY" CHANGE THE VALUE OF RC_lang = "ITA" TO RC_lang = "YOURLANGUAGE"
#5)RESTART REDCAP

RC_outputs = {
"accident":"^5%s ^3was distracted killed by himself",
"adminrights": "^3Admin level assigned to ^5%s",
"alias": "^3Alias of ^5%s:^3",
"antirecon": "^5%s ^1kicked for double connection in less than ^6%s",
"balanceauto":"^3Not needed: team balance is  ^7AUTOMATIC ^3at round end",
"balanceclan":"^3Not possibile when balancing is in ^7CLAN MODE",
"balancexecuted": "^3Team balancing executed.",
"balancemanual": "^3Team balancing ^7if needed ^3at round end",
"balancemode": "^3Team balancing ^6%s",
"balancenoneed": "^3Teams already balanced. Ask to an admin for shuffling.",
"balanceoff":"^3Team balancing is OFF. Use ^6!ab ^3 for switch it ON",
"ban": "^5%s ^1is not welcome on this server anymore.",
"bestplayers": "^3Best players:",
"caricoplayer": "^5%s ^3 data loaded from DB",
"dbnick":"^5%s ^3assigned as main nick",
"mapskill": " ^5%s^3 map skill: ^6%s",
"executed": "^3Command ^6%s ^3executed",
"forgiven": "^3Player ^5%s ^3forgiven",
"forgivenall": "^3All teammates forgiven",
"forgivenone": "^3Nothing to forgive to ^5%s",
"flood": "^5%s ^1kicked for flooding",
"guidchange": "^1CHEATER FOUND: ^5%s ^1in game GUID change. ^1Kicked",
"headshot": "^5%s ^7%s HS ^3(^6%s o/o^3)",
"insults": "^3Insults are not allowed. ^1%s more times and you ll be kicked",
"invalidguid": "^1POSSIBLE CHEAT: ^5%s ^1kicked for irregular guid",
"invalidnick": "^5%s ^1kicked for irregular Nick",
"levassigned":"^3Level ^6%s ^3assigned to ^5%s.",
"lownotoriety": "^5%s ^1Low reliability or new QKEY: ^6%s ^3against ^6%s ^3required",
"lownotoriety2": "^3Come back in ^6%s ^3days with the ^2SAME QKEY",
"movedtoblue": "^3%s moved to blue team: ^5%s",
"movedtored": "^3%s moved to red team: ^5%s",
"muteall": "^1Mute/Unmute all!",
"muted":"^5%s ^3muted because he was still muted when leaved at last disconnect",
"nickchanges": "^5%s ^1kicked because of multiple nick change (%s)",
"newfake":"^3You are using a new fake. Reliability reduced by ^6%s. ^3Your reliability is now %s",
"noavailcmd": "^3This command is not available during startup.",
"noclearcfg": "^3Ambiguous or not existing config.",
"nocleartarget": "^3Ambiguous Nick. Check again or use slot ID",
"noclearmap": "^3Ambiguous or not existing. Check again or use ^6!cmd mapname",
"noIDfound": "^3Player ID not found. Use ^2!find ^3command to found the right ID.",
"nolevel": "^7Level %s ^3command your level is ^7%s",
"norecorderase": "^1You cannot clean a record",
"notimefromini": "^1You cannot call for a vote in the first 60 seconds",
"notimetocmd": "^3Still wait for ^7%s minutes ^3to call this command.",
"not_update": "^3Notoriety of ^5%s ^3= ^7%s",
"not_changed": "^3MIN. Notoriety to play in this server: ^6%s",
"nuked": "^3Nuke launched on ^5%s ^3by ^5%s",
"ora": "^3It's ^7%s",
"pwdset": "^3Password set. Reload the map to activate it",
"record_alltime": "^2TOP Kill streak by ^5%s ^6%s kills",
"record_daily": "^2DAILY Kill streak by ^5%s ^6%s kills",
"record_monthly": "^2MONTHLY Kill streak by ^5%s ^6%s kills",
"record_no_not": "^5%s, ^3reliability too low. No kill streak record allowed.",
"record_no_ppl": "^3Less than ^7%s ^3players in game.  ^5%s's kill streak ^3not saved",
"record_personal": "^5%s ^2personal record ^6%s kills",
"record_weekly": "^2WEEKLY Kill streak by ^5%s ^6%s kills",
"resetdone": "^3Record %s erased.",
"resetnotdone":"^1Error. ^3Specify a parameter: %s",
"restart": "^1 Restarting RedCap...",
"salvoplayer": "^3Saving ^5%s data...",
"silentmode": "^3Silent mode ^6%s",
"skill": "^3Skill: ^7%s ^3Map skill: ^7%s ^3Kill streak: ^7%s ",
"smited": "^3Godwill hit ^5%s",
"space":"^3Server full. ^5%s ^3enter in game or you will be kicked.",
"spacekicked": "^3Server full. Spectator ^5%s ^3kicked.",
"spamadded":"^3Message added.",
"spamerased":"^3Message erased",
"spamnotfound":"^1Message not found.",
"startup":"^2RedCap is in start-up mode.",
"startupend": "^3Start-up is finished. ^2RedCap is fully running.",
"stillban": "^5%s, ^1you are still banned until ^6%s",
"suicide": "^1Suicide: ^3penalty of ^6%s ^3skill points",
"tbkicked":"^3kicked ^5%s",
"tempban": "^5%s ^1is banned for ^7%s ^1hours.",
"tempbanmax": "^3Max tempban value is ^6%s",
"thit": "^1NO TEAMHITS! ^3Skill penalty applied. Warning level ^1%s ",
"tkill": "^1NO TEAMKILL! ^3Skill penalty applied. Warning level ^1%s ",
"toohighlevel":"^1You cannot assign levels higher than your, that is ^6%s",
"toomanyres":"^3Too many results ^5(%s). ^3Please better specify the nick.",
"top": "^2%s record: ^4%s ^5%s ^2: %s #",
"unbandone": "^3Unban done. If problems manually unban the IP using ^2!cmd removeIP x.y.z.k",
"voteON":"^3ote is now enabled for ^7%s ^3seconds",
"voteOFF":"^3Vote disabled",
"warbaseloaded" : "^2War mode ON. ^3Loading %s ...",
"warloaded": "^2Practice war mode ON. ^3Loading %s ...",
"warning":"^5%s ^1kicked for reaching of warning limit",
"warunloaded": "^2War ended. ^3Reloading %s ...",
"wrongcmd":"^1I'm ^2RedCap^1, not B3 or some other bot!.",
}

RC_kills = {        #messaggi di killstreak
0 :"^5%s ^3stopped ^5%s's kill streak",
1 :"",
2 :"",
3 :"",
4 : '^5%s^3 is in killing mode...',
5 : '^5%s^3 is warming up: ^15 ^3kills!',
6 : '^3 there are six new corpses thanks to ^5%s ',
7 : '^4%s^3 7 kill? Not so bad!',
8 : '^3Eigth kill by ^5%s, ^3Is he camping?',
9 : '^5%s^3 9 kills. Looking for a record?',
10 : '^5%s^3 1^40 ^3K^4I^5L^6L^8S^9!! ',
11 : '^5%s^3 11 kills! You are not a noob...',
12 : '^5%s^3 12 kills...aimbot or wallhack?',
13 : '^5%s^3 13 kills? ^1Danger! There is a PRO in game!',
14 : '^3 14 kills? Save private ^5%s!',
15 : '^5%s^3 15 kills? are you Tarquin?!',
16 : '^5%s^3 16 kills? 16 kills? one more and i\'ll kick you!!',
17 : '^54%s^3 17 kills? I was kidding!',
18 : '^5%s^3 18 ^1You are more pro than before!',
19 : '^5%s^3 19 kills! Are you playing against fools!?!?',
20 : '^5%s^3 20 ^3KILLS^4!^5!^6!',
21 : '^5%s^3 21 kills...i can\'t believe it! :-(',
22 : '^5%s^3 22 kills? 1337!',
23 : '^5%s^3 23 kill? ^4ok guys, John Rambo is here',
24 : '^5%s^3 24 corpses... ^4bigger massacre than Waco!',
25 : '^5%s^3Kills counter is OVER! ^3U^4N^6B^1E^7L^8I^9E^0V^1A^3B^5L^3E^6!',
}

RC_logoutputs = {
"command": "%s alias %s (lev:%s) used: %s (lev:%s)",
}

RC_status = {
1: "^3Player ^5%s ",
2: "^3Skill:^7%s ",
4: "^3Istskill:^7%s ",
8: "^3Streak:^7%s ",
16: "^3Rounds:^7%s ",
32: "^3Reliability:^7%s ",
64: "^3Slot:^7%s ",
128: "^3Registered as:^7%s ",
256: "^3IP:^7%s ",
512: "^3Level:^2%s ",
1024: "^3Warning:^7%s ",
2048:" ^3Last visit: ^7%s ",
4096: "^3Alias:^7%s ",
8192: "^3from ^7%s",
}
