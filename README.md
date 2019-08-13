# Imitation_Analyzer
This program detects imitations between instrumental voices. It takes MusicXML files as inputs and returns a CVS file as an output using music21.


## Description
IMAN (for IMitation ANalyzer) is a program developed in 2019 by Sylvain Margot, in collaboration with Néstor Nápoles López and Laurent Feisthauer. It works in python3, using music21. <br /> <br /> This program detects imitations within Josquin\'s and La Rue\'s masses duos. An imitation can be sub-divided into two parts: the fragment (the part that is melodically exactly imitated) and the core (the part that is melodically and rhythmically exactly imitated). These two parts often coincide, but not always. <br /> <br /> For each imitation, the program outputs several datas:<br />   - where it begins and where it ends in both voices (float, "measure.semiminim"),<br />   - its time interval of imitation (float, "in semiminims"),<br />   - its pitch interval of imitation (string, "diatonic interval"),<br />   - the length of its core (float, "in semiminims"),<br />   -the number of notes (integer, "number of notes"),<br />   - the length of the piece (float, "in semiminims"),<br />   - its rhythmic density (float, "an average of 1 would correspond to a fragment made of semiminims only, an average of 0.5 to a fragment made of minims only, etc.),<br />   - and finally its characteristic (string, "Depending on the length of its core and its time interval of imitation, an imitation can be considered as a Stretto Fuga, Canonic piece, Stretto Fuga canonic piece, or as a simple imitation"). <br /> <br /> The program takes as inputs:<br />   - a Canon_threshold (integer, "the minimum ratio between an imitation and its piece to consider the lattest as a canon"),<br />   - a Notes_threshold (integer, "the minimum amount of notes in the imitation core to keep record of it"),<br />   - a Duration_threshold (float, "the minimum duration of the imitation core to keep record of it (in semiminims)"), <br />   - Corpora (list of strings, "the name of the corpora we consider"), <br />   - and a File_name (string, "the name of the .csv file we want as a final result")<br /> <br /> The program is composed of six sub-programs: <br /> 1. the Continuous_Part sub-program - It returns a instrumental part as a string of events. All tied notes are reduced to a single note with its real duration (Real_dur) <br /> 2. the Diag_Interval sub-program - It returns the melodic interval between two events if they are both notes, or returns "Rest" if at least one of the events is a rest <br /> 3. the Stretto_Fuga_Detector sub-program. It classifies an imitation as a Stretto Fuga, a canonic piece, or a Stretto Fuga canonic piece according to its Time Interval and the length of its core <br /> 4. the Load_Corpora sub-program - It loads the corpora you want to analyze <br /> 5. the Imitation_Detector sub-program - It detects all imitations between two instrumental parts <br /> 6. the Imitation_Parameters sub-program - It classifies and arranges the results according to our musicological needs

The code here requires the `music21`, `os`, `csv`, `argparse`, and `numpy` python packages

## Running the code
Clone the repository recursively (this is necessary for getting the `mass-duos-corpus-josquin-larue`, containing the data)

```
git clone https://github.com/ELVIS-Project/Imitation_Analyzer --recursive
```

Run the Stretto Fuga Finder script
```
python Stretto_Fuga_Finder.py
```

