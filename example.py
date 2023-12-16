import mido as md
from textprocessing import TextConverter, Music
from AudioConverter import AudioConverter
from Rules import Rules

music = Music()
rules = Rules(music, 120, 64, 4, 0)
converter = TextConverter('O fueoefdgfdc BPM++abcdR+bdd-R-;abababcde', rules)
converter.compose(music)
music.save("sample.mid")
recorder = AudioConverter(music)
recorder.playback()