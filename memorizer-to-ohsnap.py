# -*- coding: utf-8 -*-

import requests
import json
from sys import stdin, argv

def make_ohsnap_file(remote_file_uri=None, data=None):
    if not remote_file_uri and not data:
        print('No remote URI or dataspecified!')
        return

    if remote_file_uri:
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

        valid_answers = True

        for x in range(0, len(q['answers'])):
            if type(q['correct']) is list:
                correct = x in q['correct']
            else:
                correct = x == q['correct']

            if len(q['answers'][x]) >= 500:
                valid_answers = False

            question['answers'].append({ 'description': q['answers'][x], 'correct': correct })

        if 'image' not in q and valid_answers:
            output['questions'].append(question)

    with open('%s.json' % output['subject'], 'w') as f:
        f.write(json.dumps(output))


if __name__ == '__main__':
    if len(argv) > 1:
        with open(argv[1]) as f:
            make_ohsnap_file(data=json.loads(f.read().strip()))
    else:
        make_ohsnap_file(remote_file_uri=stdin.readline().strip())
