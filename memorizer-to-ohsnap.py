# -*- coding: utf-8 -*-

import requests
import json
from sys import stdin

def make_ohsnap_file(remote_file_uri):
    if not remote_file_uri:
        print('No remote URI specified!')
        return

    source = requests.get(remote_file_uri)
    data = source.json()

    output = {}
    output['subject'] = data['name'].upper()
    output['questions'] = []

    for q in data['questions']:
        question = {}
        question['description'] = q['question']
        if len(question['description']) >= 500:
            continue
        question['answers'] = []
        for x in range(0, len(q['answers'])):
            if type(q['correct']) is list:
                correct = x in q['correct']
            else:
                correct = x == q['correct']

            question['answers'].append({ 'description': q['answers'][x], 'correct': correct })

        if 'image' not in q:
            output['questions'].append(question)

    with open('%s.json' % output['subject'], 'w') as f:
        f.write(json.dumps(output))

make_ohsnap_file(stdin.readline().strip())
