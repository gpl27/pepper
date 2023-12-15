class UserInput:
    """
    UserInput: interface com o usuário
    
    O objetivo dessa classe é obter do usuário a string que
    deverá ser processada pelo programa. Essa string pode vir
    de um arquivo texto, ou pode ser fornecida diretamente pelo usuário
    """
    def __init__(self, inputs) -> None:
        self._text_input = inputs[0]
        self._bpm_input = inputs[1]
        self._filename_input = inputs[2]

    def __str__(self) -> str:
        return f"Text Input: {self._text_input}\nBPM Input: {self._bpm_input}\nFilename Input: {self._filename_input}"
    
    def get_text_input(self):
        return self._text_input
    
    def get_bpm_input(self):
        return self._bpm_input
    
    def get_filename_input(self):
        return self._filename_input
    
    def get_user_inputs(self):
        return [self._text_input, self._bpm_input, self._filename_input]
