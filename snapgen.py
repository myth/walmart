from random import shuffle
from copy import deepcopy
from itertools import product

# Change these variables to suit your needs
SUBJECT = 'Virksomhetsarkitektur og innovasjon'
TERM_PREFIX = 'In the context of Enterprise Modeling, what best illustrates'
TERM_SUFFIX = '?'
DEFINITIONS = [
    ('Perspective', 'What are the important components?'),
    ('Framework', 'How do the different problems and questions relate to each other?'),
    ('Procedure, Notation and Concepts', 'What questions have to be asked?'),
    ('Ways of cooperation', 'Who asks, and who replies?'),
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
        f.write('%s %s %s\n' % (TERM_PREFIX, term, TERM_SUFFIX))
        shuffle(descriptions)
        for desc in descriptions:
            if (term, desc) in DEFINITIONS:
                f.write('..%s\n' % desc)
            else:
                f.write('.%s\n' % desc)
