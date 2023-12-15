import mido as md
from textprocessing import TextConverter, Music
from AudioConverter import AudioConverter
from Rules import Rules

mid = md.MidiFile()
rules = Rules(mid, 100, 127, 4)
converter = TextConverter(r'ABCDEFGBPM+abcdR+bdd', rules, mid)
converter.compose()
music = Music("sample.mid")
recorder = AudioConverter(music)
recorder.playback()