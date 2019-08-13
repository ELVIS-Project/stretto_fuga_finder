import numpy as np
import os
import csv
import argparse
from music21 import *
from collections import OrderedDict



'''IMAN (for IMitation ANalyzer) is a program developed in 2019 by Sylvain Margot, in collaboration with Néstor Nápoles López and Laurent Feisthauer. \n \n This program detects imitations within Josquin\'s and La Rue\'s masses duos. \n \n An imitation can be sub-divided into two parts: the fragment (the part that is melodically exactly imitated) and the core (the part that is melodically and rhythmically exactly imitated). These two parts often coincide, but not always. For each imitation, the program outputs several datas: where it begins and where it ends in both voices (float, "measure.semiminim"), its time interval of imitation (float, "in semiminims"), its pitch interval of imitation (string, "diatonic interval"), the length of its core (float, "in semiminims"), the number of notes (integer, "number of notes"), the length of the piece (float, "in semiminims"), its rhythmic density (float, "an average of 1 would correspond to a fragment made of semiminims only, an average of 0.5 to a fragment made of minims only, etc.), and finally its characteristic (string, "Depending on the length of its core and its time interval of imitation, an imitation can be considered as a Stretto Fuga, Canonic piece, Stretto Fuga canonic piece, or as a simple imitation"). \n The program takes as inputs a Canon_threshold (integer, "the minimum ratio between an imitation and its piece to consider the lattest as a canon"), a Notes_threshold (integer, "the minimum amount of notes in the imitation core to keep record of it"), a Duration_threshold (float, "the minimum duration of the imitation core to keep record of it (in semiminims)"), Corpora (list of strings, "the name of the corpora we consider"), and a File_name (string, "the name of the .csv file we want as a final result")\n \n The program is composed of six sub-programs: \n 1) the Continuous_Part sub-program - It returns a instrumental part as a string of events. All tied notes are reduced to a single note with its real duration (Real_dur) \n 2) the Diag_Interval sub-program - It returns the melodic interval between two events if they are both notes, or returns "Rest" if at least one of the events is a rest \n 3) the Stretto_Fuga_Detector sub-program. It classifies an imitation as a Stretto Fuga, a canonic piece, or a Stretto Fuga canonic piece according to its Time Interval and the length of its core \n 4) the Load_Corpora sub-program - It loads the corpora you want to analyze \n 5) the Imitation_Detector sub-program - It detects all imitations between two instrumental parts \n 6) the Imitation_Parameters sub-program - It classifies and arranges the results according to our musicological needs'''



parser = argparse.ArgumentParser(
    prog='Imitation_Analyzer',
    description = 'This program detects imitations between instrumental voices. It takes MusicXML files as inputs and returns a CVS file as an output using music21.')
parser.add_argument('float', metavar='Canon_threshold', type=float, help='The minimum ratio between an imitation and its piece to consider the lattest as a canon in percentage (float)')
parser.add_argument('integer', metavar='Notes_threshold', type=int, help='The minimum amount of notes in the imitation core to keep record of it (integer)')
parser.add_argument('integer', metavar='Duration_threshold', type=int, help='The minimum duration of the imitation core to keep record of it in semiminims (integer)')
parser.add_argument('list of strings', metavar='Corpora', type=list, help='The name of the corpora we consider (list of strings)')
parser.add_argument('string', metavar='File_name', type=str, help='The name of the .csv file we want as a final result (string)')
args = parser.parse_args()


