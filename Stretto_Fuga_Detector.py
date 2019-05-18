from music21 import *
from collections import OrderedDict
import numpy as np

Josquin_secure_corpus=corpus.corpora.LocalCorpus()
Josquin_secure_corpus.addPath('../Mass duos Josquin - De La Rue/Josquin (secure)/XML')
Piece=corpus.parse('XML/Josquin Missa Ave maris stella - Agnus II.xml')
Piece_Parts=instrument.partitionByInstrument(Piece)

Piece_Upper_voice = OrderedDict()
Piece_Lower_voice = OrderedDict()
Interval_pattern = []

def DiagInterval(note1,note2):
    if note1 == 'Rest':
        return 'Rest'
    elif note2 == 'Rest':
        return 'Rest'
    else:
        return interval.notesToInterval(note1,note2).niceName.split()[1]


Values = {
0: "parallel motion at",
1: "stretto fuga at the minime",
2: "stretto fuga at the semi-breve",
3: "stretto fuga at the doted semi-breve",
4: "stretto fuga at the breve",
5: "stretto fuga at the breve and a minime",
6: "stretto fuga at the dotted breve",
7: "stretto fuga at the breve and a doted semi-breve",
8: "stretto fuga at the longa"
}

L_upp=len(Piece_Parts.parts[0].notesAndRests.stream())
L_low=len(Piece_Parts.parts[1].notesAndRests.stream())
L=min(L_upp, L_low)

for i in range (0,L_upp):
    try:
        Piece_Parts[0].notesAndRests.stream()[i].pitch
    except:
        Piece_Upper_voice[Piece_Parts[0].notesAndRests.stream()[i].offset]=["Rest",Piece_Parts[0].notesAndRests.stream()[i].measureNumber]
    else:
        Piece_Upper_voice[Piece_Parts[0].notesAndRests.stream()[i].offset]=[Piece_Parts[0].notesAndRests.stream()[i].pitch,Piece_Parts[0].notesAndRests.stream()[i].measureNumber]

for j in range (0,L_low):
    try:
        Piece_Parts.parts[1].notesAndRests.stream()[j].pitch
    except:
        Piece_Lower_voice[Piece_Parts[1].notesAndRests.stream()[j].offset]=["Rest",Piece_Parts[1].notesAndRests.stream()[j].measureNumber]
    else:
        Piece_Lower_voice[Piece_Parts[1].notesAndRests.stream()[j].offset]=[Piece_Parts[1].notesAndRests.stream()[j].pitch,Piece_Parts[1].notesAndRests.stream()[j].measureNumber]

for k in range (-8,9):

    A=[]

    if k<0:
        Imitation="below"
    elif k == 0:
        Imitation=""
    else:
        Imitation="above"
    B=0

    for l in range (0,L-1):
        if list(Piece_Lower_voice.items())[l][0]+k in Piece_Upper_voice:
            if list(Piece_Lower_voice.items())[l+1][0]+k in Piece_Upper_voice:
                if DiagInterval(Piece_Lower_voice[list(Piece_Lower_voice.items())[l][0]][0],Piece_Upper_voice[list(Piece_Lower_voice.items())[l][0]+k][0]) == DiagInterval(Piece_Lower_voice[list(Piece_Lower_voice.items())[l+1][0]][0],Piece_Upper_voice[list(Piece_Lower_voice.items())[l+1][0]+k][0]):
                    B=B+1
                    if B==3:
                        A.append("Measure {}, ".format(Piece_Lower_voice[list(Piece_Lower_voice.items())[l-2][0]][1])+Values[abs(k)]+" a "+DiagInterval(Piece_Lower_voice[list(Piece_Lower_voice.items())[l][0]][0],Piece_Upper_voice[list(Piece_Lower_voice.items())[l][0]+k][0])+" "+Imitation+";")
                    else:
                        pass
                elif DiagInterval(Piece_Lower_voice[list(Piece_Lower_voice.items())[l+1][0]][0],Piece_Upper_voice[list(Piece_Lower_voice.items())[l+1][0]+k][0])=='Rest':
                    if list(Piece_Lower_voice.items())[l+2][0]+k in Piece_Upper_voice:
                         if DiagInterval(Piece_Lower_voice[list(Piece_Lower_voice.items())[l][0]][0],Piece_Upper_voice[list(Piece_Lower_voice.items())[l][0]+k][0]) == DiagInterval(Piece_Lower_voice[list(Piece_Lower_voice.items())[l+2][0]][0],Piece_Upper_voice[list(Piece_Lower_voice.items())[l+2][0]+k][0]):
                             B=B+1
                         else:
                             if A!=[]:
                                 A[-1]=A[-1]+" it ends measure {}".format(Piece_Lower_voice[list(Piece_Lower_voice.items())[l-1][0]][1])+"."
                             else:
                                 pass
                    else:
                        pass
                elif DiagInterval(Piece_Lower_voice[list(Piece_Lower_voice.items())[l][0]][0],Piece_Upper_voice[list(Piece_Lower_voice.items())[l][0]+k][0])=='Rest':
                    if list(Piece_Lower_voice.items())[l-1][0]+k in Piece_Upper_voice:
                        if DiagInterval(Piece_Lower_voice[list(Piece_Lower_voice.items())[l-1][0]][0],Piece_Upper_voice[list(Piece_Lower_voice.items())[l-1][0]+k][0]) == DiagInterval(Piece_Lower_voice[list(Piece_Lower_voice.items())[l+1][0]][0],Piece_Upper_voice[list(Piece_Lower_voice.items())[l+1][0]+k][0]):
                         B=B+1
                        else:
                            if A!=[]:
                                A[-1]=A[-1]+" it ends measure {}".format(Piece_Lower_voice[list(Piece_Lower_voice.items())[l-1][0]][1])+"."
                            else:
                                pass
                    else:
                        pass
                else:
                    B=0
                    if A!=[]:
                        if A[-1].endswith("."):
                            pass
                        else:
                            A[-1]=A[-1]+" it ends measure {}".format(Piece_Lower_voice[list(Piece_Lower_voice.items())[l][0]][1])+"."
                    else:
                        pass
        else:
            if A!=[]:
                if A[-1].endswith("."):
                    pass
                else:
                    A[-1]=A[-1]+" it ends measure {}".format(Piece_Lower_voice[list(Piece_Lower_voice.items())[l][0]][1])+"."
            else:
                pass
    if A!=[]:
        if A[-1].endswith("."):
            Interval_pattern.append(A)
        else:
            A[-1]=A[-1]+" until the end of the piece."
            Interval_pattern.append(A)
    else:
        pass
