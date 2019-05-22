from music21 import *
from collections import OrderedDict
import numpy as np

Josquin_secure_corpus=corpus.corpora.LocalCorpus()
Josquin_secure_corpus.addPath('../Mass duos Josquin - De La Rue/Josquin (secure)/XML')
Piece=corpus.parse('XML/Josquin Missa Ave maris stella - Agnus II.xml')


def DiagInterval(note1,note2):
    if note1 == 'Rest':
        return 'Rest'
    elif note2 == 'Rest':
        return 'Rest'
    else:
        return interval.notesToInterval(note1,note2).niceName.split()[1]


def ImitationDetector(score):

    Values = {
    0: "Parallel motion",1: "Crotchet",2: "Minime",3: "Doted minime",4: "Semibreve",5: "Semibreve and a crotchet",6: "Dotted semibreve",7: "Semibreve and a doted minime",8: "Breve"
             }

    Parts=instrument.partitionByInstrument(score)

    L_upp=len(Parts.parts[0].notesAndRests.stream())
    L_low=len(Parts.parts[1].notesAndRests.stream())
    L=min(L_upp, L_low)

    Upper_voice = OrderedDict()
    Lower_voice = OrderedDict()

    for i in range (0,L_upp):
        try:
            Parts[0].notesAndRests.stream()[i].pitch
        except:
            Upper_voice[Parts[0].notesAndRests.stream()[i].offset]=["Rest",Parts[0].notesAndRests.stream()[i].measureNumber,Parts[0].notesAndRests.stream()[i].offset]
        else:
            Upper_voice[Parts[0].notesAndRests.stream()[i].offset]=[Parts[0].notesAndRests.stream()[i].pitch,Parts[0].notesAndRests.stream()[i].measureNumber,Parts[0].notesAndRests.stream()[i].offset]

    for j in range (0,L_low):
        try:
            Parts.parts[1].notesAndRests.stream()[j].pitch
        except:
            Lower_voice[Parts[1].notesAndRests.stream()[j].offset]=["Rest",Parts[1].notesAndRests.stream()[j].measureNumber,Parts[1].notesAndRests.stream()[j].offset]
        else:
            Lower_voice[Parts[1].notesAndRests.stream()[j].offset]=[Parts[1].notesAndRests.stream()[j].pitch,Parts[1].notesAndRests.stream()[j].measureNumber,Parts[1].notesAndRests.stream()[j].offset]


    Imitation_list = []

    for k in range (-8,9):

        if k<0:
            Imitation="below"
        elif k == 0:
            Imitation=""
        else:
            Imitation="above"

        A=[]
        B=0

        for l in range (0,L-1):
            if list(Lower_voice.items())[l][0]+k in Upper_voice:
                if list(Lower_voice.items())[l+1][0]+k in Upper_voice:
                    if DiagInterval(Lower_voice[list(Lower_voice.items())[l][0]][0],Upper_voice[list(Lower_voice.items())[l][0]+k][0]) == DiagInterval(Lower_voice[list(Lower_voice.items())[l+1][0]][0],Upper_voice[list(Lower_voice.items())[l+1][0]+k][0]):
                        B=B+1
                        if B==3:
                            A.append(["Measure {}".format(Lower_voice[list(Lower_voice.items())[l-2][0]][1]),Values[abs(k)],DiagInterval(Lower_voice[list(Lower_voice.items())[l][0]][0],Upper_voice[list(Lower_voice.items())[l][0]+k][0])+" "+Imitation,Lower_voice[list(Lower_voice.items())[l-2][0]][2],None])
                        else:
                            pass
                    elif DiagInterval(Lower_voice[list(Lower_voice.items())[l+1][0]][0],Upper_voice[list(Lower_voice.items())[l+1][0]+k][0])=='Rest':
                        if list(Lower_voice.items())[l+2][0]+k in Upper_voice:
                             if DiagInterval(Lower_voice[list(Lower_voice.items())[l][0]][0],Upper_voice[list(Lower_voice.items())[l][0]+k][0]) == DiagInterval(Lower_voice[list(Lower_voice.items())[l+2][0]][0],Upper_voice[list(Lower_voice.items())[l+2][0]+k][0]):
                                 B=B+1
                             else:
                                 if A!=[]:
                                     if A[-1][4]!=None:
                                         pass
                                     else:
                                         A[-1][0]=A[-1][0]+" to measure {}".format(Lower_voice[list(Lower_voice.items())[l][0]][1])
                                         A[-1][3]=Lower_voice[list(Lower_voice.items())[l][0]][2]-A[-1][3]
                                         A[-1][4]=B
                                 else:
                                     pass
                                 B=0
                        else:
                            pass
                    elif DiagInterval(Lower_voice[list(Lower_voice.items())[l][0]][0],Upper_voice[list(Lower_voice.items())[l][0]+k][0])=='Rest':
                        if list(Lower_voice.items())[l-1][0]+k in Upper_voice:
                            if DiagInterval(Lower_voice[list(Lower_voice.items())[l-1][0]][0],Upper_voice[list(Lower_voice.items())[l-1][0]+k][0]) == DiagInterval(Lower_voice[list(Lower_voice.items())[l+1][0]][0],Upper_voice[list(Lower_voice.items())[l+1][0]+k][0]):
                             B=B+1
                            else:
                                if A!=[]:
                                    if A[-1][4]!=None:
                                        pass
                                    else:
                                        A[-1][0]=A[-1][0]+" to measure {}".format(Lower_voice[list(Lower_voice.items())[l][0]][1])
                                        A[-1][3]=Lower_voice[list(Lower_voice.items())[l][0]][2]-A[-1][3]
                                        A[-1][4]=B
                                else:
                                    pass
                                B=0
                        else:
                            pass
                    else:
                        if A!=[]:
                            if A[-1][4]!=None:
                                pass
                            else:
                                A[-1][0]=A[-1][0]+" to measure {}".format(Lower_voice[list(Lower_voice.items())[l][0]][1])
                                A[-1][3]=Lower_voice[list(Lower_voice.items())[l][0]][2]-A[-1][3]
                                A[-1][4]=B
                        else:
                            pass
                        B=0
                else:
                    if A!=[]:
                        if A[-1][4]!=None:
                            pass
                        else:
                            A[-1][0]=A[-1][0]+" to measure {}".format(Lower_voice[list(Lower_voice.items())[l][0]][1])
                            A[-1][3]=Lower_voice[list(Lower_voice.items())[l][0]][2]-A[-1][3]
                            A[-1][4]=B
                    else:
                        pass
            else:
                if A!=[]:
                    if A[-1][4]!=None:
                        pass
                    else:
                        A[-1][0]=A[-1][0]+" to measure {}".format(Lower_voice[list(Lower_voice.items())[l][0]][1])
                        A[-1][3]=Lower_voice[list(Lower_voice.items())[l][0]][2]-A[-1][3]
                        A[-1][4]=B
                else:
                    pass

        if A!=[]:
            if A[-1][4]!=None:
                Imitation_list.append(A)
                A=[]
            else:
                A[-1][0]=A[-1][0]+" to measure {}".format(Lower_voice[list(Lower_voice.items())[l][0]][1])
                A[-1][3]=Lower_voice[list(Lower_voice.items())[l][0]][2]-A[-1][3]
                A[-1][4]=B
                Imitation_list.append(A)
                A=[]
        else:
            pass
        B=0
    return Imitation_list
