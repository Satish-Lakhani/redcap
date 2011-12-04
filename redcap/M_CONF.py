#! /usr/bin/python
# -*- coding: utf-8 -*-

### =======================================================================  ###
### THESE PARAMETERS ***MUST*** BE CONFIGURED OR REDCAP WILL NOT RUN PROPERLY!!!   ###
### =======================================================================  ###

NomeFileLog = "../games.log"    				#Relative path of gameserver log
AdminGuids = ["****************************"] 	#Guid in this field is automatically enabled to the highest admin level (level 100)
SV_Baseconf = "server.cfg"  					#Name of gameserver base config file.
SV_UrtPath = "../../../q3ut4"    				#Relative path of Urban Terror  q3ut4 folder
SV_MapCycle =  "mapcycle.txt"    				#Name of cyclemap config file
Sck_ServerRcon = "********"   					#Gameserver rcon password
Sck_ServerIP =  "***.***.***.***"      			#Gameserver IP address
Sck_ServerPort = 27960 							#Gameserver IP port

### =============================================================================================  ###
### THESE PARAMETERS **MUST** BE CONFIGURED IF  *** Website_ON = True *** OR REDCAP WILL NOT RUN PROPERLY!!!   ###
### =============================================================================================  ###

Website_ON = False 							#(True or False) True if you want to use RedCap web features (rank and chatlog  FTP transfer to auxiliary website)
w_url = 'www.yoursite.com'      			#FTP url of auxiliary website
w_login = '*******' 						#FTP login of auxiliary website
w_password = '********' 					#FTP password of auxiliary website
w_ftp_directory = '/httpdocs/serverstats' 	#Remote relative path of folder used by RedCap for FTP transfer
w_directory = '/serverstats' 				#Remote relative url of folder used by RedCap for FTP transfer
w_tabella = "skilltable.htm"                #Ranking table (html format)
w_dialoghi = "dialoghi.htm"                 #Chat log table (html format)

### ==================================================================  ###
### THESE PARAMETERS *CAN* BE CONFIGURED IN ORDER TO CUSTOMIZE YOUR REDCAP   ###
### ==================================================================  ###
#PLAYER
KickForSpace = True 			#(True or False) If True RedCap kicks a spect when gameserver is full. Admins cannot be kicked.
maxSlap = 10 					#Max. slap number to be used with !s[num] command. If num > 10 then num = 10.
Ttempban = 96 					#Max duration of a temporary ban (hours)

#RECORD
MinPlayers = 4 					#Min. number of active players for registering a record
MinNotoriety = 0 				#Min. notoriety level required to a player for registering a record

#CONSOLE SPAMS
RecordSpam = True 				#(True or False) If True, Redcap periodically spams records in chat
CustomSpam = True 				#(True or False) If True, Redcap periodically spams sentences stored in spam.txt,
Spamtime = 140 					#Time between two consecutive spams

#REDCAP
botname = "^8RC| " 				#prefix of Redcap outputs (#TODO not used yet)
clanbalanceTag = "bw|"			#prefix of Home clan
RC_lang = "ITA" 				#Language localization for RedCap. ITA only #TODO (ENG FRA and others. See M_ITA.py for translation procedure)
gameserver_autorestart = 2 		#Automatically restart the Gameserver: 0: no restart 1: daily restart 2: restart when empty.

##SERVER
SV_AliasDuration = 90      		#How long (days) a player alias is hold on by RedCap before it is removed because unused
SV_AntiReconInterval = 0    	#Anti reconnect delay in sec. If SV_AntiReconInterval = X a player cannot reconnect to the game server before X seconds from the first connect.
SV_BalanceMode = 2          	#Team balance mode 0: disabled, 1: manually enabled (to be called by !tm command),  2: automatic balance when a team has 2 players more than the other one.
SV_FloodControl = True     		#(True or False) If True, Redcap will kick players that spams more than SV_MaxFlood chat lines in less then15 sec.
SV_MaxFlood = 6    				#Max number of chat lines in 15 sec. Active only when SV_FloodControl = True
SV_MaxNickChanges = 3    		#Max nick changes in 15 sec.
SV_goodNick = r"[a-zA-Z]"   	#Regex that player nick must satisfy to be allowed to play in the game server.
SV_minNick = 3   				#Min length allowed for a player nick
SV_ShowHeadshots = True  		#(True or False) If True headshot are displayed in upper gameserver chat

