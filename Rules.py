import re
import random
import mido as md


class Rules:
    """
    Rules: o objetivo deste classe é mapear a transformação do texto
    para elementos musicais.

    `mappings` deve estar em ordem decrescente de tamanho de string.
    Além disso, é necessário especificar pelo menos o caso base de 
    string vazia.
    O calculo de nota é feito relativo ao C1.
    """
    def __init__(self, music, bpm, vol, octave, program):
        self.dur = music.mid.ticks_per_beat
        self.bpm = bpm
        self.default_vol = vol
        self.vol = self.default_vol
        self.octave = octave
        self.program = program
        self.p_map = ''
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
            'O': lambda: self._repeat(),
            'o': lambda: self._repeat(),
            'U': lambda: self._repeat(),
            'u': lambda: self._repeat(),
            'I': lambda: self._repeat(),
            'i': lambda: self._repeat(),
            ' ': lambda: self._add_rest(),
            '+': lambda: self._vol_adj(self.vol*2),
            '-': lambda: self._vol_adj(self.default_vol),
            '?': lambda: self._add_note(self._calculate_midi_note(random.choice('ABCDEFG'))),
            '\n': lambda: self._change_instrument(0), # TODO: escolher para qual instrumento mudar
            ';': lambda: self._bpm_adj(random.randint(60, 180)),
            '': lambda: self._NOP()
        }
    
    def get_regex(self):
        keys_regex = '|'.join(re.escape(key) for key in self.mappings.keys())
        return f'({keys_regex})'

    def get_msgs(self, group):
        msgs = self.mappings[group]()()
        self.p_map = group
        return msgs

    def _calculate_midi_note(self, note):
        offset = {
            'c': 0,
            'd': 2,
            'e': 4,
            'f': 5,
            'g': 7,
            'a': 9,
            'b': 11,
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
    
    def _add_rest(self):
        def add_rest():
            return (md.Message('note_on', note=0, velocity=0, time=0),
                    md.Message('note_off', note=0, velocity=0, time=self.dur))
        return add_rest

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
    
    def _change_instrument(self, value):
        self.program = value
        def change_instrument():
            return md.Message('program_change', program=value, time=0),
        return change_instrument

    def _repeat(self):
        if self.p_map != '' and self.p_map in 'AaBbCcDdEeFfGg':
            return self._add_note(self._calculate_midi_note(self.p_map))
        else:
            def telefone():
                return (md.Message('program_change', program=124, time=0),
                        md.Message('note_on', note=69, time=0),
                        md.Message('note_off', note=69, time=self.dur),
                        md.Message('program_change', program=self.program, time=0))
            return telefone

    def _NOP(self):
        def NOP():
            print("NOP Detected")
            return ()
        return NOP

    def initial_msgs(self):
        tempo = md.bpm2tempo(self.bpm)
        return (md.MetaMessage('set_tempo', tempo=tempo),
                md.Message('control_change', control=7, value=self.default_vol))
