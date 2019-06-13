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
        return interval.Interval(note1,note2).directedNiceName.split()[0]+" "+interval.Interval(note1,note2).directedNiceName.split()[2]


def Stretto_Fuga_detector(duration_1, k, duration_2, interval):
    if duration_1 > abs(k):
        if duration_2 >= 85:
            if interval in ["Minim before", "Minim after", "Doted minim before", "Doted minim after", "Semibreve before", "Semibreve after", "Semibreve and a minim before", "Semibreve and a minim after", "Breve before", "Breve after"]:
                return "Stretto Fuga Canonic Piece"
            else:
                return "Canonic Piece"
        else:
            if interval in ["Minim before", "Minim after", "Doted minim before", "Doted minim after", "Semibreve before", "Semibreve after", "Semibreve and a minim before", "Semibreve and a minim after", "Breve before", "Breve after"]:
                return "Stretto Fuga"
            else:
                return " "
    else:
        return " "


Time = [-24, -16, -12, -8, -6, -4, -3, -2, -1, 1, 2, 3, 4, 6, 8, 12, 16, 24]

Values = {
    1: "Semi-minim",
    2: "Minim",
    3: "Doted minim",
    4: "Semibreve",
    6: "Semibreve and a minim",
    8: "Breve",
    12: "Breve and a semibreve",
    16: "Longa",
    24: "Longa and a breve"
}


