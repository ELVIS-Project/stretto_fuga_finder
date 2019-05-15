from music21 import *
import numpy as np
from operator import itemgetter

Josquin_secure_corpus=corpus.corpora.LocalCorpus()
Josquin_secure_corpus.addPath('../Mass duos Josquin - De La Rue/Josquin (secure)/XML')
Agnus_2=corpus.parse('XML/Josquin Missa Ave maris stella - Agnus II.xml')
Agnus_2_Parts=instrument.partitionByInstrument(Agnus_2)

Upper_voice=[]
Lower_voice=[]

for Notes_Upper_voice in Agnus_2_Parts.parts['Soprano'].getElementsByClass(note.Note):
    Upper_voice.append([Notes_Upper_voice, Notes_Upper_voice.offset])

for Rests_Upper_voice in Agnus_2_Parts.parts['Soprano'].getElementsByClass(note.Rest):
    Upper_voice.append([Rests_Upper_voice, Rests_Upper_voice.offset])

Upper_voice=sorted(Upper_voice,key=itemgetter(1))

for Notes_Lower_voice in Agnus_2_Parts.parts['Tenor'].getElementsByClass(note.Note):
    Lower_voice.append([Notes_Lower_voice, Notes_Lower_voice.offset])

for Rests_Lower_voice in Agnus_2_Parts.parts['Tenor'].getElementsByClass(note.Rest):
    Lower_voice.append([Rests_Lower_voice, Rests_Lower_voice.offset])

Lower_voice=sorted(Lower_voice,key=itemgetter(1))

L=len(Lower_voice)

for i in range (0,L):
    try:
        interval.notesToChromatic(Lower_voice[i][0],Upper_voice[i+1][0])
    except:
        print("<music21.interval.ChromaticInterval 0>")
    else:
        print(interval.notesToChromatic(Lower_voice[i][0],Upper_voice[i+1][0]))
