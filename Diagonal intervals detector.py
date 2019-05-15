from music21 import *
import numpy as np

Josquin_secure_corpus=corpus.corpora.LocalCorpus()
Josquin_secure_corpus.addPath('../Mass duos Josquin - De La Rue/Josquin (secure)/XML')
Agnus_2=corpus.parse('XML/Josquin Missa Ave maris stella - Agnus II.xml')
Agnus_2_Parts=instrument.partitionByInstrument(Agnus_2)

Agnus_2_Upper_voice = {}
Agnus_2_Lower_voice = {}
Interval_pattern = []

L_sop=len(Agnus_2_Parts.parts['Soprano'].notesAndRests.stream())
L_ten=len(Agnus_2_Parts.parts['Tenor'].notesAndRests.stream())
L=min(L_sop, L_ten)

for i in range (0,L_sop):
    try:
        Agnus_2_Parts.parts['Soprano'].notesAndRests.stream()[i].pitch
    except:
        Agnus_2_Upper_voice[Agnus_2_Parts.parts['Soprano'].notesAndRests.stream()[i].offset]=0
    else:
        Agnus_2_Upper_voice[Agnus_2_Parts.parts['Soprano'].notesAndRests.stream()[i].offset]=Agnus_2_Parts.parts['Soprano'].notesAndRests.stream()[i].pitch

for i in range (0,L_ten):
    try:
        Agnus_2_Parts.parts['Tenor'].notesAndRests.stream()[i].pitch
    except:
        Agnus_2_Lower_voice[Agnus_2_Parts.parts['Tenor'].notesAndRests.stream()[i].offset]=0
    else:
        Agnus_2_Lower_voice[Agnus_2_Parts.parts['Tenor'].notesAndRests.stream()[i].offset]=Agnus_2_Parts.parts['Tenor'].notesAndRests.stream()[i].pitch

for i in range (-8,9):
    for position in Agnus_2_Lower_voice:
        if position+i in Agnus_2_Upper_voice:
            if Agnus_2_Lower_voice[position] == 0:
                print("D = ",i, "Interval = 0")
            else:
                if Agnus_2_Upper_voice[position+i] == 0:
                    print("D = ",i, "Interval = 0")
                else:
                    print("D = ",i, "Interval = ", interval.notesToInterval(Agnus_2_Lower_voice[position],Agnus_2_Upper_voice[position+i]))
        else:
            print("D = ",i, "Interval = 0")
