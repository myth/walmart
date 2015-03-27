# -*- encoding: utf-8 -*-

import requests
import time

STATS = True
INFINITE = True
INTERVAL = 2
VOTING_ENDPOINT = 'http://www.adressa.no/poll/vote.do'

# These are the required fields from the voting form
payload = {
    "vote": "svar4",
    "mentometerId": "10790638",
    "publicationId": "167",
    "redirectTo": "http://www.adressa.no/nyheter/trondheim/article10789480.ece?service=poll&pollId=10790638",
}

while (INFINITE):
    response = requests.post(VOTING_ENDPOINT, params=payload)

    json = response.json()
    json['options'].sort(key=lambda x: x['votes'], reverse=True)

    if (STATS):
        for o in json['options']:
            print unicode(o['label']) + ': ' + unicode(o['percentage']) + ' (' + unicode(o['votes']) + ')'
        print "-------------------------------------------"

    time.sleep(INTERVAL)
