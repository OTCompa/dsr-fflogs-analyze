import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
import matplotlib.pyplot as plt
#import numpy as np


# input your stuff here
client_id = r'your-client-id-here'
client_secret = r'your-client-secret-here'
guild_id = 1337

# oauth2
client = BackendApplicationClient(client_id = client_id)
oauth = OAuth2Session(client = client)
token = oauth.fetch_token(
    token_url='https://www.fflogs.com/oauth/token', 
    client_id = client_id, 
    client_secret=client_secret,
    )

total_fights = 0
phase_frequency = [0] * 9

# get last pull 
response = requests.post(
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
                                                            fights (
                                                                encounterID: 1065,
                                                                killType: Encounters
                                                            ) {
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
data = response.json()

for encounter in data["data"]["reportData"]["reports"]["data"]:
    for fight in encounter["fights"]:
        total_fights += 1
        if fight["kill"] == True:
            phase_frequency[8] += 1
        else:
            phase_frequency[fight["lastPhaseAsAbsoluteIndex"]] += 1

            
labels = "Doorboss", "Thordan", "Nidhogg", "Eyes", "Rewind", "Dark Thordan", "Adds", "Gigachad", "Kill"

fig, ax = plt.subplots()
# lambda function shows frequency on the pie chart instead of percentage
ax.pie(
    phase_frequency, 
    wedgeprops= {
        'linewidth': 10
    },
    autopct = lambda p: '{:.0f}'.format(p * total_fights / 100) if p != 0 else "",
    startangle=90,
    counterclock = False
    )
ax.legend(labels = labels, loc='upper right')
ax.axis('equal')
ax.set_title(f"DSR wipes by phase (Total: {total_fights})")
plt.show()