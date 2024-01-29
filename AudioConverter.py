import pygame

class AudioConverter:
    """
    AudioConverter: transforma um arquivo MIDI em audio

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
        pygame.mixer.music.load(self.music.filename)

    def playback(self):
        pygame.mixer.music.play()

    def is_playing(self):
        return pygame.mixer.music.get_busy()

    def pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def restart(self):
        pygame.mixer.music.rewind()