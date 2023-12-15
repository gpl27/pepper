# Pepper's Private Band
# 
from mido import MidiFile
import pygame

class Music():
    def __init__(self, filename):
        self.filename = filename
        self.file = MidiFile(filename)
        self.length = 0

    def calc_length(self):
        pass

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
    def __init__(self, music):
        self.music = music
        freq = 44100    # audio CD quality
        bitsize = -16   # unsigned 16 bit
        channels = 2    # 1 is mono, 2 is stereo
        buffer = 1024    # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffer)
        pygame.mixer.music.set_volume(0.8) # optional volume 0 to 1.0

    def playback(self):
        clock = pygame.time.Clock()
        pygame.mixer.music.load(self.music.filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            # check if playback has finished
            clock.tick(30)
        pygame.mixer.music.unload()
        return

    def record(self):
        pass


music = Music("test.mid")
recorder = Recorder(music)
recorder.playback()