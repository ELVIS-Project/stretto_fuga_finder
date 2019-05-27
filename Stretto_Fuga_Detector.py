import numpy as np
import os
from music21 import *
from collections import OrderedDict


def LoadCorpora(load_josquin=True, load_larue=True):
    ''' Loads the corpora to study '''
    if load_josquin == True:
        corpus.addPath('./mass-duos-corpus-josquin-larue/Josquin (secure)/XML')
    if load_larue == True:
        corpus.addPath('./mass-duos-corpus-josquin-larue/La Rue (secure)/XML')

def DiagInterval(note1,note2):
    if note1 == 'Rest':
        return 'Rest'
    elif note2 == 'Rest':
        return 'Rest'
    else:
        return interval.notesToInterval(note1,note2).niceName.split()[1]

def ImitationDetector(score):
    Values = {
        0: "Parallel motion",
        1: "Crotchet",
        2: "Minime",
        3: "Doted minime",
        4: "Semibreve",
        5: "",
        6: "Doted semibreve",
        7: "",
        8: "Breve",
        9:"",
        10:"",
        11:"",
        12:"Doted breve",
        13:"",
        14:"",
        15:"",
        16: "Longa"
    }

    Parts= [p.flat.notesAndRests.stream() for p in score.parts]

    L_upp=len(Parts[0])
    L_low=len(Parts[1])
    L=min(L_upp, L_low)

    Upper_voice = OrderedDict()
    Lower_voice = OrderedDict()

    for i in range (0,L_upp):
        current_event = Parts[0][i]
        pitch_rest = current_event.pitch if hasattr(current_event, "pitch") else "Rest"
        Upper_voice[current_event.offset] = [pitch_rest, current_event.measureNumber, current_event.offset]

    for j in range (0,L_low):
        current_event = Parts[1][j]
        pitch_rest = current_event.pitch if hasattr(current_event, "pitch") else "Rest"
        Lower_voice[current_event.offset] = [pitch_rest, current_event.measureNumber, current_event.offset]

    Imitation_list = []

    for k in range (-16,17):

        if k<0:
            Emplacement="below"
        elif k == 0:
            Emplacement=""
        else:
            Emplacement="above"

        Imitation=[]
        B=0

        for l in range (0,L-1):
            if list(Lower_voice.items())[l][0]+k in Upper_voice:
                if list(Lower_voice.items())[l+1][0]+k in Upper_voice:
                    if DiagInterval(Lower_voice[list(Lower_voice.items())[l][0]][0],Upper_voice[list(Lower_voice.items())[l][0]+k][0]) == DiagInterval(Lower_voice[list(Lower_voice.items())[l+1][0]][0],Upper_voice[list(Lower_voice.items())[l+1][0]+k][0]):
                        B=B+1
                        if DiagInterval(Lower_voice[list(Lower_voice.items())[l][0]][0],Upper_voice[list(Lower_voice.items())[l][0]+k][0]) == 'Rest':
                            pass
                        elif B==3:
                            Imitation.append(["Measure {}".format(Lower_voice[list(Lower_voice.items())[l-2][0]][1]),Values[abs(k)],DiagInterval(Lower_voice[list(Lower_voice.items())[l][0]][0],Upper_voice[list(Lower_voice.items())[l][0]+k][0])+" "+Emplacement,Lower_voice[list(Lower_voice.items())[l-2][0]][2],None,score.measure(Lower_voice[list(Lower_voice.items())[l][0]][1]).duration.quarterLength])
                        else:
                            pass
                    elif DiagInterval(Lower_voice[list(Lower_voice.items())[l+1][0]][0],Upper_voice[list(Lower_voice.items())[l+1][0]+k][0])=='Rest':
                            pass
                    elif DiagInterval(Lower_voice[list(Lower_voice.items())[l][0]][0],Upper_voice[list(Lower_voice.items())[l][0]+k][0])=='Rest':
                        if list(Lower_voice.items())[l-1][0]+k in Upper_voice:
                            if DiagInterval(Lower_voice[list(Lower_voice.items())[l-1][0]][0],Upper_voice[list(Lower_voice.items())[l-1][0]+k][0]) == DiagInterval(Lower_voice[list(Lower_voice.items())[l+1][0]][0],Upper_voice[list(Lower_voice.items())[l+1][0]+k][0]):
                             B=B+2
                            else:
                                if Imitation!=[]:
                                    if Imitation[-1][4]!=None:
                                        pass
                                    else:
                                        Imitation[-1][0]=Imitation[-1][0]+" to measure {}".format(Lower_voice[list(Lower_voice.items())[l][0]][1])
                                        Imitation[-1][3]=Lower_voice[list(Lower_voice.items())[l][0]][2]-Imitation[-1][3]
                                        Imitation[-1][4]=B
                                else:
                                    pass
                                B=0
                        else:
                            pass
                    else:
                        if Imitation!=[]:
                            if Imitation[-1][4]!=None:
                                pass
                            else:
                                Imitation[-1][0]=Imitation[-1][0]+" to measure {}".format(Lower_voice[list(Lower_voice.items())[l][0]][1])
                                Imitation[-1][3]=Lower_voice[list(Lower_voice.items())[l][0]][2]-Imitation[-1][3]
                                Imitation[-1][4]=B
                        else:
                            pass
                        B=0
                else:
                    if Imitation!=[]:
                        if Imitation[-1][4]!=None:
                            pass
                        else:
                            Imitation[-1][0]=Imitation[-1][0]+" to measure {}".format(Lower_voice[list(Lower_voice.items())[l][0]][1])
                            Imitation[-1][3]=Lower_voice[list(Lower_voice.items())[l][0]][2]-Imitation[-1][3]
                            Imitation[-1][4]=B
                    else:
                        pass
            else:
                if Imitation!=[]:
                    if Imitation[-1][4]!=None:
                        pass
                    else:
                        Imitation[-1][0]=Imitation[-1][0]+" to measure {}".format(Lower_voice[list(Lower_voice.items())[l][0]][1])
                        Imitation[-1][3]=Lower_voice[list(Lower_voice.items())[l][0]][2]-Imitation[-1][3]
                        Imitation[-1][4]=B
                else:
                    pass

        if Imitation!=[]:
            if Imitation[-1][4]!=None:
                Imitation_list.append(Imitation)
                Imitation=[]
            else:
                Imitation[-1][0]=Imitation[-1][0]+" to measure {}".format(Lower_voice[list(Lower_voice.items())[l][0]][1])
                Imitation[-1][3]=Lower_voice[list(Lower_voice.items())[l][0]][2]-Imitation[-1][3]
                Imitation[-1][4]=B
                Imitation_list.append(Imitation)
                Imitation=[]
        else:
            pass
        B=0
    return Imitation_list


