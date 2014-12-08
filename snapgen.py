from random import shuffle
from copy import deepcopy
from itertools import product

subject = 'Informasjonssystemer'
definitions = [
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

terms = []
descriptions = []

for term, desc in definitions:
    terms.append(term)
    descriptions.append(desc)

with open('%s.snap' % subject, 'w') as f:
    f.write(subject + '\n')
    for term in terms:
        f.write(term + ' is ...\n')
        shuffle(descriptions)
        for desc in descriptions:
            if (term, desc) in definitions:
                f.write('..%s\n' % desc)
            else:
                f.write('.%s\n' % desc)
