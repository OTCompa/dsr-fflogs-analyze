# dsr-fflogs-analyze
To use, you need to edit the *client_id*, *client_secret*, and *guild_id* in the script. You can create a client_id and client_secret here: https://www.fflogs.com/api/clients/
### dsr-phase.py
Pie chart of wipes by phase in DSR of your guild's logs.  

### dsr-mechanics.py
Table of frequency of wipes to each major mechanic.  
Not completely finished but good enough. May decide to complete it one day.  
Cost about 200-300 FFLogs API points and took 2-3 minutes to make all the queries for me. YMMV  
**How it works**  
Using the last cast of an ability in a fight, we can estimate where the wipe happened.  
First does a query similar to that in dsr-phase.py to get fihgt and wipe phase info. Then for each log, queries events of major breakpoint abilities for each phase. The last breakpoint ability seen is the mechanic the group wiped on. 

**Issues and concerns**
- If your group has a massive amount of logs, the first query may be incomplete. I don't have a guild that has that many logs, so it's a non-issue for me :)
- If the query for events in a particular phase for a log somehow surpasses 300 events, it will not get the next page. Will fix eventually but should only affect fresh proggers (lots of wipes in p2) or a really FAT log
- This script isn't 100% accurate, of course. E.G if party wipes to Wyrmhole but one person stays alive long enough to get to tethers, the script will count that as a wipe on the tethers.
- There may be counting issues if the party wipes before a breakpoint ability is casted as the phase rolls over. Depends on how FFLogs moves to the next phase
