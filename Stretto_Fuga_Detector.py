import numpy as np
import os
import csv
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


def Stretto_Fuga_detector(duration_1, duration_2, interval):
    if duration_2 >= 90:
        return "Canonic Piece"
    else:
        if interval in ["Minime", "Doted minime", "Semibreve"]:
            if duration_1 == 1:
                return "Strict Stretto Fuga"
            elif 1 < duration_1 <= 2:
                return "Stretto Fuga"
            elif duration_1 == 1/2:
                return "Double Option"
            else:
                return " "
        else:
            return " "


Time = [-24, -16, -12, -8, -6, -4, -3, -2, -1, 1, 2, 3, 4, 6, 8, 12, 16, 24]

Values = {
    1: "Semi-minime",
    2: "Minime",
    3: "Doted minime",
    4: "Semibreve",
    6: "Semibreve and a minime",
    8: "Breve",
    12: "Breve and a semibreve",
    16: "Longa",
    24: "Longa and a breve"
}


def ImitationDetector(score):

    Parts = [p.flat.notesAndRests.stream() for p in score.parts]

    L_upp = len(Parts[0])
    L_low = len(Parts[1])
    L = min(L_upp, L_low)

    Upper_voice = OrderedDict()
    Lower_voice = OrderedDict()

    for i in range (0,L_upp):
        current_event = Parts[0][i]
        pitch_rest = current_event.pitch if hasattr(current_event, "pitch") else "Rest"
        if pitch_rest != "Rest":
            pitch_tie = current_event.tie.type if isinstance(current_event.tie,tie.Tie) else None
        else:
            pitch_tie = "Rest"
        Upper_voice[current_event.offset] = [pitch_rest, current_event.measureNumber, current_event.offset, pitch_tie, current_event.quarterLength]

    for j in range (0,L_low):
        current_event = Parts[1][j]
        pitch_rest = current_event.pitch if hasattr(current_event, "pitch") else "Rest"
        if pitch_rest != "Rest":
            pitch_tie = current_event.tie.type if isinstance(current_event.tie,tie.Tie) else None
        else:
            pitch_tie = "Rest"
        Lower_voice[current_event.offset] = [pitch_rest, current_event.measureNumber, current_event.offset, pitch_tie, current_event.quarterLength]

    Imitation_list = []

    for k in Time:

        if k<0:
            Emplacement = "below"
        elif k == 0:
            Emplacement = ""
        else:
            Emplacement = "above"

        if list(Lower_voice.keys())[0] + k in Upper_voice:
            I = DiagInterval(Lower_voice[list(Lower_voice.items())[0][0]][0], Upper_voice[list(Lower_voice.items())[0][0]+k][0])
            D = Lower_voice[0][4]
        else:
            I = None
            D = 0
        Imitation = []
        B = 0

        for l in range (1,L-1):
            if Lower_voice[list(Lower_voice.items())[l][0]][0] == 'Rest':
                if list(Lower_voice.keys())[l] + k in Upper_voice:
                    if Upper_voice[list(Lower_voice.items())[l][0]+k][0] == 'Rest':
                        pass
                    else:
                        if Imitation != []:
                            if Imitation[-1][5] != None:
                                pass
                            else:
                                Imitation[-1][1] = Lower_voice[list(Lower_voice.items())[l][0]][1]
                                Imitation[-1][4] = Lower_voice[list(Lower_voice.items())[l][0]][2] - Imitation[-1][4]
                                Imitation[-1][5] = B
                                Imitation[-1][7] = D/k
                        else:
                            pass
                        B = 0
                else:
                    if Imitation != []:
                        if Imitation[-1][5] != None:
                            pass
                        else:
                            Imitation[-1][1] = Lower_voice[list(Lower_voice.items())[l][0]][1]
                            Imitation[-1][4] = Lower_voice[list(Lower_voice.items())[l][0]][2] - Imitation[-1][4]
                            Imitation[-1][5] = B
                            Imitation[-1][7] = D/k
                    else:
                        pass
                    B = 0
            else:
                if Lower_voice[list(Lower_voice.items())[l][0]][3] == 'stop':
                    pass
                elif Lower_voice[list(Lower_voice.items())[l][0]][3] == 'continue':
                    pass
                else:
                    if list(Lower_voice.keys())[l] + k in Upper_voice:
                        if DiagInterval(Lower_voice[list(Lower_voice.items())[l][0]][0],Upper_voice[list(Lower_voice.items())[l][0]+k][0]) == I:
                            B = B+1
                            if B == 3:
                                Imitation.append([Lower_voice[list(Lower_voice.items())[l-3][0]][1], None, Values[abs(k)], I + " " + Emplacement, Lower_voice[list(Lower_voice.items())[l-3][0]][2], None, score.measure(Lower_voice[list(Lower_voice.items())[l][0]][1]).duration.quarterLength, None])
                            else:
                                pass
                        else:
                            if Imitation != []:
                                if Imitation[-1][5] != None:
                                    pass
                                else:
                                    Imitation[-1][1] = Lower_voice[list(Lower_voice.items())[l][0]][1]
                                    Imitation[-1][4] = Lower_voice[list(Lower_voice.items())[l][0]][2] - Imitation[-1][4]
                                    Imitation[-1][5] = B
                                    Imitation[-1][7] = D/k
                            else:
                                pass
                            B = 0
                            I = DiagInterval(Lower_voice[list(Lower_voice.items())[l][0]][0], Upper_voice[list(Lower_voice.items())[l][0]+k][0])
                            D = Lower_voice[list(Lower_voice.items())[l][0]][4]
                    else:
                        if Imitation != []:
                            if Imitation[-1][5] != None:
                                pass
                            else:
                                Imitation[-1][1] = Lower_voice[list(Lower_voice.items())[l][0]][1]
                                Imitation[-1][4] = Lower_voice[list(Lower_voice.items())[l][0]][2] - Imitation[-1][4]
                                Imitation[-1][5] = B
                                Imitation[-1][7] = D/k
                        else:
                            pass
                        B = 0
        if Imitation != []:
            if Imitation[-1][5] != None:
                Imitation_list.append(Imitation)
                Imitation = []
            else:
                Imitation[-1][1] = Lower_voice[list(Lower_voice.items())[l][0]][1]
                Imitation[-1][4] = Lower_voice[list(Lower_voice.items())[l][0]][2]-Imitation[-1][4]
                Imitation[-1][5] = B
                Imitation[-1][7] = D/k
                Imitation_list.append(Imitation)
                Imitation = []
        else:
            pass
    return Imitation_list


