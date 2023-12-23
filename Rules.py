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
    def __init__(self, ticks: int, bpm: int, vol: int, octave: int, program: int):
        self.ticks = ticks
        self.bpm = bpm
        self.default_vol = vol
        self.vol = self.default_vol
        self.octave = octave
        self.program = program
        self.p_map = ''
        self.mappings = {
            'BPM+': self._BPMp_map,
            'R+': self._Rp_map,
            'R-': self._Rm_map,
            'A': self._A_map, 
            'B': self._B_map,
            'C': self._C_map,
            'D': self._D_map,
            'E': self._E_map,
            'F': self._F_map,
            'G': self._G_map,
            'a': self._A_map, 
            'b': self._B_map,
            'c': self._C_map,
            'd': self._D_map,
            'e': self._E_map,
            'f': self._F_map,
            'g': self._G_map,
            'O': self._repeat,
            'o': self._repeat,
            'U': self._repeat,
            'u': self._repeat,
            'I': self._repeat,
            'i': self._repeat,
            ' ': self._rest_map,
            '+': self._p_map,
            '-': self._m_map,
            '?': self._rnote_map,
            '\n': self._nl_map, # TODO: escolher para qual instrumento mudar
            ';': self._sc_map,
            '': self._NOP
        }

    def initial_msgs(self):
        tempo = md.bpm2tempo(self.bpm)
        return (md.MetaMessage('set_tempo', tempo=tempo),
                md.Message('control_change', control=7, value=self.default_vol))
    
    def get_keys(self) -> list:
        return self.mappings.keys()

    def get_msgs(self, group) -> tuple:
        msgs = self.mappings[group]()
        self.p_map = group
        return msgs

    def _note2midi(self, note):
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

    def _BPMp_map(self) -> tuple:
        self.bpm += 80
        tempo = md.bpm2tempo(self.bpm)
        return md.MetaMessage('set_tempo', tempo=tempo),

    def _Rp_map(self) -> tuple:
        self.octave = self.octave+1 if self.octave+1 < 10 else self.octave
        return ()

    def _Rm_map(self) -> tuple:
        self.octave = self.octave-1 if self.octave-1 > 0 else self.octave
        return ()

    def _A_map(self) -> tuple:
        note = self._note2midi('A')
        return (md.Message('note_on', note=note, time=0),
                md.Message('note_off', note=note, time=self.ticks))

    def _B_map(self) -> tuple:
        note = self._note2midi('B')
        return (md.Message('note_on', note=note, time=0),
                md.Message('note_off', note=note, time=self.ticks))

    def _C_map(self) -> tuple:
        note = self._note2midi('C')
        return (md.Message('note_on', note=note, time=0),
                md.Message('note_off', note=note, time=self.ticks))

    def _D_map(self) -> tuple:
        note = self._note2midi('D')
        return (md.Message('note_on', note=note, time=0),
                md.Message('note_off', note=note, time=self.ticks))

    def _E_map(self) -> tuple:
        note = self._note2midi('E')
        return (md.Message('note_on', note=note, time=0),
                md.Message('note_off', note=note, time=self.ticks))

    def _F_map(self) -> tuple:
        note = self._note2midi('F')
        return (md.Message('note_on', note=note, time=0),
                md.Message('note_off', note=note, time=self.ticks))

    def _G_map(self) -> tuple:
        note = self._note2midi('G')
        return (md.Message('note_on', note=note, time=0),
                md.Message('note_off', note=note, time=self.ticks))

    def _repeat(self) -> tuple:
        if self.p_map != '' and self.p_map in 'AaBbCcDdEeFfGg':
            note = self._note2midi(self.p_map.upper())
            return (md.Message('note_on', note=note, time=0),
                    md.Message('note_off', note=note, time=self.ticks))
        else:
            return (md.Message('program_change', program=124, time=0),
                    md.Message('note_on', note=69, time=0),
                    md.Message('note_off', note=69, time=self.ticks),
                    md.Message('program_change', program=self.program, time=0))

    def _rest_map(self) -> tuple: 
        return (md.Message('note_on', note=0, velocity=0, time=0),
                md.Message('note_off', note=0, velocity=0, time=self.ticks))

    def _p_map(self) -> tuple:
        self.vol = self.vol*2 if self.vol*2 < 128 else 127
        return md.Message('control_change', control=7, value=self.vol),

    def _m_map(self) -> tuple:
        self.vol = self.default_vol
        return md.Message('control_change', control=7, value=self.vol),

    def _rnote_map(self) -> tuple:
        note = self._note2midi(random.choice('ABCDEFG'))
        return (md.Message('note_on', note=note, time=0),
                md.Message('note_off', note=note, time=self.ticks))

    def _nl_map(self) -> tuple: # TODO: choose how to change instrument
        return ()

    def _sc_map(self) -> tuple:
        self.bpm = random.randint(60, 180)
        tempo = md.bpm2tempo(self.bpm)
        return md.MetaMessage('set_tempo', tempo=tempo),

    def _NOP(self) -> tuple:
        print("NOP")
        return ()
