import re
import mido as md

# TODO: fazer Music representar tanto um MIDI ja gravado,
# quanto um MIDI futuro. Utilizar tanto em Rules quanto aqui
class Music:
    def __init__(self, filename):
        self.filename = filename
        self.file = md.MidiFile(filename)
        self.length = 0

    def calc_length(self):
        pass

class TextConverter:
    """
    TextConverter: transforma uma string em um arquivo MIDI
    
    O objetivo dessa classe é transformar uma string de entrada
    em um arquivo MIDI de saída utilizando as regras de tranformação
    de string fornecida por Rules.
    """
    def __init__(self, input, rules, midiFile):
        self.input = input
        self.rules = rules
        self.mid = midiFile

    def setInput(self, input):
        self.input = input

    def setRules(self, rules):
        self.rules = rules

    def compose(self):
        track = md.MidiTrack()
        self.mid.tracks.append(track)

        # Apply initial settings
        for msg in self.rules.initial_msgs():
            print(msg)
            track.append(msg)

        # Build regex from Rules
        keys_regex = '|'.join(re.escape(key) for key in self.rules.mappings.keys())
        regex_pattern = f'({keys_regex})'

        tmp = self.input
        while tmp:
            # Get first match
            match = re.match(regex_pattern, tmp)
            group = match.group()

            # Apply Rule
            msgs = self.rules.mappings[group]()()

            # Append Messages
            for msg in msgs:
                print(msg)
                track.append(msg)

            # Reduce string
            i = len(group) if len(group) > 0 else 1
            tmp = tmp[i:]

        self.mid.save("sample.mid")
