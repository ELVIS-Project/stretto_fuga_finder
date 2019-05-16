from music21 import *
import numpy as np

Josquin_secure_corpus=corpus.corpora.LocalCorpus()
Josquin_secure_corpus.addPath('../Mass duos Josquin - De La Rue/Josquin (secure)/XML')
Piece=corpus.parse('XML/Josquin Missa Ave maris stella - Agnus II.xml')
Piece_Parts=instrument.partitionByInstrument(Piece)

Piece_Upper_voice = {}
Piece_Lower_voice = {}
Interval_pattern = []

L_upp=len(Piece_Parts.parts[0].notesAndRests.stream())
L_low=len(Piece_Parts.parts[1].notesAndRests.stream())
L=min(L_upp, L_low)

for i in range (0,L_upp):
    try:
        Piece_Parts[0].notesAndRests.stream()[i].pitch
    except:
        Piece_Upper_voice[Piece_Parts[0].notesAndRests.stream()[i].offset]=0
    else:
        Piece_Upper_voice[Piece_Parts[0].notesAndRests.stream()[i].offset]=Piece_Parts[0].notesAndRests.stream()[i].pitch

for i in range (0,L_low):
    try:
        Piece_Parts.parts[1].notesAndRests.stream()[i].pitch
    except:
        Piece_Lower_voice[Piece_Parts[1].notesAndRests.stream()[i].offset]=0
    else:
        Piece_Lower_voice[Piece_Parts[1].notesAndRests.stream()[i].offset]=Piece_Parts[1].notesAndRests.stream()[i].pitch

for i in range (-8,9):
    for position in Piece_Lower_voice:
        if position+i in Piece_Upper_voice:
            if Piece_Lower_voice[position] == 0:
                print("D = ",i, "Interval = 0")
            else:
                if Piece_Upper_voice[position+i] == 0:
                    print("D = ",i, "Interval = 0")
                else:
                    print("D = ",i, "Interval = ", interval.notesToInterval(Piece_Lower_voice[position],Piece_Upper_voice[position+i]).niceName.split()[1])
        else:
            print("D = ",i, "Interval = 0")
