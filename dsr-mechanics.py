import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
#import matplotlib.pyplot as plt
#import numpy as np
import pandas as pd
from enum import IntEnum

# input your stuff here
client_id = r'your-client-id-here'
client_secret = r'your-client-secret-here'
guild_id = 1337

# TODO: add the rest of p1
# TODO: add check for mechanics with no unique casts
phase_ability_ids = [
    # phase 1
    {
        25300: "holiest of holy"
    },

    # phase 2
    {
        25555: "strength",
        25569: "sanctity",
        25533: "ultimate end",
        25539: "thordan enrage"
    },

    # phase 3
    {
        26376: "final chorus",
        26381: "wyrmhole",
        26396: "soul tether",
        29750: "nidhogg enrage"
    },

    # phase 4
    {
        29050: "eyes beginning",
        26817: "orbs",
        26819: "dives",
        26813: "steep in rage",
        26402: "eyes enrage"
    },

    # intermission 1
    {
        25314: "intermission",
        26971: "intermission enrage"
    },

    # phase 5
    {
        27529: "wrath of the heavens",
        27538: "death of the heavens",
        27528: "dark thordan enrage"
    },

    # phase 6 and intermission 2
    {
        26215: "adds beginning",
        27957: "wyrmsbreath", # add dupe check
        27969: "akh afah", # add dupe check
        27966: "hallowed plume", # add dupe check
        27973: "wroth flames",
        27937: "adds enrage",
        29156: "shockwave",
        29752: "alternative end"
    },
    
    # phase 7
    {
        28060: "exaflare's edge", # add dupe check
        28065: "trinity",
        29452: "akh morn's edge", # add dupe check
        28058: "gigaflare's edge", # add dupe check
        28206: "dkt enrage"
    },

    # kill
    {
        6969: "kill"
    }
]

class Phase(IntEnum):
    phase_1 = 0
    phase_2 = 1
    phase_3 = 2
    phase_4 = 3
    intermission_1 = 4
    phase_5 = 5
    phase_6 = 6
    phase_7 = 7
    kill = 8

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.value

# initialize wipe frequency dictionary
# it's in the format of
"""
{
    "phase_1": {
        25300: frequency
    },
    "phase_2": {
        25555: frequency,
        25569: frequency,
        25533: frequency,
        25539: frequency
    }
    ...
}
"""
wipe_frequency = {
    str(phase):  {
        mechanic: 0
        for mechanic in phase_ability_ids[phase]
    }
    for phase in Phase
    }


# oauth2
client = BackendApplicationClient(client_id = client_id)
oauth = OAuth2Session(client = client)
token = oauth.fetch_token(
    token_url='https://www.fflogs.com/oauth/token', 
    client_id = client_id, 
    client_secret=client_secret,
    )

# get log IDs and fight phase info
logs_response = requests.post(
    'https://www.fflogs.com/api/v2/client',
    headers={
        'Authorization': f'Bearer {token["access_token"]}',
    },
    json={
        'query': '''
            query GetPhaseInfo ($guildID: Int) {
                reportData {
                    reports(
                        guildID:$guildID
                ) {
                        data {
                            code
                            fights (
                                encounterID: 1065,
                                killType: Encounters
                            ) {
                                id
                                kill
                                lastPhaseAsAbsoluteIndex
                            }
                        }
                    }
                }
            }
        ''',
        'variables': {
            'guildID': guild_id
        }
    }
)
logs = logs_response.json()

total_logs = 0
for log in logs["data"]["reportData"]["reports"]["data"]:
    if log["fights"] is not None:
        total_logs += 1
print(f"Initial log retrieval done. Total logs to go through: {total_logs}")
marker = 0
# get mechanic wipe data by phase
for log in logs["data"]["reportData"]["reports"]["data"]:
    report_code = log["code"]
    marker += 1
    print(f"({marker}/{total_logs}) Getting phase info for log: {report_code}")
    fights = log["fights"]
    if not fights:
        continue

    for phase in Phase:
        print(f"{report_code}: {phase}")


        filter_expression = "ability.id=" + " OR ability.id=".join(
            str(ability_id)
            for ability_id in phase_ability_ids[phase]
        )

    
        # for each phase, check initial fight info if any wipes exist in phase
        # if they do, add them to fight_IDs, otherwise skip phase
        fight_IDs = []
        for fight in fights:
            if fight["kill"] == True and phase == Phase.kill:
                wipe_frequency["kill"][6969] += 1
                continue
            if fight["lastPhaseAsAbsoluteIndex"] == phase.value:
                fight_IDs.append(fight["id"])

        if not fight_IDs:
            continue
        
        mechanics_response = requests.post(
            'https://www.fflogs.com/api/v2/client',
            headers={
                'Authorization': f'Bearer {token["access_token"]}',
            },
            json={
                'query': '''
                    query GetMechanicsInfo ($reportCode: String, $filterExpression: String, $fightIDs: [Int]) {
                        reportData {
                            report(code:$reportCode) {
                                events (
                                    startTime:0,
                                    endTime:2147483647,
                                    encounterID:1065,
                                    fightIDs: $fightIDs
                                    hostilityType: Enemies,
                                    dataType: Casts,
                                    filterExpression:$filterExpression
                                    ) {
                                    data
                                }
                            }
                        }
                    }
                ''',
                'variables': {
                    "reportCode": report_code,
                    "fightIDs": fight_IDs,
                    "filterExpression": filter_expression,
                }
            }
        )
        farthest = {}
        mechanics_data = mechanics_response.json()
        for event in mechanics_data["data"]["reportData"]["report"]["events"]["data"]:
            farthest[event["fight"]] = event["abilityGameID"]

        for wipe_mech in farthest.values():
            wipe_frequency[phase.name][wipe_mech] += 1
print("Finished.")


df = pd.DataFrame.from_dict({(i,phase_ability_ids[Phase[i]][j]): wipe_frequency[i][j]
                             for i in wipe_frequency.keys()
                             for j in wipe_frequency[i].keys()},
                            orient='index')
df.fillna(0, inplace=True)
print(df)