##STATUS Sum the values of each information you want to be shown
'''
1: Welcome %nick
2: Skill
4: Map skill
8: Highest streak
16: Played rounds
32: Reliability
64: Player slot number
128: Official nick
256: IP
512: Player level
1024: Received warnings
2048: Players last visit
4096: Players alias
'''
saluti = 1 + 2048 													#Information shown at player connection
status = 1 + 32 + 128 + 1024 + 2048 								#Information about player given to everybody
status_adm = 1 + 8 + 16 + 32 + 64 + 128 + 256 + 512 + 2048 + 1024 	#Information about player given to  the admins

#SKILL
Sk_penalty = 4   			#Teamkill penalty: it represents the number of additional kill you should gain in order to nullify the penalty.
Sk_Ks_min = 5    			#(not used)
Sk_Ks_not = 0    			#Kill streaks made by players with lower notoriety than this are not spammed.
Sk_Ks_show = 5   			#Kill streaks shorter than this are not spammed by RedCap.
Sk_Ks_showbig = 9 			#Kill streaks longer than this are spammed by RedCap in bigtext.

##VOTO
voteTime = 30 				#How long (seconds) vote mode is enabled
voteType =536870986 		#Temporary vote mode (see http://www.urbanterror.info/docs/texts/123/#2.2 for value meaning)
unvoteType = 0 				#Standard vote mode. 0 means no vote allowed (see http://www.urbanterror.info/docs/texts/123/#2.2 for value meaning).
timeBetweenVote = 3 		#Time to elapse (minutes) before temporary mode could be enabled again.
Tcyclemap = 12 				#Time to elapse (minutes) between two cyclemap

##WARNING
W_max_warns = 5.0   		#Warning level to be kicked. (warning can be assigned by RedCap or Admins)
W_adm_warn = 1.0    		#Value of a warning assigned by a Admin (TODO: Not used yet)
W_tk_warn = 1.0        		#Value of a warning caused by a teamkill
W_hit_warn = 0.3       		#Value of a warning caused by a teamhit

##MISCELLANEOUS
commandlogMinLevel = 2 		#All the commands with level equal or above this value are recorded in command log.
Control_Daily = 6 			#Hour (0-24) when daily maintenance activities will start
Nt_MinNot_toplay = 0.55 	#Min. notoriety  to play in the gameserver. New player's notoriety is 0
w_minRounds = 60 			#Rounds to play before a player is shown in webrank
#maxAbsence = 25 			# giorni di assenza prima di essere cancellati dal server

#COMMANDS LEVEL (Max lev = 100). Player can execute all the commands having a level lower or equal to their own level. Redcap automatically assign level 0 to each new player, unless a different level has been assigned by some admin.:
lev_alias = 1 				#Shows player's alias
lev_admin = 1 				#All the players having this level or higher are considered gameserver admins. Admins receives more detailed information about other players. Presence of an admin could enable or disable some Redcap features.
lev_balancemode = 2 		#Switches team autobalance ON/MANUAL/OFF
lev_balance = 0 			#Ask to RedCap for a teambalance at round end
lev_ban = 3 				#Permanently bans a player
lev_callvote = 1 			#Enables vote mode "voteType" for "voteTime" seconds.
lev_cycle = 2 				#Cycles immediately to the next map
lev_dbnick = 3 				#Set the actual player's nick as his main nick. Main nick is the one displayed in records and webrank
lev_esegui = 4 				#Executes an rcon command
lev_force = 2 				#Moves a player to Red, Blue or Spect
lev_info = 0 				#Shows some info about game server and RedCap itself
lev_kick = 1 				#Kicks a player
lev_level = 4 				#Assign a level to a player
lev_map = 1 				#Loads a new map
lev_maplist = 1 			#Shows a list of all the maps availables on the gameserver
lev_mute = 1 				#mute a player
lev_muteall = 2 			#mute all the players in game
lev_notoriety = 2 			#Changes the min. reliability level required to play on the gameserver
lev_nuke = 2 				#nukes a player
lev_ora = 0 				#Shows server time
lev_password = 1 			#Sets a password on the game server
lev_RCrestart = 4 			#Restart the RedCap
lev_skill = 0 				#Shows plasyer's skill
lev_slap = 1 				#Slaps a player n times
lev_spam = 2 				#adds / cancels a message from spam list
lev_spamlist = 0 			#Lists all spam messages
lev_status = 0 				#Gives several details about player(s). Details depends from applicant level
lev_tmpban = 1 				#Temporary ban
lev_top = 0 				#Shows top records
lev_trust = 3 				#Increases or decreases player's reliability level
lev_war = 1 				#Loads a CW config and set the gameserver in war mode
lev_unwar = 1 				#Unload war mode setting the game server to its standard configuration

