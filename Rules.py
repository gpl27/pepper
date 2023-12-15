import random
import mido as md


class Rules:
    """
    Rules: o objetivo deste classe é mapear a transformação do texto
    para elementos musicais.

    Para Rules que possuem regras que são prefixo de outras, ordene
    em ordem de prioridade. O calculo de nota é feito relativo ao C1
    TODO
    encontrar um jeito de fazer apenas um nivel de currying
    """
    def __init__(self, midiFile, bpm, vol, octave):
        self.dur = midiFile.ticks_per_beat
        self.bpm = bpm
        self.default_vol = vol
        self.vol = self.default_vol
        self.octave = octave
        self.mappings = {
            'BPM+': lambda: self._bpm_adj(self.bpm+80),
            'R+': lambda: self._octave_adj(self.octave+1),
            'R-': lambda: self._octave_adj(self.octave-1),
            'A': lambda: self._add_note(self._calculate_midi_note('A')), 
            'B': lambda: self._add_note(self._calculate_midi_note('B')),
            'C': lambda: self._add_note(self._calculate_midi_note('C')),
            'D': lambda: self._add_note(self._calculate_midi_note('D')),
            'E': lambda: self._add_note(self._calculate_midi_note('E')),
            'F': lambda: self._add_note(self._calculate_midi_note('F')),
            'G': lambda: self._add_note(self._calculate_midi_note('G')),
            'a': lambda: self._add_note(self._calculate_midi_note('A')), 
            'b': lambda: self._add_note(self._calculate_midi_note('B')),
            'c': lambda: self._add_note(self._calculate_midi_note('C')),
            'd': lambda: self._add_note(self._calculate_midi_note('D')),
            'e': lambda: self._add_note(self._calculate_midi_note('E')),
            'f': lambda: self._add_note(self._calculate_midi_note('F')),
            'g': lambda: self._add_note(self._calculate_midi_note('G')),
            ' ': lambda: self._add_note(0),
            '+': lambda: self._vol_adj(self.vol*2),
            '-': lambda: self._vol_adj(self.default_vol),
            '?': lambda: self._add_note(self._calculate_midi_note(random.choice('ABCDEFG'))),
            '\n': lambda: self._change_instrument(),
            ';': lambda: self._bpm_adj(random.randint(60, 180))
        }

    def _calculate_midi_note(self, note):
        offset = {
            'C': 0,
            'D': 2,
            'E': 4,
            'F': 5,
            'G': 7,
            'A': 9,
            'B': 11
        }
        return 12 + 12*self.octave + offset[note]

    def _add_note(self, note):
        def add_note():
            return (md.Message('note_on', note=note, time=0),
                    md.Message('note_off', note=note, time=self.dur))
        return add_note

    def _vol_adj(self, value):
        value = value if value <= 127 and value >= 0 else self.vol
        self.vol = value
        def vol_adj():
            return md.Message('control_change', control=7, value=value),
        return vol_adj

    def _bpm_adj(self, value):
        self.bpm = value
        tempo = md.bpm2tempo(value)
        def bpm_adj():
            return md.MetaMessage('set_tempo', tempo=tempo),
        return bpm_adj
    
    def _octave_adj(self, value):
        value = value if value <= 9 and value >= 1 else self.octave
        self.octave = value
        def octave_adj():
            return ()
        return octave_adj
    
    def _change_instrument(self):
        #TODO
        program = 0
        def change_instrument():
            return md.Message('program_change', program=program, time=0),
        return change_instrument

    def initial_msgs(self):
        tempo = md.bpm2tempo(self.bpm)
        return (md.MetaMessage('set_tempo', tempo=tempo),
                md.Message('control_change', control=7, value=self.default_vol))
