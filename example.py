import mido as md
from textprocessing import TextConverter, Music
from AudioConverter import AudioConverter
from Rules import Rules

mid = md.MidiFile()
rules = Rules(mid, 120, 64, 4)
converter = TextConverter('O fueoefdgfdc BPM++abcdR+bdd-R-;abababcde', rules, mid)
converter.compose()
music = Music("sample.mid")
recorder = AudioConverter(music)
recorder.playback()