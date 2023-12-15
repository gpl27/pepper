class Rules:
    """
    Rules: o objetivo deste classe é mapear a transformação do texto para elementos musicais
    """
    def __init__(self):
        self.output_port = None  # output MIDI
        self.note_mapping = {
            'A': 69, # Lá
            'B': 71, # Si
            'C': 60, # Dó 
            'D': 62, # Ré
            'E': 64, # Mi
            'F': 65, # Fá
            'G': 67  # Sol
        }