def Imitation_Analyzer(Canon_threshold, Notes_threshold, Duration_threshold, Corpora, File_name):
    '''Imitation_Analyzer centralizes the execution of the sub-programs, the parameters inputs, and the output of results as a .csv file'''

    if __name__ == '__main__':
        Load_Corpora(Corpora)
        Corpora_imitations = []
        Piece_CSV_data = [['Composer', 'Piece', 'Movement', 'Beginning of the imitation at the lower voice', 'End of the imitation at the lower voice', 'Beginning of the imitation at the upper voice', 'End of the imitation at the upper voice', 'Time interval of imitation (in semi-minims)', 'Pitch interval of imitation', 'Length of the core (in semi-minims)', 'Length of the fragment (number of notes)', 'Length of the piece (in semi-minims)', 'Rhythmic density', 'Characteristics']]
        for file in corpus.getLocalPaths():
            Corpora_imitations.append(Imitation_Parameters(Canon_threshold, Notes_threshold, Duration_threshold, file))
        for score in Corpora_imitations:
            metadata = score[0]
            for li in score[1:]:
                Piece_csv_str = '{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}'.format(metadata[0], metadata[1], metadata[2], li[0], li[1], li[2], li[3], li[4], li[5], li[6], li[7], li[8], li[9], li[10])
                Piece_CSV_data.append(Piece_csv_str.split(','))
        with open(File_name, 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(Piece_CSV_data)
        csvFile.close()



def Continuous_Part(part):
    ''' Continuous_Part returns a instrumental part as a string of events. All tied notes are reduced to a single note with its real duration (Real_dur). '''

    Real_dur = 0
    Voice = OrderedDict([])

    for i in range (-len(part)+1, 1): #Because the real duration of a tied note is attributed to the first one but is determined by the following ones, it is easier to proceed backwards
        current_event = part[-i]
        pitch_rest = current_event.pitch if hasattr(current_event, "pitch") else "Rest"
        if pitch_rest != "Rest":
            pitch_tie = current_event.tie.type if isinstance(current_event.tie,tie.Tie) else None
            if pitch_tie == 'stop':
                Real_dur = current_event.quarterLength
            elif pitch_tie == 'continue':
                Real_dur = Real_dur + current_event.quarterLength
            elif pitch_tie == 'start':
                Real_dur = Real_dur + current_event.quarterLength
                Voice[current_event.offset]=[pitch_rest, current_event.measureNumber + (current_event.beat*4-3)/10, current_event.offset, Real_dur] #For each event, we keep its pitch/rest properties, its relative position within the piece (under the float format measure.semiminim), its absolute position within the piece (in semiminims) and its real duration (if the note is tied)
                Voice.move_to_end(current_event.offset, last=False) #Because we proceed backwards, each new event must be pushed at the beginning of the list
            else:
                Real_dur = current_event.quarterLength
                Voice[current_event.offset]=[pitch_rest, current_event.measureNumber + (current_event.beat*4-3)/10, current_event.offset, Real_dur]
                Voice.move_to_end(current_event.offset, last=False) #Because we proceed backwards, each new event must be pushed at the beginning of the list
        else:
            Real_dur = current_event.quarterLength
            Voice[current_event.offset]=[pitch_rest, current_event.measureNumber + (current_event.beat*4-3)/10, current_event.offset, Real_dur]
            Voice.move_to_end(current_event.offset, last=False)
    return(Voice)



def Diag_Interval(event_1,event_2):
    ''' Diag_Interval returns the melodic interval between two events if they are both notes. Returns 'Rest' if at least one of the events is a rest '''

    if event_1 == 'Rest':
        return 'Rest'
    elif event_2 == 'Rest':
        return 'Rest'
    else:
        return interval.Interval(event_1,event_2).directedNiceName.split()[0]+" "+interval.Interval(event_1,event_2).directedNiceName.split()[2]



def Stretto_Fuga_Detector(Canon_threshold, Core_length, Time_interval, Core_proportional_length):
    ''' Stretto_Fuga_Detector classifies an imitation as a Stretto Fuga, a canonic piece, or a Stretto Fuga canonic piece according to its Time Interval and the length of its core '''

    if Core_length > abs(Time_interval): #To be defined as a Stretto Fuga (and obviously a canon), the imitated core must overlap the imitation
        if Core_proportional_length >= Canon_threshold:
            if abs(Time_interval) in [2,3,4,6,8]: #Stretto Fuga can be at the minim, the dotted minim, the semibreve, the dotted semibreve, or the longa
                return "Stretto Fuga Canonic Piece"
            else:
                return "Canonic Piece"
        else:
            if abs(Time_interval) in [2,3,4,6,8]: #Stretto Fuga can be at the minim, the dotted minim, the semibreve, the dotted semibreve, or the longa
                return "Stretto Fuga"
            else:
                return " "
    else:
        return " "



def Load_Corpora(Corpora):
    ''' Load_Corpora loads the corpora to study and returns an error message if one of them does not exist '''

    for set_of_pieces in Corpora:
        if set_of_pieces == 'Josquin (secure)':
            corpus.addPath('./mass-duos-corpus-josquin-larue/Josquin (secure)/XML')
        elif set_of_pieces == 'La Rue (secure)':
            corpus.addPath('./mass-duos-corpus-josquin-larue/La Rue (secure)/XML')
        elif set_of_pieces == 'Josquin (not secure)':
            corpus.addPath('./mass-duos-corpus-josquin-larue/Josquin (not secure)/XML')
        elif set_of_pieces == 'La Rue (not secure)':
            corpus.addPath('./mass-duos-corpus-josquin-larue/La Rue (unsecure)/XML')
        elif set_of_pieces == 'Test':
            corpus.addPath('./mass-duos-corpus-josquin-larue/Test/XML')
        else:
            print(set_of_pieces, ': Unknown Corpus')



def Imitation_Detector(Notes_threshold, score):
    ''' Imitation_Detector detects all imitations between two parts '''

    Length_piece = int(score.asTimespans()[-1].offset)

    Parts = [p.flat.notesAndRests.stream() for p in score.parts]
    Upper_voice = Continuous_Part(Parts[0])
    Lower_voice = Continuous_Part(Parts[1])

    Imitation_list = [] #Imitation_list[] collects all the imitations within a single piece

    for Time_interval in [x for x in range(-Length_piece,Length_piece) if x != 0]:

        Imitation = [] #Imitation[] collects the imitations for a given time interval

        if list(Lower_voice.keys())[0] + Time_interval in Upper_voice: #if the imitation begins with the beginning of the lowest voice
            Interval = Diag_Interval(Lower_voice[list(Lower_voice.items())[0][0]][0], Upper_voice[list(Lower_voice.items())[0][0] + Time_interval][0])
            Initial_measure_low_voice = Lower_voice[list(Lower_voice.items())[0][0]][1]
            Initial_measure_upp_voice = Upper_voice[list(Lower_voice.items())[0][0] + Time_interval][1]
            Core_first_offset = Lower_voice[list(Lower_voice.items())[0][0]][2]
            Number_of_notes = 1
            if Lower_voice[list(Lower_voice.items())[0][0]][3] == Upper_voice[list(Lower_voice.items())[0][0] + Time_interval][3]:
                Notes_in_core = 1
            else:
                Notes_in_core = 0
        else:
            Interval = None
            Initial_measure_low_voice = None
            Initial_measure_upp_voice = None
            Core_first_offset = 0
            Number_of_notes = 0
            Notes_in_core = 0

        for Event_number in range (0,len(Lower_voice)-1): #for each note of the lower voice

            if Lower_voice[list(Lower_voice.items())[Event_number][0]][0] == 'Rest': #if the lower voice event is a rest
                if list(Lower_voice.keys())[Event_number] + Time_interval in Upper_voice:
                    if Upper_voice[list(Lower_voice.items())[Event_number][0] + Time_interval][0] == 'Rest': #an imitation can include rests
                        pass
                    else:
                        if Imitation != []:
                            if Imitation[-1][7] != None: #if there was no running imitation
                                pass
                            else: #if there was a running imitation, stops at the previous event
                                Imitation[-1][1] = Lower_voice[list(Lower_voice.items())[Event_number - 1][0]][1]
                                Imitation[-1][3] = Upper_voice[list(Lower_voice.items())[Event_number - 1][0] + Time_interval][1]
                                Imitation[-1][6] = Lower_voice[list(Lower_voice.items())[Event_number][0]][2] - Imitation[-1][6]
                                Imitation[-1][7] = Number_of_notes
                        else:
                            pass
                        #reinitialize the imitation
                        Interval = None
                        Initial_measure_low_voice = None
                        Initial_measure_upp_voice = None
                        Core_first_offset = 0
                        Number_of_notes = 0
                        Notes_in_core = 0
                else:
                    if Imitation != []:
                        if Imitation[-1][7] != None: #if there was no running imitation
                            pass
                        else: #if there was a running imitation, stops at the previous event
                            Imitation[-1][1] = Lower_voice[list(Lower_voice.items())[Event_number - 1][0]][1]
                            Imitation[-1][3] = Upper_voice[list(Lower_voice.items())[Event_number - 1][0] + Time_interval][1]
                            Imitation[-1][6] = Lower_voice[list(Lower_voice.items())[Event_number][0]][2] - Imitation[-1][6]
                            Imitation[-1][7] = Number_of_notes
                    else:
                        pass
                    #reinitialize the imitation
                    Interval = None
                    Initial_measure_low_voice = None
                    Initial_measure_upp_voice = None
                    Core_first_offset = 0
                    Number_of_notes = 0
                    Notes_in_core = 0

            else:
                if list(Lower_voice.keys())[Event_number] + Time_interval in Upper_voice: #if the lower voice event is a note
                    if Upper_voice[list(Lower_voice.items())[Event_number][0]+Time_interval][0] == 'Rest':
                        if Imitation != []:
                            if Imitation[-1][7] != None: #if there was no running imitation
                                pass
                            else: #if there was a running imitation, stops at the previous event
                                Imitation[-1][1] = Lower_voice[list(Lower_voice.items())[Event_number - 1][0]][1]
                                Imitation[-1][3] = Upper_voice[list(Lower_voice.items())[Event_number - 1][0] + Time_interval][1]
                                Imitation[-1][6] = Lower_voice[list(Lower_voice.items())[Event_number][0]][2] - Imitation[-1][6]
                                Imitation[-1][7] = Number_of_notes
                        else:
                            pass
                        #reinitialize the imitation
                        Interval = None
                        Initial_measure_low_voice = None
                        Initial_measure_upp_voice = None
                        Core_first_offset = 0
                        Number_of_notes = 0
                        Notes_in_core = 0

                    elif Lower_voice[list(Lower_voice.items())[Event_number][0]][3] == Upper_voice[list(Lower_voice.items())[Event_number][0] + Time_interval][3]:  #if the rhythmic value of the two notes is the same
                        if Diag_Interval(Lower_voice[list(Lower_voice.items())[Event_number][0]][0],Upper_voice[list(Lower_voice.items())[Event_number][0] + Time_interval][0]) == Interval: #if the interval between the two notes is the pitch imitation interval
                            Number_of_notes = Number_of_notes + 1
                            Notes_in_core = Notes_in_core + 1
                            if Notes_in_core == Notes_threshold:
                                Imitation.append([Initial_measure_low_voice, None, Initial_measure_upp_voice, None, abs(Time_interval), Interval.split()[1], Core_first_offset, None])
                            else:
                                pass
                        else:
                            if Imitation != []:
                                if Imitation[-1][7] != None: #if there was no running imitation
                                    pass
                                else: #if there was a running imitation, stops at the previous event
                                    Imitation[-1][1] = Lower_voice[list(Lower_voice.items())[Event_number - 1][0]][1]
                                    Imitation[-1][3] = Upper_voice[list(Lower_voice.items())[Event_number - 1][0] + Time_interval][1]
                                    Imitation[-1][6] = Lower_voice[list(Lower_voice.items())[Event_number][0]][2] - Imitation[-1][6]
                                    Imitation[-1][7] = Number_of_notes
                            else:
                                pass
                            #reinitialize the imitation with the new pitch interval of imitation
                            Interval = Diag_Interval(Lower_voice[list(Lower_voice.items())[Event_number][0]][0], Upper_voice[list(Lower_voice.items())[Event_number][0] + Time_interval][0])
                            Core_first_offset = Lower_voice[list(Lower_voice.items())[Event_number][0]][2]
                            Number_of_notes = 1
                            Notes_in_core = 1
                            Initial_measure_low_voice = Lower_voice[list(Lower_voice.items())[Event_number][0]][1]
                            Initial_measure_upp_voice = Upper_voice[list(Lower_voice.items())[Event_number][0] + Time_interval][1]

                            if list(Upper_voice).index(list(Lower_voice.items())[Event_number][0] + Time_interval) - 1 in Upper_voice : #depending on what preceeds it, an imitation can begin with a different rhythmic value than what it imitates
                                if Diag_Interval(Lower_voice[list(Lower_voice.items())[Event_number - 1][0]][0],list(Upper_voice.items())[list(Upper_voice).index(list(Lower_voice.items())[Event_number][0] + Time_interval) - 1][1][0]) == Interval:
                                    Number_of_notes = 2
                                    Initial_measure_low_voice = Lower_voice[list(Lower_voice.items())[Event_number - 1][0]][1]
                                    Initial_measure_upp_voice = list(Upper_voice.items())[list(Upper_voice).index(list(Lower_voice.items())[Event_number][0] + Time_interval) - 1][1][1]
                                else:
                                    pass
                            else:
                                pass

                    elif Diag_Interval(Lower_voice[list(Lower_voice.items())[Event_number][0]][0], Upper_voice[list(Lower_voice.items())[Event_number][0] + Time_interval][0]) == Interval: #depending on what follows it, an imitation can end with a different rhythmic value than what it imitates
                        Number_of_notes = Number_of_notes+1
                        if Imitation != []:
                            if Imitation[-1][7] != None: #if there was no running imitation
                                pass
                            else: #if there was a running imitation, stops at the current event
                                Imitation[-1][1] = Lower_voice[list(Lower_voice.items())[Event_number][0]][1]
                                Imitation[-1][3] = Upper_voice[list(Lower_voice.items())[Event_number][0] + Time_interval][1]
                                Imitation[-1][6] = Lower_voice[list(Lower_voice.items())[Event_number][0]][2] - Imitation[-1][6]
                                Imitation[-1][7] = Number_of_notes
                        else:
                            pass
                        #reinitialize the imitation
                        Number_of_notes = 0
                        Interval = None
                        Initial_measure_low_voice = None
                        Initial_measure_upp_voice = None
                        Core_first_offset = 0
                        Notes_in_core = 0

                    else:
                        if Imitation != []:
                            if Imitation[-1][7] != None: #if there was no running imitation
                                pass
                            else: #if there was a running imitation, stops at the current event
                                Imitation[-1][1] = Lower_voice[list(Lower_voice.items())[Event_number - 1][0]][1]
                                Imitation[-1][3] = Upper_voice[list(Lower_voice.items())[Event_number - 1][0] + Time_interval][1]
                                Imitation[-1][6] = Lower_voice[list(Lower_voice.items())[Event_number][0]][2] - Imitation[-1][6]
                                Imitation[-1][7] = Number_of_notes
                        else:
                            pass
                        #reinitialize the imitation
                        Number_of_notes = 0
                        Interval = None
                        Initial_measure_low_voice = None
                        Initial_measure_upp_voice = None
                        Core_first_offset = 0
                        Notes_in_core = 0
                else:
                    if Imitation != []:
                        if Imitation[-1][7] != None: #if there was no running imitation
                            pass
                        else: #if there was a running imitation, stops at the current event
                            Imitation[-1][1] = Lower_voice[list(Lower_voice.items())[Event_number - 1][0]][1]
                            Imitation[-1][3] = Upper_voice[list(Lower_voice.items())[Event_number - 1][0] + Time_interval][1]
                            Imitation[-1][6] = Lower_voice[list(Lower_voice.items())[Event_number][0]][2] - Imitation[-1][6]
                            Imitation[-1][7] = Number_of_notes
                    else:
                        pass
                    #reinitialize the imitation
                    Number_of_notes = 0
                    Interval = None
                    Initial_measure_low_voice = None
                    Initial_measure_upp_voice = None
                    Core_first_offset = 0
                    Notes_in_core = 0

        if Imitation != []:
            if Imitation[-1][7] != None:  #if there was no running imitation
                Imitation_list.append(Imitation)
            else: #if there was a running imitation, closes at the current string of events
                Imitation[-1][1] = Lower_voice[list(Lower_voice.items())[Event_number - 1][0]][1]
                Imitation[-1][3] = Upper_voice[list(Lower_voice.items())[Event_number - 1][0] + Time_interval][1]
                Imitation[-1][6] = Lower_voice[list(Lower_voice.items())[Event_number][0]][2] - Imitation[-1][6]
                Imitation[-1][7] = Number_of_notes
                Imitation_list.append(Imitation)
        else:
            pass
        #reinitialize the imitation
        Number_of_notes = 0
        Interval = None
        Initial_measure_low_voice = None
        Initial_measure_upp_voice = None
        Core_first_offset = 0
        Notes_in_core = 0

    return Imitation_list



def Imitation_Parameters(Canon_threshold, Notes_threshold, Duration_threshold, file):
    ''' Imitation_Parameters classifies and arranges the results according to our musicologic needs'''

    score=corpus.parse(file)
    Piece_imitations=[[score[2].content,score[1].content,score[0].content]]
    try:
        Imitation_Detector(Notes_threshold, score)
    except:
        Piece_imitations.append("Error")
        print(score[2].content,score[1].content,score[0].content)
    else:
        Imitation_list=Imitation_Detector(Notes_threshold, score)
        for Time_interval in Imitation_list:
            for Imitation in Time_interval:
                if Imitation[6]>=Duration_threshold:
                    Piece_imitations.append([Imitation[0], Imitation[1], Imitation[2], Imitation[3], Imitation[4], Imitation[5], round(Imitation[6]), Imitation[7], score.asTimespans()[-1].offset, round(Imitation[7]/Imitation[6],2), Stretto_Fuga_Detector(Canon_threshold, round(Imitation[6]), Imitation[4], round(Imitation[6]/score.asTimespans()[-1].offset*100))])
                else:
                    pass
    return Piece_imitations