### ================================================================================================================  ###
### THESE PARAMETERS ***MUST NOT*** BE CHANGED UNLESS YOU EXACTLY KNOW WHAT ARE YOU DOING OR REDCAP WILL NOT RUN PROPERLY!!!   ###
### ================================================================================================================  ###

versione = "1.00 Beta(20111211)" 	#RedCap Version. !!! PLEASE ADD "-MOD by YOURNAME" TO THE VERSION NUMBER IF YOU MODIFY SOMETHING OF THE SCRIPT OUTSIDE OF THIS CONFIGURATION FILE. !!!

##AUXILIARY FILES and LOGS
badguid = "badguid.log" 	#Bad guids record file
crashlog = "crash.log" 		#RedCap activity and crashes logfile
commandlog = "command.log" 	#RedCap commands record file (commandlogMinLevel value specify which command should be recorded into the file)
NomeArchivi = "Archivi" 	#Gamelogs and database backup folder
NomeDB = "Rc_DB.sqlite" 	#name of DB file
socketlog = "socket.log" 	#Not sent command logfile
SpamFile = "spam.txt"   	#Custom spams here
SV_Basewar = "basewar.cfg"  #Basic CW config that RedCap loads if nothing else is specified
SV_Logfolder = "logs"   	#Log folder

##NOTORIETY:  If player notoriety is lower than Nt_MinNot_toplay, the player is immediately kicked from gameserver.
Nt_badguid = -20    		#Notoriety penalty for bad formatted guid
Nt_dayXpoint = 5    		#Guid age (days) giving 1 notoriety point
Nt_floodpenalty = -0.2  	#Notoriety penalty for flooding
Nt_guidchange = -50 		#Notoriety penalty for guid change in game
Nt_roundXpoint = 200    	#N. of round to be played giving 1 notoriety point
Nt_warnpenalty = -1 		#Notoriety penalty for a kick from RedCap

##SKILL parameters
#EXAMPLE: appoximative score that a 1000 skill player should obtain to keep his skill unchanged:
#Sk_range=300: score: 785-1;
#Sk_range=500: score 55-1;
#Sk_range=600: score 28-1;
#Sk_range=700: score 17-1;
#Sk_range=800: score 12-1;
#Sk_range=900: score 9-1;
#Sk_range=1000: score 7-1;
#Sk_range=3000: score 2-1;

Sk_team_impact = 0.3     	#Part of skill variation based on opponent team mean skill. (Remaining is based on direct opponent's skill)
Sk_Kpp = 5   				#N. of times you should kill an equivalent skilled opponent to gain 1 skill point.
Sk_range = 800   			#Theoric skill ceil value.

## SOCKET
Sck_ServerTimeout = 1   	#Waiting time for an answer from gameserver (sec)
Sck_Tsleep = 0.8     		#Delay between two consecutive rcon commands (sec)
Sck_ServerLog =  SV_Logfolder + "/" + socketlog #Path to socketlog

##TEMPI
CRON1 = 15 					#Cron1 frequency in seconds (fast timer)
CRON2 = 3600 				#Cron2 frequency in seconds (slow timer)
TempoCiclo = 0.5 			#Gameserver log control frequency in seconds

#SERVIZIO
GameServerDown = 20 		#Waiting time before considering gameserver down (not used)
