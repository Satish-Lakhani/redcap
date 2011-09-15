#! /usr/bin/python
# -*- coding: utf-8 -*-

#IMPORTANT!: TRANSLATION TO OTHER LANGUAGE
#1) MAKE A COPY OF THIS FILE AND RENAME IT "M_YOURLANGUAGE.PY"
#2)TRANSLATE INTO YOUR LANGUAGE THE SENTENCE ON THE RIGHT SIDE OF COLON (:) - USE ASCII 128 ONLY.
#3)DO NOT MODIFY OR CANCEL THE %s VARIABLES!! DO NOT MODIFY ANYTHING OUTSIDE OF SENTENCES " " !!
#4)IN "M_CONF.PY" CHANGE THE VALUE OF RC_lang = "ITA" TO RC_lang = "YOURLANGUAGE"
#5)RESTART REDCAP

RC_outputs = {
"accident":"^4%s ^2non ha fatto attenzione e si e' ammazzato da solo",
"antirecon": "^2%s ^1kikkato per doppia connessione in meno di ^4%s",
"balanceauto":"^2Il bilanciamento avviene in ^4AUTOMATICO ^2all'inizio di ogni round",
"balancexecuted": "^2Bilanciamento effettuato.",
"balancemanual": "^2Il bilanciamento verra' effettuato ^4se necessario ^2a inizio round",
"balancemode": "^2Bilanciamento teams %s",
"balancenoneed": "^Teams equivalenti. Chiedere eventualmente lo shuffle ad un admin",
"balanceoff":"La funzione bilanciamento non e' attiva. Usare il comando ^4!ab ^2 per attivarla",
"ban": "^1La presenza di ^4%s ^1non e' piu' gradita su questo server",
"bestplayers": "^2Migliori player:",
"mapskill": " ^4%s^2 skill di mappa: ^5%s",
"executed": "^2Comando ^4%s ^2eseguito",
"flood": "^2%s ^1kikkato per flooding",
"guidchange": "^2%s ^1kikkato per cambio GUID durante il gioco",
"insults": "^2Gli insulti non sono permessi. ^1Ancora %s volte e verrai kikkato",
"invalidguid": "^2%s ^1kikkato per GUID non regolare",
"invalidnick": "^2%s ^1kikkato per NICK non regolare",
"levassigned":"^2Assegnato livello ^4%s ^2a ^4%s.",
"lownotoriety": "^2%s ^1kikkato per affidabilita troppo bassa: ^4%s2 ^2contro ^4%s3 ^2richiesta",
"muteall": "^1SILENZIO, ^2per favore!",
"muted":"^4%s ^2mutato in quanto era mutato all'ultima disconnessione",
"nickchanges": "^2%s ^1kikkato per troppi cambi nick (%s)",
"nocleartarget": "^2Nick ambiguo. Riprova o usa lo slot ID",
"nolevel": "^2Comando di ^4livello %s. ^2Il tuo livello e' %s",
"notimetocmd": "^2Devi aspettare ancora ^4%s minuti ^2per chiamare questo comando",
"nuked": "^2Nuke lanciata su ^4%s ^2da ^4%s",
"ora": "^2Sono le ^4%s",
"pwdset": "^2Password inserita. ^3Sara' attiva dal prossimo map load",
"record_alltime": "^6RECORD ASSOLUTO di ^4%s ^6%s kills",
"record_monthly": "^6RECORD MENSILE di ^4%s ^6%s kills",
"record_weekly": "^6RECORD SETTIMANALE di ^4%s ^6%s kills",
"record_daily": "^6RECORD ODIERNO di ^4s% ^6%s kills",
"record_personal": "^2Record personale di ^4%s ^6%s kills",
"skill": "^2Skill: ^4%s ^2Instantanea: ^4%s",
"space":"^2Slots pieni. Spettatore ^4%s ^kikkato.",
"startup":"^2RedCap in fase di avvio",
"startupend": "^2Fase di avvio terminata. ^4RedCap operativo",
"stillban": "^1%s, sei ancora bannato fino al ^6%s",
"suicide": "^1Suicidio: ^2penalizzazione di ^1%s ^2punti skill",
"tempban": "^1%s bannato per ore ^4%s",
"tempbanmax": "^2Il massimo ban temporaneo e' di ore ^4%s",
"thit": "^1NO TEAMHITS! ^2Applicata penalita skill. ^4Livello warning ^1%s ",
"tkill": "^1NO TEAMKILL! ^2Applicata penalita skill. ^4Livello warning ^1%s ",
"toohighlevel":"^1Non puoi assegnare livelli superiori al tuo che e' ^4%s",
"voteON":"^2Il voto e' ora attivo per ^4%s ^2secondi",
"warning":"^2%s ^1kikkato per somma di warning",
"wrongcmd":"^3Comando non riconosciuto dal bot ^4RedCap",
}

RC_kills = {        #messaggi di killstreak
0 :"^4%s ^2ha fermato la serie di ^5%s",
1 :"",
2 :"",
3 :"",
4 : '^4%s^2 4 noobs? you can do better!',
5 : '^4%s^2 is warming up: ^15 ^2kills!',
6 : '^4%s^2 killed 6 enemies in a row',
7 : '^4%s^2 7 scalps? not bad!',
8 : '^4%s^2 are you camping? ^1(8 kills!)',
9 : '^4%s^2 9 kills. You are on fire!!',
10 : '^4%s^2 1^40 ^3K^4I^5L^6L^8S^9!! ',
11 : '^4%s^2 11 kills! You sure ain\'t a noob...',
12 : '^4%s^2 12 kills...aimbot or wallhack?',
13 : '^4%s^2 13 kills? ^1You are a PRO!',
14 : '^4%s^2 14 kills? kills? someone kill him!',
15 : '^4%s^2 15 kills? are you Kabal?!',
16 : '^4%s^2 16 kills? 16 kills? one more and i\'ll kick you!!',
17 : '^4%s^2 17 kills? I was kidding!',
18 : '^4%s^2 18 ^1You are more pro than before!',
19 : '^4%s^2 19 kills! Are you playing against fools!?!?',
20 : '^4%s^2 20 ^3KILLS^4!^5!^6!',
21 : '^4%s^2 21 kills...i can\'t believe it! :-(',
22 : '^4%s^2 22 kills? 1337!',
23 : '^4%s^2 23 kill? ^4ok guys, John Rambo is here',
24 : '^4%s^2 24 corpses... ^4bigger massacre than waco!',
25 : '^4%s^2Kill counter is OVER! ^3U^4N^6B^1E^7L^8I^9E^0V^1A^3B^5L^2E^6!',
}

RC_logoutputs = {
"command": "%s alias %s (lev:%s) ha usato: %s (lev:%s)",
}

RC_status = {
1: "^2Player ^4%s ",
2: "^2Skill:^5%s ",
4: "^2Istskill:^5%s ",
8: "^2Streak:^5%s ",
16: "^2Rounds:^5%s ",
32: "^2Affidabilita:^5%s ",
64: "^2Slot:^5%s ",
128: "Registrato:^4%s ",
256: "^2IP:^5%s ",
512: "^2Level:^5%s ",
1024: "^2Alias:^7%s ",
2048:" ^2Ultima visita: ^3%s ",
4096: "^2Warning:^1%s ",
}
