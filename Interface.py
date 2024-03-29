import os
import time
import dearpygui.dearpygui as dpg
from textprocessing import TextConverter, Music, Rules
from AudioConverter import AudioConverter

class Interface:
    """
    Interface: a classe gerencia a criação e interação com a interface gráfica usando Dear PyGui.
    Contém os métodos para ler o texto de entrada do usuário.
    """
    # TODO: 
    # organize files
    # interaction with music (start, pause, restart music)

    # Consts
    MIN_BPM_VALUE = 20
    MAX_BPM_VALUE = 200
    MENU_WIDTH = 500
    MENU_HEIGHT = 400
    WINDOW_WIDTH = 720
    WINDOW_HEIGHT = 720
    WINDOW_WRAP = 20
    FONT_SIZE = 16

    # Private vars
    _file_content = ''
    _music = Music()
    
    # Initializes Dear PyGui context and setup interface (public)
    def __init__(self):
        dpg.create_context()
        self._setup_interface()
        dpg.create_viewport(title='Pepper\'s Private Band', width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("__main_window", True)

    # Run the interface (public)
    def run(self):
        dpg.start_dearpygui()
        dpg.destroy_context()

    # Menu Functions (private)
    def _menu_import(self):
        # import the selected file and write the content into input text 
        def _menu_import_callback(sender, app_data):
            _file_path = app_data["file_path_name"]
            with open(_file_path, 'r') as f:
                Interface._file_content = f.read()
                dpg.configure_item(item='__text_input', default_value=self._file_content)

        # open file selector for the txt file
        with dpg.file_dialog(directory_selector=False, show=True, callback=_menu_import_callback, tag="file_dialog_tag", width=self.MENU_WIDTH, height=self.MENU_HEIGHT):
            dpg.add_file_extension(".txt", color=(150, 255, 150, 255))

    # gives information about the program
    def _menu_help(self):
        with dpg.window(label="Help Window", width=self.MENU_WIDTH, height=self.MENU_HEIGHT, show=True, no_collapse=True, no_resize=False):
            with dpg.group(width=self.MENU_WIDTH):
                dpg.add_text("The main goal of the software is to generate music from text.", wrap=self.MENU_WIDTH-self.WINDOW_WRAP)
                dpg.add_separator()
                dpg.add_text("The software receives as input an unstructured text (like a short story or newspaper page) and generates a set of notes corresponding to the text according to some parameters (like timbre, rhythm, BPM). The parameters are defined via a mapping of text to musical information.", indent= 1, wrap=self.MENU_WIDTH-self.WINDOW_WRAP)
    
    # Buttons callbacks (private)
    # check the inputs, generate the songs and show save buttons
    def _btn_generate(self, sender, app_data):
        # aux function for showing error messages after generate button was pressed
        def _show_error(tag, text):
            dpg.configure_item(item=tag, default_value=text, show=True, color=(255, 0, 0, 255))

        _show_options_flag = True

        # clear error messages
        for input_error_tag in ["__text_input_error", "__bpm_input_error", "__filename_input_error"]:
            dpg.configure_item(item=input_error_tag, show=False)

        _values = dpg.get_values(["__text_input", "__bpm_input", "__filename_input"])
        
        # verify input values
        if not _values[0]:
            _show_error("__text_input_error", "Text input is required")
            _show_options_flag = False
        
        if not (self.MIN_BPM_VALUE <= int(_values[1]) <= self.MAX_BPM_VALUE):
            _show_error("__bpm_input_error", f'BPM value must be between {self.MIN_BPM_VALUE} and {self.MAX_BPM_VALUE}')
            _show_options_flag = False
        
        if not _values[2]:
            _show_error("__filename_input_error", "Filename is required")
            _show_options_flag = False

        if _show_options_flag:

            # present a loading indicator for couple seconds
            dpg.configure_item(item="__loading_indicator", show=True)
            time.sleep(2)
            dpg.configure_item(item="__loading_indicator", show=False)

            # integrate the input values with the Music class                       
            _string_to_music = self._file_content + _values[0]                      
            _rules = Rules(self._music.get_ticks(), _values[1], 64, 4, 0)           
            _converter = TextConverter(_string_to_music, _rules)
            self._music = Music()                    
            _converter.compose(self._music)                                         
            self._music.save("sample.mid")
            self._recorder = AudioConverter(self._music)                                                                          
                                                                                    
            # show music buttons                                                    
            dpg.configure_item(item="__btn_play", show=True)                        
            dpg.configure_item(item="__btn_pause", show=True)                       
            dpg.configure_item(item="__btn_restart", show=True)                       
                                                                                      
            # show save buttons                                                       
            dpg.configure_item(item="__btn_save_mid", show=True)                      
            dpg.configure_item(item="__btn_save_txt", show=True)                      
                                                                                      
                                                               
                                                                                      
    # play the generated music
    def _btn_play_callback(self):
         # play the song                                                           
        self._recorder.playback()  

    # pause the generated music
    def _btn_pause_callback(self):
        self._recorder.pause()

    # restart the generated music
    def _btn_restart_callback(self):
        self._recorder.restart()

    # save the generated song into a mid file after the generation of the song
    def _btn_save_mid(self):
        _filename = dpg.get_value("__filename_input")

        # handle callback writing the input text in the dir/filename specified
        def _save_mid_callback(sender, app_data):
            _selected_directory = app_data["file_path_name"]
            _full_path = f"{_selected_directory}/{_filename}.mid"
            self._music.save(_full_path)
            dpg.configure_item(item="__saved_mid", default_value="Saved .mid File!", show=True, color=(0, 255, 0, 255))

        # open dir selector for the mid file
        with dpg.file_dialog(directory_selector=True, show=True, tag="__file_dialog_mid", callback=_save_mid_callback, width=self.MENU_WIDTH, height=self.MENU_HEIGHT):
            pass

    # save the input text as a txt file after the generation of the song 
    def _btn_save_txt(self):
        _filename = dpg.get_value("__filename_input")

        # handle callback writing the input text in the dir/filename specified
        def _save_txt_callback(sender, app_data):
            _selected_directory = app_data["file_path_name"]
            _full_path = f"{_selected_directory}/{_filename}.txt"
            with open(_full_path, "w") as file:
                _text = dpg.get_value("__text_input")
                file.write(_text)
            
            dpg.configure_item(item="__saved_txt", default_value="Saved .txt File!", show=True, color=(0, 255, 0, 255))

        # open dir selector for the txt file
        with dpg.file_dialog(directory_selector=True, show=True, tag="__file_dialog_txt", callback=_save_txt_callback, width=self.MENU_WIDTH, height=self.MENU_HEIGHT):
            pass

    # Sets up the interface (private)    
    def _setup_interface(self):
        # add a font registry
        with dpg.font_registry():
            # library limitations only supports full path of the font
            _cur_dir = os.getcwd()
            _default_font = dpg.add_font(f'{_cur_dir}/UbuntuMono.ttf', self.FONT_SIZE)

        with dpg.window(tag="__main_window"):
            with dpg.menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="Import File", callback=self._menu_import)
                dpg.add_menu_item(label="Help", callback=self._menu_help)

            # Load images and icons
            # Help Image
            _img_width, _img_height, _img_channels, _img_data = dpg.load_image("icons8-help-18.png")
            with dpg.texture_registry(show=False):
                dpg.add_static_texture(_img_width, _img_height, _img_data, tag="__texture_help")

            # Play image
            _img_width, _img_height, _img_channels, _img_data = dpg.load_image("icons8-play-18.png")
            with dpg.texture_registry(show=False):
                dpg.add_static_texture(_img_width, _img_height, _img_data, tag="__texture_play")

            # Pause image
            _img_width, _img_height, _img_channels, _img_data = dpg.load_image("icons8-pause-18.png")
            with dpg.texture_registry(show=False):
                dpg.add_static_texture(_img_width, _img_height, _img_data, tag="__texture_pause")
           
            # Restart image
            _img_width, _img_height, _img_channels, _img_data = dpg.load_image("icons8-restart-18.png")
            with dpg.texture_registry(show=False):
                dpg.add_static_texture(_img_width, _img_height, _img_data, tag="__texture_restart")


            # Input text
            dpg.add_spacer(height=5)
            with dpg.group(horizontal=True):
                dpg.add_text("Your Text")
                dpg.add_image_button("__texture_help", tag="__text_input_help")
                with dpg.tooltip("__text_input_help"):
                    dpg.add_text("Here you write the text that will be converted into music.\n"
                                 "Can't be empty!")

            dpg.add_input_text(tag="__text_input", multiline=True)
            dpg.add_text(tag="__text_input_error", show=False)

            
            
            # Input BPM
            with dpg.group(horizontal=True):
                dpg.add_text("BPM")
                dpg.add_image_button("__texture_help", tag="__bpm_input_help")
                with dpg.tooltip("__bpm_input_help"):
                    dpg.add_text("Here you choose the BPM (Beats Per Minute) of the generated music.\n"
                                 "Must be between 20 and 200!")

            dpg.add_input_int(tag="__bpm_input", min_value=self.MIN_BPM_VALUE, max_value=self.MAX_BPM_VALUE, min_clamped=True, max_clamped=True)
            dpg.add_text(tag="__bpm_input_error", show=False)
            
            # Input Filename
            with dpg.group(horizontal=True):
                dpg.add_text("Filename")
                dpg.add_image_button("__texture_help", tag="__filename_input_help")
                with dpg.tooltip("__filename_input_help"):
                    dpg.add_text("Here you write the output filename. \n"
                                 "Don't worry with the extension (.mid and/or .txt), this will be added later :).\n"
                                 "The filename can't be empty!")

            dpg.add_input_text(tag="__filename_input")
            dpg.add_text(tag="__filename_input_error", show=False)
            
            # Generate button
            dpg.add_spacer(height=5)
            dpg.add_button(tag="__btn_generate", label="Generate", callback=self._btn_generate)
            with dpg.tooltip("__btn_generate"):
                    dpg.add_text("Generate the Music! Let's dance \n"
                                " (-_-) \n"
                                " /) )> \n"
                                "  / \ ")
            
            dpg.add_separator()

            # Loading indicator
            dpg.add_loading_indicator(tag="__loading_indicator", show=False)
            
            dpg.add_spacer(height=15)
            with dpg.group(horizontal=True):

                # Music Buttons
                # Play Button
                dpg.add_image_button("__texture_play", tag="__btn_play", callback=self._btn_play_callback, show=False)
                with dpg.tooltip("__btn_play"):
                    dpg.add_text("Play the music")

                # Pause Button
                dpg.add_image_button("__texture_pause", tag="__btn_pause", callback=self._btn_pause_callback, show=False)
                with dpg.tooltip("__btn_pause"):
                    dpg.add_text("Pause the music")

                # Restart Button
                dpg.add_image_button("__texture_restart", tag="__btn_restart", callback=self._btn_restart_callback, show=False)
                with dpg.tooltip("__btn_restart"):
                    dpg.add_text("Restart the music")


            # Save Buttons
            dpg.add_spacer(height=10)
            with dpg.group(horizontal=True):

                # Save Mid button
                dpg.add_button(tag="__btn_save_mid", label="Save Mid", callback=self._btn_save_mid, show=False)
                dpg.add_text(tag="__saved_mid", show=False)
                with dpg.tooltip("__btn_save_mid"):
                        dpg.add_text("Save the music into a .mid file")

                dpg.add_spacer(height=5)

                # Save Text button
                dpg.add_button(tag="__btn_save_txt", label="Save Text", callback=self._btn_save_txt, show=False)
                dpg.add_text(tag="__saved_txt", show=False)
                with dpg.tooltip("__btn_save_txt"):
                    dpg.add_text("Save the input text into a .txt file\n"
                                "You can import this text file after")

            # set default font
            dpg.bind_font(_default_font)