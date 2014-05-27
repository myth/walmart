# -*- coding: utf-8 -*-

title = 'MMI'
questions = ["Smith and Mosier ('86) High level goals for data display. Hva menes med Consistency of data display?",
             "Smith and Mosier ('86) High level goals for data display. Hva menes med Efficient information assimilation of the user?",
             "Smith and Mosier ('86) High level goals for data display. Hva menes med Minimal memory load on the user?",
             "Smith and Mosier ('86) High level goals for data display. Hva menes med Compatibility of data display with data entry?",
             "Smith and Mosier ('86) High level goals for data display. Hva menes med Flexibility for user control of data display?"]

answers = ["Standardiser bruk av elementer gjennom applikasjonen slik at du får konsistens.",
           "Formatet på informasjonen bør være kjent for brukeren og være i sammenheng med dataene som skal vises. Eks. vis liste som en liste, og ha punkter/tallene på venstreside og ikke på høyreisde.",
           "Brukeren skal ikke behøve å huske ting fra en visning til den neste.",
           "Formatet på vist informasjon skal være direkte lenket til formatet på input-fields. Eks. bruk input-fields som oppdaterer andre sider direkte (live preview f.eks.)",
           "Brukere burde kunne få informasjonen vist på en måte som passer med oppgaven de skal gjøre."]


def map(title, questions, answers):
    output = []
    output.append(title)
    for q in questions:
        output.append(q)
        for a in answers:
            output.append('.%s' % a)
    return output

if __name__ == '__main__':
    o = map(title, questions, answers)
    f = open('lazyq.snap', 'w')
    for x in o:
        f.write('%s\n' % x)
    f.close()
