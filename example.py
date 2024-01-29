from textprocessing import TextConverter, Music, Rules
from AudioConverter import AudioConverter

music = Music()
rules = Rules(music.get_ticks(), 120, 64, 4, 0)
converter = TextConverter('O fueoefdgfdc BPM++abcdR+bdd-R-;abababcde', rules)
converter.compose(music)
music.save("sample.mid")
recorder = AudioConverter(music)
recorder.playback()
while recorder.is_playing():
    pass