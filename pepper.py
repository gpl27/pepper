# Pepper's Private Band
# 


class Composer():
    """
    Composer: transforma uma string em um arquivo MIDI
    
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


class Recorder():
    """
    Recorder: transforma um arquivo MIDI em audio

    O objetivo dessa classe é transformar um arquivo MIDI      
    ou em uma gravação de audio, ou em um playback em tempo
    real
    """
    def __init__(self, MIDIFile):
        self.MIDIFile = MIDIFile

    def setMIDIFile(self, MIDIFILE):
        self.MIDIFile = MIDIFILE

    def playback(self):
        pass

    def record(self):
        pass