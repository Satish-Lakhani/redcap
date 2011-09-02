#! /usr/bin/python
# -*- coding: utf-8 -*-

#IMPORTANT!: TRANSLATION TO OTHER LANGUAGE
#1) MAKE A COPY OF THIS FILE AND RENAME IT M_YOURLANGUAGE.PY
#2)TRANSLATE IN YOUR LANGUAGE THE SENTENCE ON THE RIGHT OF COLON (:)
#3)DO NOT MODIFY OR CANCEL THE %s VARIABLES!! DO NOT MODIFY ANYTHING OUTSIDE OF SENTENCES " " !!
#4)IN M_CONF.PY CHANGE THE VALUE OF RC_lang = "ITA" TO RC_lang = "YOURLANGUAGE"
#5)RESTART REDCAP

RC_outputs = {
"antirecon":"^2%s ^1kikkato per doppia connessione in meno di ^4%s",
"flood":"^2%s ^1kikkato per flooding",
"guidchange":"^2%s ^1kikkato per cambio GUID durante il gioco",
"insults":"^2Gli insulti non sono permessi. ^1Ancora %s volte e verrai kikkato",
"invalidguid":"^2%s ^1kikkato per GUID non regolare",
"invalidnick":"^2%s ^1kikkato per NICK non regolare",
"lownotoriety":"^2%s ^1kikkato per affidabilita troppo bassa: ^4%s2 ^2contro ^4%s3 ^2richiesta",
"nickchanges":"^2%s ^1kikkato per troppi cambi nick (%s)",
"nocleartarget":"^2Nick ambiguo. Riprova o usa lo slot ID",
"nolevel":"^2Comando di ^4livello %s. ^2Il tuo livello e' %s",
"notimetocmd":"^2Devi aspettare ancora ^4%s minuti ^2per chiamare questo comando",
"nuked":"^2Nuke lanciata su ^4%s",
"ora":"^2Sono le ^4%s",
"pwdset":"^2Password inserita. ^3Sara' attiva dal prossimo map load",
"record_alltime": "^6RECORD ASSOLUTO di ^4s%: ^6%s kills",
"record_monthly": "^6RECORD MENSILE di ^4s%: ^6%s kills",
"record_weekly": "^6RECORD SETTIMANALE di ^4s%: ^6%s kills",
"record_daily": "^6RECORD ODIERNO di ^4s%: ^6%s kills",
"record_personal": "^2Record personale di ^4s%: ^2%s kills",
"stillban": "^1%s, sei ancora bannato fino al ^6%s",
"tkill": "^1NO TEAMKILL! ^2Applicata penalita skill. ^4Livello warning: ^1%s ",
"voteON":"^2Il voto e' ora attivo per ^4%s ^2secondi",
"warning":"^2%s ^1kikkato per somma di warning",
"wrongcmd":"^3Comando non riconosciuto dal bot ^4RedCap",
}

RC_saluti = {
1: "^2Benvenuto ^4%s",
2: " ^2alias ^3%s",
4: " 2 ^2Skill: ^3%s",
8: " ^2Affidabilita: ^3%s",
16:" ^2Ultima visita: ^3%s",
}

RC_logoutputs = {
"command": "%s alias %s (lev:%s) ha usato: %s (lev:%s)",
}

RC_kills = {        #messaggi di killstreak
0 :"^4%s ^2ha fermato la serie di ^5%s",
1 :"",
2 :"",
3 :"",
4 : '^2 4 noobs? you can do better!',
5 : '^2 is warming up: ^15 ^2kills!',
6 : '^2 killed 6 enemies in a row',
7 : '^2 7 scalps? not bad!',
8 : '^2 are you camping? ^1(8 kills!)',
9 : '^2 9 kills. You are on fire!!',
10 : '^2 1^40 ^3K^4I^5L^6L^8S^9!! ',
11 : '^2 11 kills! You sure ain\'t a noob...',
12 : '^2 12 kills...aimbot or wallhack?',
13 : '^2 13 kills? ^1You are a PRO!',
14 : '^2 14 kills? kills? someone kill him!',
15 : '^2 15 kills? are you Kabal?!',
16 : '^2 16 kills? 16 kills? one more and i\'ll kick you!!',
17 : '^2 17 kills? I was kidding!',
18 : '^2 18 ^1You are more pro than before!',
19 : '^2 19 kills! Are you playing against fools!?!?',
20 : '^2 20 ^3KILLS^4!^5!^6!',
21 : '^1 21 kills...i can\'t believe it! :-(',
22 : '^1 22 kills? 1337!',
23 : '^2 23 kill? ^4ok guys, John Rambo is here',
24 : '^2 24 corpses... ^4bigger massacre than waco!',
25 : '^2Kill counter is OVER! ^3U^4N^6B^1E^7L^8I^9E^0V^1A^3B^5L^2E^6!',
}