def Long_imitation_Detector(filename):
    Piece=corpus.parse(filename)
    LI_List=[[Piece[2].content,Piece[1].content,Piece[0].content]]
    try:
        ImitationDetector(Piece)
    except:
        LI_List.append("Error")
    else:
        Imitation_list=ImitationDetector(Piece)
        for Interval in Imitation_list:
            for Imitation in Interval:
                if Imitation[4]>=2*Imitation[6]:
                    LI_List.append([Imitation[0], Imitation[1], Imitation[2], Imitation[3], round(Imitation[4]/Piece.asTimespans()[-1].offset*100), round(Imitation[5]/Imitation[4],2), Stretto_Fuga_detector(Imitation[7], round(Imitation[4]/Piece.asTimespans()[-1].offset*100), Imitation[2])])
                else:
                    pass
    return LI_List


def Short_imitation_Detector(filename):
    Piece=corpus.parse(filename)
    SI_List=[[Piece[2].content,Piece[1].content,Piece[0].content]]
    try:
        ImitationDetector(Piece)
    except:
        SI_List.append("Error")
    else:
        Imitation_list=ImitationDetector(Piece)
        for Interval in Imitation_list:
            for Imitation in Interval:
                if Imitation[4]<2*Imitation[6]:
                    SI_List.append([Imitation[0], Imitation[1], Imitation[2], Imitation[3], Stretto_Fuga_detector(Imitation[7], round(Imitation[4]/Piece.asTimespans()[-1].offset*100), Imitation[2])])
                else:
                    pass
    return SI_List


if __name__ == '__main__':
    LoadCorpora(load_josquin=True, load_larue=True)
    li_list = []
    si_list=[]
    li_CSV_data = []
    si_CSV_data = []
    for f in corpus.getLocalPaths():
        li_list.append(Long_imitation_Detector(f))
        si_list.append(Short_imitation_Detector(f))
    for piece in li_list:
        metadata = piece[0]
        for li in piece[1:]:
            li_csv_str = '{}, {}, {}, {}, {}, {}, {}, {}, {}, {}'.format(metadata[0], metadata[1], metadata[2], li[0], li[1], li[2], li[3], li[4], li[5], li[6])
            li_CSV_data.append(li_csv_str.split(','))
    for piece in si_list:
        metadata = piece[0]
        for si in piece[1:]:
            si_csv_str = '{}, {}, {}, {}, {}, {}, {}, {}'.format(metadata[0], metadata[1], metadata[2], si[0], si[1], si[2], si[3], si[4])
            si_CSV_data.append(si_csv_str.split(','))
    with open('Long_Imitation.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(li_CSV_data)
    csvFile.close()
    with open('Short_Imitation.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(si_CSV_data)
    csvFile.close()
