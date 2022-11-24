# dsr-fflogs-analyze
### dsr-phase.py
Pie chart of wipes by phase in DSR of your guild's logs

### dsr-mechanics.py
Table of frequency of wipes to each major mechanic 

**How it works**
Using the last cast of an ability in a fight, we can estimate where the wipe happened.
First does a query similar to that in dsr-phase.py to get fihgt and wipe phase info. Then for each log, queries events of major breakpoint abilities for each phase. The last breakpoint ability seen is the mechanic the group wiped on. 

**Issues and concerns**
- If the query for events in a particular phase for a log somehow surpasses 300 events, it will not get the next page. Will fix eventually but should only affect fresh proggers (lots of wipes in p2) or a really FAT log
- This script isn't 100% accurate, of course. E.G if party wipes to Wyrmhole but one person stays alive long enough to get to tethers, the script will count that as a wipe on the tethers.
- There may be counting issues if the party wipes before a breakpoint ability is casted as the phase rolls over. Depends on how FFLogs moves to the next phase
