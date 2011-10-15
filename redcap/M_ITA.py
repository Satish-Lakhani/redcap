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
"adminrights": "^2Assegnato livello admin a %s",
"alias": "^2Alias di %s:^3",
"antirecon": "^2%s ^1kikkato per doppia connessione in meno di ^4%s",
"balanceauto":"^1Non necessario: ^2il bilanciamento avviene in ^4AUTOMATICO ^2all'inizio di ogni round",
"balancexecuted": "^2Bilanciamento effettuato.",
"balancemanual": "^2Il bilanciamento verra' effettuato ^4se necessario ^2a inizio round",
"balancemode": "^2Bilanciamento teams ^4%s",
"balancenoneed": "^2Teams equivalenti. Chiedere eventualmente lo shuffle ad un admin",
"balanceoff":"^2La funzione bilanciamento non e' attiva. Usare il comando ^4!ab ^2 per attivarla",
"ban": "^1La presenza di ^4%s ^1non e' piu' gradita su questo server",
"bestplayers": "^2Migliori player:",
"caricoplayer": "^2Caricati i dati di ^4%s da DB",
"dbnick":"^2Assegnato ^4%s ^2come nick principale",
"mapskill": " ^4%s^2 skill di mappa: ^5%s",
"executed": "^2Comando ^4%s ^2eseguito",
"flood": "^2%s ^1kikkato per flooding",
"guidchange": "^2%s ^1kikkato per cambio GUID durante il gioco",
"headshot": "^4%s ^2%s HS (^4%s ^2o/o)",
"insults": "^2Gli insulti non sono permessi. ^1Ancora %s volte e verrai kikkato",
"invalidguid": "^2%s ^1kikkato per GUID non regolare",
"invalidnick": "^2%s ^1kikkato per NICK non regolare",
"levassigned":"^2Assegnato livello ^4%s ^2a ^4%s.",
"lownotoriety": "^2%s ^1kikkato per affidabilita troppo bassa: ^4%s2 ^2contro ^4%s3 ^2richiesta",
"muteall": "^1Muto/Smuto ^2tutti!",
"muted":"^4%s ^2mutato in quanto era mutato all'ultima disconnessione",
"nextmap": "^2Prossima mappa: ^4%s",
"nickchanges": "^2%s ^1kikkato per troppi cambi nick (%s)",
"noavailcmd": "^2Comando non disponibile in fase di avvio.",
"noclearcfg": "^2Configurazione ambigua o inesistente.",
"nocleartarget": "^2Nick ambiguo. Riprova o usa lo slot ID",
"noclearmap": "^2Mappa ambigua o inesistente. Riprova o usa ^4!cmd nomemappa",
"nolevel": "^2Comando di ^4livello %s. ^2Il tuo livello e' %s",
"notimefromini": "^1Non puoi chiamare un voto nei primi 60 secondi della mappa",
"notimetocmd": "^2Devi aspettare ancora ^4%s minuti ^2per chiamare questo comando",
"nuked": "^2Nuke lanciata su ^4%s ^2da ^4%s",
"ora": "^2Sono le ^4%s",
"pwdset": "^2Password inserita. ^4Sara' attiva dal prossimo map load",
"record_alltime": "^6RECORD ASSOLUTO di ^4%s ^6%s kills",
"record_daily": "^6RECORD ODIERNO di ^4s% ^6%s kills",
"record_monthly": "^6RECORD MENSILE di ^4%s ^6%s kills",
"record_no_not": "^4%s, ^2Affidabilita troppo bassa per validare un record",
"record_no_ppl": "^2meno di ^4%s ^2persone in game. Record di  ^4%s ^2non convalidato",
"record_personal": "^2Record personale di ^4%s ^6%s kills",
"record_weekly": "^6RECORD SETTIMANALE di ^4%s ^6%s kills",
"restart": "^1 Riavvio RedCap...",
"salvoplayer": "^2Salvo i dati di ^4%s",
"skill": "^2Skill: ^4%s ^2Instantanea: ^4%s ^2Streak: ^4%s ",
"space":"^2Slots pieni. Spettatore ^4%s ^kikkato.",
"spamadded":"^2Frase aggiunta",
"spamerased":"^2Frase cancellata",
"spamnotfound":"^1Frase non trovata",
"startup":"^2RedCap in fase di avvio",
"startupend": "^2Fase di avvio terminata. ^4RedCap operativo",
"stillban": "^1%s, sei ancora bannato fino al ^6%s",
"suicide": "^1Suicidio: ^2penalizzazione di ^1%s ^2punti skill",
"tempban": "^1%s bannato per ore ^4%s",
"tempbanmax": "^2Il massimo ban temporaneo e' di ore ^4%s",
"thit": "^1NO TEAMHITS! ^2Applicata penalita skill. ^4Livello warning ^1%s ",
"tkill": "^1NO TEAMKILL! ^2Applicata penalita skill. ^4Livello warning ^1%s ",
"toohighlevel":"^1Non puoi assegnare livelli superiori al tuo che e' ^4%s",
"top": "^6%s: ^4%s ^5%s ^6il %s",
"voteON":"^2Il voto e' ora attivo per ^4%s ^2secondi",
"warbaseloaded" : "^5Modalita war. ^2Carico %s ...",
"warloaded": "^5Modalita' WAR. ^2Carico %s ...",
"warning":"^2%s ^1kikkato per somma di warning",
"warunloaded": "^5Fine WAR. ^2Ricarico %s ...",
"wrongcmd":"^1Comando non riconosciuto dal bot ^4RedCap",
}

RC_kills = {        #messaggi di killstreak
0 :"^4%s ^2ha fermato la serie di ^5%s",
1 :"",
2 :"",
3 :"",
4 : '^4%s^2 e\' in forma...',
5 : '^4%s^2 si sta scaldando: ^15 ^2kills!',
6 : '^2 ci sono sei nuove vedove grazie a ^4%s ',
7 : '^4%s^2 7 kill? Non male!',
8 : '^2Ottava kill per^4%s, ^2stara\' camperando?',
9 : '^4%s^2 9 kills. Record in vista?',
10 : '^4%s^2 1^40 ^3K^4I^5L^6L^8S^9!! ',
11 : '^4%s^2 11 kills! Non sei un noob...',
12 : '^4%s^2 12 kills...aimbot or wallhack?',
13 : '^4%s^2 13 kills? ^1Attenzione c\'e\' un PRO in game!',
14 : '^2 14 kills? Fermate il soldato ^4%s!',
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
128: "^2Registrato:^4%s ",
256: "^2IP:^5%s ",
512: "^2Level:^5%s ",
1024: "^2Warning:^7%s ",
2048:" ^2Ultima visita: ^3%s ",
4096: "^2Alias:^1%s ",
}
