import random
import mido as md


class Rules:
    """
    Rules: o objetivo deste classe é mapear a transformação do texto
    para elementos musicais.

    Para Rules que possuem regras que são prefixo de outras, ordene
    em ordem de prioridade. O calculo de nota é feito relativo ao C1
    """
    def __init__(self, midiFile):
        self.dur = midiFile.ticks_per_beat
        self.bpm = 90
        self.default_vol = 32
        self.vol = self.default_vol
        self.octave = 4
        self.mappings = {
            'BPM+': self._bpm_adj(self.bpm+80),
            'R+': self._octave_adj(self.octave+1),
            'R-': self._octave_ad(self.octave-1),
            'A': self._add_note(self._calculate_midi_note('A')), 
            'B': self._add_note(self._calculate_midi_note('B')),
            'C': self._add_note(self._calculate_midi_note('C')),
            'D': self._add_note(self._calculate_midi_note('D')),
            'E': self._add_note(self._calculate_midi_note('E')),
            'F': self._add_note(self._calculate_midi_note('F')),
            'G': self._add_note(self._calculate_midi_note('G')),
            'a': self._add_note(self._calculate_midi_note('A')), 
            'b': self._add_note(self._calculate_midi_note('B')),
            'c': self._add_note(self._calculate_midi_note('C')),
            'd': self._add_note(self._calculate_midi_note('D')),
            'e': self._add_note(self._calculate_midi_note('E')),
            'f': self._add_note(self._calculate_midi_note('F')),
            'g': self._add_note(self._calculate_midi_note('G')),
            ' ': self._add_note(0),
            '+': self._vol_adj(self.vol*2),
            '-': self._vol_adj(self.default_vol),
            '?': self._add_note(self._calculate_midi_note(random.choice('ABCDEFG'))),
            '\n': self._change_instrument(),
            ';': self._bpm_adj(random.randint(60, 180))
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
            return (md.Message('control_change', control=7, value=value))
        return vol_adj

    def _bpm_adj(self, value):
        self.bpm = value
        def bpm_adj():
            return (md.MetaMessage('set_tempo', tempo=md.bpm2tempo(value)))
        return bpm_adj
    
    def _octave_adj(self, value):
        value = value if value <= 9 and value >= 1 else self.octave
        self.octave = value
        def octave_adj():
            return None
        return octave_adj
    
    def _change_instrument(self):
        #TODO
        program = 0
        def change_instrument():
            return (md.Message('program_change', program=program, time=0))
        return change_instrument

