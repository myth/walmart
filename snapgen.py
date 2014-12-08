from random import shuffle
from copy import deepcopy
from itertools import product

# Change these variables to suit your needs
SUBJECT = 'Informasjonssystemer'
TERM_PREFIX = 'What best describes'
TERM_SUFFIX = '?'
DEFINITIONS = [
    ('Organizational culture', 'The major understanding and assumptions for a business'),
    ('Organizational change', 'How organizations plan for, implement, and handle change'),
    ('Change model', 'Representation of change theories that identifies the phases of change'),
    ('Unfreezing', 'Ceasing old habits and creating a climate receptive to change'),
    ('Moring', 'The process of learning new methods and systems'),
    ('Refreezing', 'Reinforce changes to make the new process accepted'),
    ('Organizational learning', 'Adapting to new conditions or altering practices over time'),
    ('Return of Investment (ROI)', 'Profits generated as a percentage of the investment in IS'),
    ('Earning growth', 'The increase in profit'),
]

# Do not change anything below...

terms = []
descriptions = []

for term, desc in DEFINITIONS:
    terms.append(term)
    descriptions.append(desc)

with open('%s.snap' % SUBJECT, 'w') as f:
    f.write(SUBJECT + '\n')
    for term in terms:
        f.write('%s term %s\n' % (TERM_PREFIX, TERM_SUFFIX))
        shuffle(descriptions)
        for desc in descriptions:
            if (term, desc) in DEFINITIONS:
                f.write('..%s\n' % desc)
            else:
                f.write('.%s\n' % desc)
