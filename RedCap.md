[<back to homepage](http://code.google.com/p/redcap/)
# RedCap requirements #
_if your server do not comply requirements 1, 2, 3, it will be **not** possible to run RedCap unless your server Provider install it for you._

  1. <font color='red'>Python >2.5 installed on the server (It is standard on Linux based gameserver, to be verified on Windows based server)</font>
  1. <font color='red'>Remote FTP access to the server</font>
  1. <font color='red'>Possibility to remote start a script on the game server, or at least to modify the existing script starting Urban Terror.</font>
  1. Console remote access to the game server (ssh type) is **not** a must but it helps a lot.
  1. **No** need of MySQL

# Features list #
_Most of these features are customizable and can be switched on or off._

  * Exhaustive chat command set with **40 different commands** (See [full command list](RedCap_User_guide.md)).
  * **Fully customizable configuration file** (See [full configuration guide](RedCap_config_file.md)).
  * **Anticheat log control**: RedCap kicks for bad guid, in game guid change, nick rotation hack. In case of automatic kick IP and GUID are recorded in a separate log file for further use.
  * **Webranking and stats** with automatic FTP transfer on your clan website as full HTML document or HTML table
  * Use authorization level individually customizable for each command.
  * Command use recording in a separate log file for further use.
  * Possibility to use all rcon commands from game chat through !cmd`<_cmd_>`
  * Automatic (or manual) **team balance**.
  * Player IP geolocalization at City level
  * Anti fake system (every new fake costs one half of player reliability)
  * Anti flooding control (fully customizable).
  * Automatic daily maintenance (DB cleaning, gameserver restart, files backup, etc...)
  * Irregular nicknames control (customizable through a [regexp](http://en.wikipedia.org/wiki/Regular_expression))
  * **Bad words censoring** (customizable through a [regexp](http://en.wikipedia.org/wiki/Regular_expression) list)
  * Player **skill calculation system based on statistic** kill expectancy, opponent skill and opposite team mean skill.
  * General player stats showing skill, killstreak, hit distribution and more...
  * IP recording in stats.
  * Player alias recording in stats.
  * Player temporary ban and enforced ban by IP and GUID
  * Access control to gameserver based on player reliability (customizable)
  * Anti reconnection system.
  * One command **switch to and from CW mode** with possibility to load different configuration files. RedCap stops every visible activity during CW.
  * Possibility to manage (create, delete, list) spam messages directly from game chat.
  * Spectator auto kick when gameserver is full.
  * Automatic or manual warnings for bad behaviours (teamkills, teamhits, offensive language, etc). Automatic kick at max warning level overtaking.
  * DB Maintenance: automatic clean of unused guids
  * DB Maintenance: automatic clean of older alias when more than maxAlias
  * DB Maintenance: automatic daily compression by VACUUM statement to keep DB size as small as possible.
  * **NO automatic ban**. Ban is the heaviest in game penalty, then RedCap philosophy is to leave this decision to an human admin.

Sample of remote webrank:
![http://www.bravewarriors.eu/EXT_IMG/stats.png](http://www.bravewarriors.eu/EXT_IMG/stats.png)

# TO DO List #
  1. ~~Player geolocalization~~
  1. Player identification after IP and GUID change (euristic)
  1. IrC integration
  1. ~~Forgive commands.~~
  1. ~~Silent mode~~
  1. Web interface for RedCap configuration.
  1. Granular gameserver allowed weapon choice
  1. Complete the optimization for modes other than Team Survivor (IN PROGRESS)
  1. Language localization other than ENG and ITA (you are welcome ;))
  1. ~~UrT 4.2 update~~

# Credits & Licence #
RedCap has been developed from scratch by bw|Lebbra! **NO copy and paste from other sources!**

Download and use of RedCap is free of charge for non-commercial use under GNU/GPL 2

Copyright (C) 2012 Alessandro Verdoni

_This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License._

_This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details._

_You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA._