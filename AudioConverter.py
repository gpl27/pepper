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