def SFDetector(filename):
    Piece=corpus.parse(filename)
    SF_List=[[Piece[2].content,Piece[1].content,Piece[0].content]]
    try:
        ImitationDetector(Piece)
    except:
        SF_List.append("Error")
    else:
        Imitation_List=ImitationDetector(Piece)
        for Interval in Imitation_List:
            for Imitation in Interval:
                if Imitation[3]>=2*Imitation[5]:
                    SF_List.append([Imitation[0],Imitation[1],Imitation[2],round(Imitation[3]/Piece.asTimespans()[-1].offset*100),round(Imitation[4]/Imitation[3],2)])
                else:
                    pass
    return SF_List


def SIDetector(filename):
    Piece=corpus.parse(filename)
    SI_List=[[Piece[2].content,Piece[1].content,Piece[0].content]]
    try:
        ImitationDetector(Piece)
    except:
        SI_List.append("Error")
    else:
        Imitation_List=ImitationDetector(Piece)
        for Interval in Imitation_List:
            for Imitation in Interval:
                if Imitation[3]<2*Imitation[5]:
                    SI_List.append([Imitation[0],Imitation[1],Imitation[2]])
                else:
                    pass
    return SI_List


if __name__ == '__main__':
    LoadCorpora(load_josquin=True, load_larue=True)
    for f in corpus.getLocalPaths():
        print(SFDetector(f))
    # print(SFDetector(corpus.getWork('Et in spiritum')))