def ImitationDetector(score):

    Parts = [p.flat.notesAndRests.stream() for p in score.parts]

    L_0 = len(Parts[0])
    L_1 = len(Parts[1])

    Upper_voice = OrderedDict([])
    Lower_voice = OrderedDict([])

    Real_dur_upp = 0
    Real_dur_low = 0

    for i in range (-L_0+1, 1):
        current_event = Parts[0][-i]
        pitch_rest = current_event.pitch if hasattr(current_event, "pitch") else "Rest"
        if pitch_rest != "Rest":
            pitch_tie = current_event.tie.type if isinstance(current_event.tie,tie.Tie) else None
            if pitch_tie == 'stop':
                Real_dur_upp = current_event.quarterLength
            elif pitch_tie == 'continue':
                Real_dur_upp = Real_dur_upp + current_event.quarterLength
            elif pitch_tie == 'start':
                Real_dur_upp = Real_dur_upp + current_event.quarterLength
                Upper_voice[current_event.offset]=[pitch_rest, current_event.measureNumber, current_event.offset, Real_dur_upp]
                Upper_voice.move_to_end(current_event.offset, last=False)
            else:
                Real_dur_upp = current_event.quarterLength
                Upper_voice[current_event.offset]=[pitch_rest, current_event.measureNumber, current_event.offset, Real_dur_upp]
                Upper_voice.move_to_end(current_event.offset, last=False)
        else:
            Real_dur_upp = current_event.quarterLength
            Upper_voice[current_event.offset]=[pitch_rest, current_event.measureNumber, current_event.offset, Real_dur_upp]
            Upper_voice.move_to_end(current_event.offset, last=False)

    for j in range (-L_1+1, 1):
        current_event = Parts[1][-j]
        pitch_rest = current_event.pitch if hasattr(current_event, "pitch") else "Rest"
        if pitch_rest != "Rest":
            pitch_tie = current_event.tie.type if isinstance(current_event.tie,tie.Tie) else None
            if pitch_tie == 'stop':
                Real_dur_low = current_event.quarterLength
            elif pitch_tie == 'continue':
                Real_dur_low = Real_dur_low + current_event.quarterLength
            elif pitch_tie == 'start':
                Real_dur_low = Real_dur_low + current_event.quarterLength
                Lower_voice[current_event.offset]=[pitch_rest, current_event.measureNumber, current_event.offset, Real_dur_low]
                Lower_voice.move_to_end(current_event.offset, last=False)
            else:
                Real_dur_low = current_event.quarterLength
                Lower_voice[current_event.offset]=[pitch_rest, current_event.measureNumber, current_event.offset, Real_dur_low]
                Lower_voice.move_to_end(current_event.offset, last=False)
        else:
            Real_dur_low = current_event.quarterLength
            Lower_voice[current_event.offset]=[pitch_rest, current_event.measureNumber, current_event.offset, Real_dur_low]
            Lower_voice.move_to_end(current_event.offset, last=False)

    Imitation_list = []
    L_upp = len(Upper_voice)
    L_low = len(Lower_voice)
    L = min(L_upp, L_low)

    for k in Time:

        if k<0:
            Emplacement = " before"
            Distance = " below"
        else:
            Emplacement = " after"
            Distance = " above"

        if list(Lower_voice.keys())[0] + k in Upper_voice:
            I = DiagInterval(Lower_voice[list(Lower_voice.items())[0][0]][0], Upper_voice[list(Lower_voice.items())[0][0]+k][0])
            D = Lower_voice[0][3]
            Init = Lower_voice[list(Lower_voice.items())[0][0]][1]
            Len = Lower_voice[list(Lower_voice.items())[0][0]][2]
        else:
            I = None
            D = 0
            Init = None
            Len = 0
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
                                Imitation[-1][7] = D/abs(k)
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
                            Imitation[-1][7] = D/abs(k)
                    else:
                        pass
                    B = 0
            else:
                if list(Lower_voice.keys())[l] + k in Upper_voice:
                    if Upper_voice[list(Lower_voice.items())[l][0]+k][0] == 'Rest':
                        if Imitation != []:
                            if Imitation[-1][5] != None:
                                pass
                            else:
                                Imitation[-1][1] = Lower_voice[list(Lower_voice.items())[l][0]][1]
                                Imitation[-1][4] = Lower_voice[list(Lower_voice.items())[l][0]][2] - Imitation[-1][4]
                                Imitation[-1][5] = B
                                Imitation[-1][7] = D/abs(k)
                        else:
                            pass
                        B = 0
                    elif Lower_voice[list(Lower_voice.items())[l][0]][3] == Upper_voice[list(Lower_voice.items())[l][0]+k][3]:
                        if DiagInterval(Lower_voice[list(Lower_voice.items())[l][0]][0],Upper_voice[list(Lower_voice.items())[l][0]+k][0]) == I:
                            B = B+1
                            if B == 2:
                                Imitation.append([Init, None, Values[abs(k)] + Emplacement, I.split()[1] + Distance, Len, None, abs(k), None])
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
                                    Imitation[-1][7] = D/abs(k)
                            else:
                                pass
                            B = 0
                            I = DiagInterval(Lower_voice[list(Lower_voice.items())[l][0]][0], Upper_voice[list(Lower_voice.items())[l][0]+k][0])
                            D = Lower_voice[list(Lower_voice.items())[l][0]][3]
                            Init = Lower_voice[list(Lower_voice.items())[l][0]][1]
                            Lower_voice[list(Lower_voice.items())[l][0]][2]
                            Len = Lower_voice[list(Lower_voice.items())[l][0]][2]
                    else:
                        if Imitation != []:
                            if Imitation[-1][5] != None:
                                pass
                            else:
                                Imitation[-1][1] = Lower_voice[list(Lower_voice.items())[l][0]][1]
                                Imitation[-1][4] = Lower_voice[list(Lower_voice.items())[l][0]][2] - Imitation[-1][4]
                                Imitation[-1][5] = B
                                Imitation[-1][7] = D/abs(k)
                        else:
                            pass
                        B = 0
                        I = None
                        D = 0
                        Init = None
                        Len = 0
                else:
                    if Imitation != []:
                        if Imitation[-1][5] != None:
                            pass
                        else:
                            Imitation[-1][1] = Lower_voice[list(Lower_voice.items())[l][0]][1]
                            Imitation[-1][4] = Lower_voice[list(Lower_voice.items())[l][0]][2] - Imitation[-1][4]
                            Imitation[-1][5] = B
                            Imitation[-1][7] = D/abs(k)
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
                Imitation[-1][7] = D/abs(k)
                Imitation_list.append(Imitation)
                Imitation = []
        else:
            pass
        B = 0
    return Imitation_list


def Imitation_Parameters(filename):
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
                LI_List.append([Imitation[0], Imitation[1], Imitation[2], Imitation[3], round(Imitation[4]),round(Imitation[4]/Piece.asTimespans()[-1].offset*100), round(Imitation[5]/Imitation[4],2), Stretto_Fuga_detector(round(Imitation[4]), Imitation[6], round(Imitation[4]/Piece.asTimespans()[-1].offset*100), Imitation[2])])
    return LI_List

if __name__ == '__main__':
    LoadCorpora(load_josquin=True, load_larue=True)
    li_list = []
    li_CSV_data = [['Composer', 'Piece', 'Movement', 'Initial measure', 'Final measure', 'Time interval of imitation', 'Pitch interval of imitation', 'Absolute length', 'Relative length', 'Density', 'Characteristics']]
    for f in corpus.getLocalPaths():
        li_list.append(Imitation_Parameters(f))
    for piece in li_list:
        metadata = piece[0]
        for li in piece[1:]:
            li_csv_str = '{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}'.format(metadata[0], metadata[1], metadata[2], li[0], li[1], li[2], li[3], li[4], li[5], li[6], li[7])
            li_CSV_data.append(li_csv_str.split(','))
    with open('Imitation_Test.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(li_CSV_data)
    csvFile.close()
