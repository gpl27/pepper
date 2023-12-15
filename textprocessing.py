from AudioConverter import AudioConverter
from mido import MidiFile

class Music:
    def __init__(self, filename):
        self.filename = filename
        self.file = MidiFile(filename)
        self.length = 0

    def calc_length(self):
        pass

class TextConverter:
    """
    TextConverter: transforma uma string em um arquivo MIDI
    
    O objetivo dessa classe é transformar uma string de entrada
    em um arquivo MIDI de saída utilizando as regras de tranformação
    de string fornecidas junto com a string
    """
    def __init__(self, input, rules):
        self.input = input
        self.rules = rules

    def setInput(self, input):
        self.input = input

    def setRules(self, rules):
        self.rules = rules

    def compose(self):
        pass

music = Music("test.mid")
recorder = AudioConverter(music)
recorder.playback()