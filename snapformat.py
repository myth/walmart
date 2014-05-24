# -*- coding: utf-8 -*-

# This script uses the uberbasic snapsyntax to process a text file and create a json file
# containing quiz questions and answers.

# Input format:

# First line is subject name
# No starting tab means question
# One tab means wrong answer
# Two tab means correct answer

import json
from sys import stdin

if __name__ == '__main__':

    s = {}
    q = []
    i = -1

    data = stdin.readlines()
    s['subject'] = data[0].strip()
    data = data[1:]

    if not data:
        exit('Input file was empty')
    for line in data:
        if line[0] != '\t':
            q.append({'description': line, 'answers': []})
            i += 1
        else:
            a = {}
            if line[1] != '\t':
                a['description'] = line[1:].strip()
                a['correct'] = False
            else:
                a['description'] = line[2:].strip()
                a['correct'] = True
            q[i]['answers'].append(a)

    s['questions'] = q

    f = open('%s.json' % s['subject'], 'w')
    f.write(json.dumps(s))
    f.close()
