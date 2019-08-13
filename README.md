# Imitation Analyzer (IMAN)
This program detects imitations between instrumental voices. It takes MusicXML files as inputs and returns a CVS file as an output using music21.


## Description
IMAN (for IMitation ANalyzer) is a program developed in 2019 by Sylvain Margot, in collaboration with Néstor Nápoles López and Laurent Feisthauer. It works in python3, using music21. <br /> <br /> This program detects imitations within Josquin\'s and La Rue\'s masses duos. An imitation can be sub-divided into two parts: the fragment (the part that is melodically exactly imitated) and the core (the part that is melodically and rhythmically exactly imitated). These two parts often coincide, but not always.

For each imitation, the program outputs several datas:
- where it begins and where it ends in both voices (measure.semiminim),
- its time interval of imitation (in semiminims),
- its pitch interval of imitation (as a diatonic interval),
- the length of its core (in semiminims),
- the number of notes (number of notes),
- the length of the piece (in semiminims),
- its rhythmic density (an average of 1 would correspond to a fragment made of semiminims only, an average of 0.5 to a fragment made of minims only, etc.),   
- and its characteristic (depending on the length of its core and its time interval of imitation, an imitation can be considered as a Stretto Fuga, Canonic piece, Stretto Fuga canonic piece, or as a simple imitation).

The program takes as inputs:
- a Canon_threshold (integer) - the minimum ratio between an imitation and its piece to consider the lattest as a canon (in percentage),
- a Notes_threshold (integer) - the minimum amount of notes in the imitation core to keep record of it,
- a Duration_threshold (float) - the minimum duration of the imitation core to keep record of it (in semiminims),
- a File_name (string) - the name of the .csv file we want as a final result,
- and Corpora (list of strings) - the name of the corpora we consider,

The program is composed of six sub-programs:
1. the Continuous_Part sub-program - returns a instrumental part as a string of events. All tied notes are reduced to a single note with its real duration (Real_dur)
2. the Diag_Interval sub-program - returns the melodic interval between two events if they are both notes, or returns "Rest" if at least one of the events is a rest
3. the Stretto_Fuga_Detector sub-program - classifies an imitation as a Stretto Fuga, a canonic piece, or a Stretto Fuga canonic piece according to its Time Interval and the length of its core
4. the Load_Corpora sub-program - loads the corpora you want to analyze
5. the Imitation_Detector sub-program - detects all imitations between two instrumental parts
6. the Imitation_Parameters sub-program - classifies and arranges the results according to our musicological needs

The code here requires the `music21`, `sys`, `os`, `csv`, `argparse`, and `numpy` python packages


## Running the code
Clone the repository recursively (this is necessary for getting the `mass-duos-corpus-josquin-larue`, containing the data)

```
git clone https://github.com/ELVIS-Project/Imitation_Analyzer --recursive
```

Run the Stretto Fuga Finder script
```
python3 Imitation_Analyzer.py Canon_threshold Notes_threshold Duration_threshold File_name Corpora
```

