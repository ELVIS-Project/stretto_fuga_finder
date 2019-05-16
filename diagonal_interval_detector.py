from music21 import *
import numpy as np

Josquin_secure_corpus=corpus.corpora.LocalCorpus()
Josquin_secure_corpus.addPath('../Mass duos Josquin - De La Rue/Josquin (secure)/XML')
Piece=corpus.parse('XML/Josquin Missa Ave maris stella - Agnus II.xml')
Piece_Parts=instrument.partitionByInstrument(Piece)

Piece_Upper_voice = {}
Piece_Lower_voice = {}
Interval_pattern = []

Values = {
0: "Paralel intervals at",
1: "Imitation at the minime",
2: "Imitation at the semi-breve",
3: "Imitation at the doted semi-breve",
4: "Imitation at the breve",
5: "Imitation at the breve and a minime",
6: "Imitation at the dotted breve",
7: "Imitation at the breve and a doted semi-breve",
8: "Imitation at the longa"
}

L_upp=len(Piece_Parts.parts[0].notesAndRests.stream())
L_low=len(Piece_Parts.parts[1].notesAndRests.stream())
L=min(L_upp, L_low)

for i in range (0,L_upp):
    try:
        Piece_Parts[0].notesAndRests.stream()[i].pitch
    except:
        Piece_Upper_voice[Piece_Parts[0].notesAndRests.stream()[i].offset]=0
    else:
        Piece_Upper_voice[Piece_Parts[0].notesAndRests.stream()[i].offset]=[Piece_Parts[0].notesAndRests.stream()[i].pitch,Piece_Parts[0].notesAndRests.stream()[i].measureNumber]

for i in range (0,L_low):
    try:
        Piece_Parts.parts[1].notesAndRests.stream()[i].pitch
    except:
        Piece_Lower_voice[Piece_Parts[1].notesAndRests.stream()[i].offset]=0
    else:
        Piece_Lower_voice[Piece_Parts[1].notesAndRests.stream()[i].offset]=[Piece_Parts[1].notesAndRests.stream()[i].pitch,Piece_Parts[1].notesAndRests.stream()[i].measureNumber]

for i in range (-8,9):
    if i<0:
        Imitation="below"
    elif i == 0:
        Imitation=""
    else:
        Imitation="above"

    for position in Piece_Lower_voice:
        if position+i in Piece_Upper_voice:
            if Piece_Lower_voice[position] == 0:
                print("Rest")
            else:
                if Piece_Upper_voice[position+i] == 0:
                    print("Rest")
                else:
                    print("At Measure",Piece_Lower_voice[position][1]," ",Values[abs(i)],"a",interval.notesToInterval(Piece_Lower_voice[position][0],Piece_Upper_voice[position+i][0]).niceName.split()[1],Imitation)
        else:
            print("Free counterpoint")
