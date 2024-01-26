import dearpygui.dearpygui as dpg
import time
from textprocessing import TextConverter, Music, Rules
from AudioConverter import AudioConverter

class Interface:
    """
    Interface: a classe gerencia a criação e interação com a interface gráfica usando Dear PyGui.
    Contém os métodos para ler o texto de entrada do usuário.
    """
    # TODO: 
    # beautify interface (noggers)

    # Consts
    MIN_BPM_VALUE = 20
    MAX_BPM_VALUE = 200
    MENU_WIDTH = 500
    MENU_HEIGHT = 400
    WINDOW_WIDTH = 720
    WINDOW_HEIGHT = 720
    WINDOW_WRAP = 20

    # Private vars
    _file_content = ''
    _music = Music()
    
    # Initializes Dear PyGui context and setup interface (public)
    def __init__(self):
        dpg.create_context()
        self._setup_interface()
        dpg.create_viewport(title='Title', width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main_window", True)

    # Run the interface (public)
    def run(self):
        dpg.start_dearpygui()
        dpg.destroy_context()

    # Menu Functions (private)
    def _menu_import(self):
        def callback(sender, app_data):
            file_path = app_data["file_path_name"]
            file_handler(file_path)

        def file_handler(file_path):
            with open(file_path, 'r') as f:
                Interface._file_content = f.read()
                print(Interface._file_content)
                dpg.configure_item(item='_text_input', default_value=self._file_content)

        with dpg.file_dialog(directory_selector=False, show=True, callback = callback, tag="file_dialog_tag", width=self.MENU_WIDTH, height=self.MENU_HEIGHT):
            dpg.add_file_extension(".txt", color=(150, 255, 150, 255))


    def _menu_help(self):
        with dpg.window(label="Help Window", width=self.MENU_WIDTH, height=self.MENU_HEIGHT, show=True, no_collapse=True, no_resize=False):
            with dpg.group(width=self.MENU_WIDTH):
                dpg.add_text("The main goal of the software is to generate music from text.", wrap=self.MENU_WIDTH-self.WINDOW_WRAP)
                dpg.add_separator()
                dpg.add_text("The software receives as input an unstructured text (like a short story or newspaper page) and generates a set of notes corresponding to the text according to some parameters (like timbre, rhythm, BPM). The parameters are defined via a mapping of text to musical information.", indent= 1, wrap=self.MENU_WIDTH-self.WINDOW_WRAP)
    
    def _btn_generate(self, sender, app_data):
        show_btn_save_flag = True

        # clear error messages
        for input_error_tag in ["_text_input_error", "_bpm_input_error", "_filename_input_error"]:
            dpg.configure_item(item=input_error_tag, show=False)

        values = dpg.get_values(["_text_input", "_bpm_input", "_filename_input"])
        
        # verify input values
        if not values[0]:
            self._show_error("_text_input_error", "Text input is required")
            show_btn_save_flag = False
        
        if not (self.MIN_BPM_VALUE <= int(values[1]) <= self.MAX_BPM_VALUE):
            self._show_error("_bpm_input_error", f'BPM value must be between {self.MIN_BPM_VALUE} and {self.MAX_BPM_VALUE}')
            show_btn_save_flag = False
        
        if not values[2]:
            self._show_error("_filename_input_error", "Filename is required")
            show_btn_save_flag = False

        if show_btn_save_flag:
            # present a loading indicator for couple seconds
            dpg.configure_item(item="_loading_indicator", show=True)
            time.sleep(2)
            dpg.configure_item(item="_loading_indicator", show=False)

            dpg.configure_item(item="_btn_save", show=True)

            string_to_music = Interface._file_content + values[0]
            rules = Rules(Interface._music.get_ticks(), 120, 64, 4, 0)
            converter = TextConverter(string_to_music, rules)
            converter.compose(Interface._music)
            Interface._music.save("sample.mid")
            recorder = AudioConverter(Interface._music)
            recorder.playback()
            
    def _show_error(self, tag, text):
        dpg.configure_item(item=tag, default_value=text, show=True, color=(255, 0, 0, 255))

    def _btn_save(self):
        pass

    # Sets up the interface (private)    
    def _setup_interface(self):
        with dpg.window(tag="main_window"):
            with dpg.menu_bar():
                with dpg.menu(label="File"):
                    dpg.add_menu_item(label="Import File", callback=self._menu_import)
                dpg.add_menu_item(label="Help", callback=self._menu_help)

            # Input text
            dpg.add_text("Your Text")
            dpg.add_input_text(tag="_text_input", multiline=True)
            dpg.add_text(tag="_text_input_error", show=False)
            
            # Input BPM
            dpg.add_text("BPM")
            dpg.add_input_int(tag="_bpm_input", min_value=self.MIN_BPM_VALUE, max_value=self.MAX_BPM_VALUE, min_clamped=True, max_clamped=True)
            dpg.add_text(tag="_bpm_input_error", show=False)
            
            # Input Filename
            dpg.add_text("Filename")
            dpg.add_input_text(tag="_filename_input")
            dpg.add_text(tag="_filename_input_error", show=False)
            
            dpg.add_button(label="Generate", callback=self._btn_generate)
            
            dpg.add_loading_indicator(tag="_loading_indicator", show=False)

            dpg.add_separator()
            
            # TODO: add music player from pygame and INTEGRATE
            # me right now:
            #             ⠀⠀⠀⠀⠀⠀   ⢀⣠⣖⣱⣞⡿⣽⣯⣿⣳⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            # ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠩⠚⣺⠿⠿⠛⣉⠡⢉⠻⣟⡛⠛⠲⢦⣼⣝⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            # ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⢶⠀⣀⡤⠶⣾⠋⣐⡆⡑⢠⠃⡶⢀⢂⡙⢧⡁⢊⢿⣞⣾⢿⢦⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            # ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡼⣿⡿⠋⠡⢰⡟⢁⢂⢾⠀⠔⠂⢼⡇⢤⠂⡔⡈⣷⠠⡈⢷⡉⠛⢿⣷⣹⣆⠀⠀⠀⠀⠀⠀⠀⠀
            # ⠀⠀⠀⠀⠀⠀⠀⠀⣠⢾⣿⡿⠡⠌⣵⠋⡐⡼⢃⣾⢈⠘⡈⣿⡄⣻⡆⡐⠄⡸⣆⠡⠌⢻⡐⠠⢿⣿⡼⣆⠀⠀⠀⠀⠀⠀⠀⠀
            # ⠀⠀⠀⠀⠀⠀⠀⢠⣿⢿⡿⢁⠒⣼⢁⠂⡼⢡⡏⡸⡜⣇⠐⢻⢬⣱⡇⡑⣮⡀⢹⠠⢉⠘⢇⠡⢺⣿⣳⣿⣦⠀⠀⠀⠀⠀⠀⠀
            # ⠀⠀⠀⠀⠀⠀⣰⣯⢿⣿⠃⡬⢁⣧⡼⢲⣷⣿⢳⣻⢧⠱⢺⣹⢶⣿⢿⣳⣿⡾⡾⣝⡠⣇⡦⢂⠹⠸⣷⣽⢼⣧⠀⠀⠀⠀⠀⠀
            # ⠀⠀⠀⠀⣠⣴⡏⣠⡞⢡⡌⢡⣼⠧⣟⣟⣾⣯⠾⣯⣿⣧⢦⣿⣿⣿⣮⣙⣻⣷⣿⣿⣇⢠⠿⣀⠡⠂⢏⢳⣝⣞⠇⠀⠀⠀⠀⠀
            # ⠀⠀⠀⢰⣯⣿⣾⢧⡔⣺⠔⣿⢾⣿⣿⣿⣿⠿⠿⣿⣟⡿⣯⣳⣿⣯⣿⣿⣿⣿⣿⣿⣿⣚⠧⣼⢡⠊⣆⠶⣹⢿⡄⣀⠀⠀⠀⠀
            # ⠀⠀⠀⢼⣿⣿⣱⣎⣾⣻⢍⣿⣾⣿⡿⠋⢀⣤⡀⠙⣿⣟⣿⣿⡽⣿⣿⠉⣀⡀⠈⠹⣿⡿⣼⡏⣟⢶⡟⢮⡕⣮⣽⣿⣳⠀⠀⠀
            # ⠀⠀⠀⢸⣼⡯⣿⣿⡞⡿⣏⡽⣻⡟⠃⣀⣈⣥⣤⡤⣻⣿⡟⣿⣛⣿⢋⣄⣈⡁⠀⠀⣽⣿⢾⣟⣭⡟⣿⣡⡿⣻⢿⡽⠏⠀⠀⠀
            # ⠀⠀⠀⠀⠉⠙⢻⣿⡼⢷⡟⣭⢿⣳⣮⣽⣿⠿⠟⠛⠛⠙⡛⠙⠛⠛⠛⠿⢿⣟⡿⣦⣸⣿⣾⣼⡭⡟⣼⡹⢿⡙⠋⠀⠀⠀⠀⠀
            # ⠀⠀⠀⠀⠀⠀⡴⣿⣿⣷⡜⡼⣿⠷⢋⠁⠠⡀⢂⣡⠶⠧⣬⡴⠶⢤⡉⠐⢄⠈⡙⠿⣽⣿⢾⡡⣟⣽⣽⣿⡿⣧⠀⠀⠀⠀⠀⠀
            # ⠀⠀⠀⠀⠀⠀⠙⠻⣿⣿⣧⠳⣼⡆⠠⢈⡐⢀⢲⣇⣀⣀⣀⣀⣀⡀⢳⡌⢀⠒⠠⠐⢨⣟⣱⣾⣷⣿⣿⣿⡽⠏⠀⠀⠀⠀⠀⠀
            # ⠀⠀⠀⠀⠀⠀⠀⠀⠹⣞⣿⣷⣤⣹⣄⠡⢀⣺⣏⠉⣠⠖⠚⠲⣍⠉⠛⣷⡄⠌⢂⢡⡟⢈⣷⣿⣿⢻⣷⠋⠀⠀⠀⠀⠀⠀⠀⠀
            # ⠀⠀⠀⠀⠀⠀⠀⠀⢰⢿⡼⣷⣮⣝⡻⢦⡄⠻⠶⠋⢁⣼⣛⣦⡈⠳⣌⡽⠂⢈⣠⣾⣫⣿⣾⡿⠿⣯⡗⠀⠀⠀⠀⠀⠀⠀⠀⠀
            # ⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣛⡿⢿⣿⣽⣿⣥⡀⠑⠊⠜⠉⡇⠃⡐⠠⢀⣽⣾⣿⣿⣿⡏⢭⣻⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            # ⠀⠀⠀⠀⠀⠀⣠⣴⣿⢽⣦⡈⠉⠉⣻⣽⣿⣧⢛⡳⣮⣤⣁⣐⣤⡶⢟⢫⣼⣿⡿⣟⣥⠀⠀⠀⠀⠀⢰⠦⢤⣄⡀⠀⠀⠀⠀⠀
            # ⠀⠀⠀⠀⣠⣾⣻⣷⠿⢋⠍⡟⠓⠶⣯⡿⣿⣶⣯⣹⢭⣭⢋⢽⣭⣭⣯⣗⣶⣾⠿⣷⣖⠁⣀⣤⠴⢲⠾⣯⣻⢯⣻⣶⡄⠀⠀⠀
            # ⠀⠀⢀⣴⣿⡿⠟⡡⠎⡜⢢⠱⣚⠛⠳⣽⣿⣿⣿⣿⣿⣧⠎⣼⣸⣿⣿⣿⣿⣿⣝⢶⡹⢫⠗⢦⣤⡏⡒⢤⡉⠷⣗⢷⡗⠀⠀⠀
            # ⠀⠀⢸⣻⡟⣡⢋⢴⡩⢜⡡⢓⠬⣉⠓⣼⣿⣿⣿⣿⣿⣯⣗⣼⣹⣿⣿⣿⣿⣿⣿⡏⡔⢣⠚⡔⢢⠱⣉⠦⣉⠖⡩⢿⡄⠀⠀⠀
            # ⠀⠀⣻⣿⠓⣤⡟⢫⡗⢪⡔⣋⢖⡩⢎⣿⣿⣿⣿⣿⣿⣿⣻⣟⣿⣿⣿⣿⣿⣿⣿⡷⣘⠥⣋⠼⣡⢓⡌⣖⡳⢮⡱⢩⣇⠀⠀⠀
            # ⠀⢰⣟⣿⠽⣇⠰⢸⣏⢲⡱⢬⣆⢇⣻⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⢠⡛⢤⣷⡘⣆⡓⢦⣻⠄⢛⢧⣻⡀⠀
            # ⠀⣏⣾⡏⣞⡜⣳⣽⣮⡗⣼⠟⣻⠔⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⠿⢿⡆⡝⣾⢉⣷⠸⣜⢥⢺⣬⢶⡋⡽⡇⠀
            # ⢰⣷⡿⣘⣧⣚⠥⣾⣻⣵⢏⡢⣹⢯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣾⣸⣧⣹⢇⢊⠼⣟⡿⣎⡝⢦⢣⣝⠲⡇⠀

            dpg.add_button(tag="_btn_save", label="Save", callback=self._btn_save, show=False)
