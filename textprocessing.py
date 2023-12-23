import re
import mido as md

# TODO: fazer Music representar tanto um MIDI ja gravado,
# quanto um MIDI futuro. Utilizar tanto em Rules quanto aqui
class Music:
    """
    Music: representa uma música genérica.

    Music pode ser tanto um arquivo MIDI já gravado quanto um
    MIDI que será gravado
    """
    def __init__(self, filename=None):
        self.filename = filename
        if filename:
            self.mid = md.MidiFile(filename)
        else:
            self.mid = md.MidiFile()
        self.length = 0

    def save(self, filename):
        self.filename = filename
        self.mid.save(filename)
    
    def get_ticks(self):
        return self.mid.ticks_per_beat

    def calc_length(self):
        pass

class TextConverter:
    """
    TextConverter: transforma uma string em um arquivo MIDI
    
    O objetivo dessa classe é transformar uma string de entrada
    em um arquivo MIDI de saída utilizando as regras de tranformação
    de string fornecida por Rules.
    """
    def __init__(self, input, rules):
        self.input = input
        self.rules = rules

    def setInput(self, input):
        self.input = input

    def setRules(self, rules):
        self.rules = rules

    def compose(self, music):
        track = md.MidiTrack()
        music.mid.tracks.append(track)

        # Apply initial settings
        for msg in self.rules.initial_msgs():
            print(msg)
            track.append(msg)

        # Build regex from Rules
        keys = self.rules.get_keys()
        regex_pattern = '|'.join(re.escape(key) for key in keys)

        tmp = self.input
        while tmp:
            # Get first match
            match = re.match(regex_pattern, tmp)
            group = match.group()

            # Apply Rule
            msgs = self.rules.get_msgs(group)

            # Append Messages
            for msg in msgs:
                print(msg)
                track.append(msg)

            # Reduce string
            i = len(group) if len(group) > 0 else 1
            tmp = tmp[i:]

