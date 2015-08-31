[<back to homepage](http://code.google.com/p/redcap/)
# REDCAP USER GUIDE #

## Preface ##

**RedCap** bot is a python script aimed to manage Urban Terror gameservers from chat line. Features includes a wide range of user commands and a lot of automatic features. Most of them can be enabled/disabled from config file.

## Commands ##
All !Redcap commands starts with **!**, someone of them accepts one or more parameters.
Not all the commands are available to everybody. An appropriate level can be assigned to each command from config file.

## Commands syntax ##
**!example**   it is the command itself

**`[r,b,s]`**   parameters choice

**`<target>`**   mandatory parameter to be replaced with target player name or some other specified value.

## Command list ##
  * **!al `<target>`** : List all the alias previously used by the player.

  * **!ab** : Cycle balance mode between AUTO/MAN/OFF/CLAN.
    * _**AUTO**_ balance is automatically executed at round end if needed.
    * _**MAN**_ balance is executed at round end if previously called by **!tm** or **!teams** command.
    * _**OFF**_  means no balance is allowed.
    * _**CLAN**_ means that all players belonging to home clan will be grouped toghether (if possible keeping teams even, of course).

  * **!ban `<target>`** : Permanently ban the target player by IP and GUID.

  * **!cmd `<cmd>`** : Same as "_\rcon_". It can execute whatsoever command _cmd_ a rcon owner could execute into the game console. <font color='red'> NOTE: be careful to assign an appropriate level to this command in config file.</font>

  * **!cy** : Immediately cycle to the next map.

  * **!dbnick `<target>`** : Set the actual nickname as main nickname for the target player.

  * **!f`<team>``[rbs]` `<target>`** : Forces the target player to join the specified team (ex: _**!fr joh**_ will force player johnny to join red team).

  * **!fall `<target>`** : All the kills or hits did by _target_ to everybody are forgiven _(Suggested level: Admin or trusted player)_.

  * **!find `<target>`** : Find _target_ in DB and shows info (as _target_ you can also use part of a nick ans RedCap will return up to 4 different records).

  * **!fp `[target]`** : You forgive all the kills or hits did by _target_ to you. If _target_ is missed you forgive all the players in game for kills or hits did by _everybody_ to you.

  * **!info** or **!help** : give some information about !Redcap itself and the gameserver.

  * **!kk `<target>`** : kick the target player from gameserver

  * **!lev`<num>` `<target>`** : Assigns the level _num_ to the target player. <font color='red'> NOTE: be careful to assign an appropriate level to this command in config file.</font>

  * **!map`<map>`** : Immediately loads the specified map. _map_ must be a valid map name or part of it.

  * **!maplist** : List all the maps available on the gameserver.

  * **!m `<target>`** : mute the target player. If a player quits before map end, he will be muted again when reconnects.

  * **!mall** : mute all the players. If a player quits before map end, he will be muted again when reconnects.

  * **!notoriety`<num>`** : Sets the lowest notoriety needed to play on the gameserver. All the players with a notoriety lower than _num_ will be kicked. When RedCap restarts, notoriety will be set again to the value specified into the config file.

  * **!n `<target>`** : nuke the target player.

  * **!ora** : displays actual gameserver time.

  * **!pwd`<pwd>`** : set a password on the gameserver. To unset the password just type **!pwd**

  * **!rere`<record>`** : Delete one or all the records. Targets can be: "_day_", "_week_", "_month_", "_alltime_", "_all_"

  * **!restart** : restart RedCap bot. Useful to reload config after some change.

  * **!s`[num]` `<target>`** : slaps _num_ times the target player. If no _num_ is specified it slaps one time.

  * **!silent** : For those admins that unlike spam it toggles silent mode ON/OFF (just new records, kick and ban are spammed).

  * **!sk `[target]`** : displays skill information about target player. If no target is specified, applicant skill will be displayed.

  * **!smite `<target>`** : Instantly kill the target _(Suggested level: Admin or trusted player)_.

  * **!spam `<text>`** : add the text _text_ to the spamlist (you can use `^1 - ^`9 for colours).

  * **!spamlist** : lists all the spam MESSAGES saved in RedCap memory.

  * **!tban`<num>` `<target>`** : Temporarily bans the target player by GUID for _num_ hours. An upper limit for _num_ can be set in config file.

  * **!top** : display alltime, monthly, weekly and daily kill records.

  * **!tm** or **!teams** : Ask for a automatic balance at round end. It works only if autobalance mode is MAN. _NOTE: Balance is executed at round end in TS mode and immediately in CTF or TDM modes_.

  * **!trust`[num]` `<target>`** : increase target player notoriety by _num_. Useful to allow a player to immediately enter onto the gameserver even if he has a fresh guid.

  * **!unban `<ID>`** : Unban the player ID (even if not in game). Use _**!find**_ command to found player ID in database and unban him.

  * **!unspam `<num>`** : delete the sentence number _num_ from spamlist.

  * **!untrust`[num]` `<target>`** : decrease target player notoriety by _num_. If notoriety decreases under the min level allowed on the gamserver, the player will be kicked.

  * **!unwar** : unsets warmode and reloads the standard gameserver config file.

  * **!v** : Enable vote for _X_ seconds. When vote is enabled vote mode is changed to "_voteType_" instead to "_unvoteType_". X, voteType and unvoteType can be set in config file.

  * **!war`[cfg]`** : set the gameserver in matchmode loading the specifide configuration file. _cfg_ can be a valid config name or part of it. If no _cfg_ is specified. RedCap will use its own standard war config file (similar to Urban Zone TS config file). Once the server remains empty for a few seconds, the warmode will be unset and normal server config reloaded. You can also unset warmode using _**!unwar**_ command.

  * **!z `[target]`** : displays some info about target player. Different detail level can be set in config file for normal players and admins. If no target is specified RedCap will show information (lesser detail) about all the players in game.