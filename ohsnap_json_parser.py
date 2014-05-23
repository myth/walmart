from urllib2 import urlopen
import json
import sys
import requests

urls = sys.argv[1:]

for url in urls:
    r = requests.get(url)
    data = r.json()
    qset = {}
    qset['subject'] = data['name']
    qset['questions'] = []
    for q in data['questions']:
        question = {}
        question['description'] = q['question']
        question['answers'] = []
        for x in range(0, len(q['answers'])):
            question['answers'].append({'description': q['answers'][x], 'correct': True if q['correct'] == x else False})
        qset['questions'].append(question)

    output = open(u'%s_%s.json' %(data['code'], data['exam']), 'w')
    output.write(json.dumps(qset))
    output.close()
