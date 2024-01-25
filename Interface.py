import dearpygui.dearpygui as dpg

class Interface:
    """
    Interface: a classe gerencia a criação e interação com a interface gráfica usando Dear PyGui.
    Contém os métodos para ler o texto de entrada do usuário.
    """
    # TODO: beautify interface (noggers)

    # Constants
    MIN_BPM_VALUE = 20
    MAX_BPM_VALUE = 200
    MENU_WIDTH = 500
    MENU_HEIGHT = 400
    WINDOW_WIDTH = 720
    WINDOW_HEIGHT = 720
    WINDOW_WRAP = 20

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
        # TODO: add file selector
        pass

    def _menu_help(self):
        with dpg.window(label="Help Window", width=self.MENU_WIDTH, height=self.MENU_HEIGHT, show=True, no_collapse=True, no_resize=False):
            with dpg.group(width=self.MENU_WIDTH):
                dpg.add_text("The main goal of the software is to generate music from text.", wrap=self.MENU_WIDTH-self.WINDOW_WRAP)
                dpg.add_separator()
                dpg.add_text("The software receives as input an unstructured text (like a short story or newspaper page) and generates a set of notes corresponding to the text according to some parameters (like timbre, rhythm, BPM). The parameters are defined via a mapping of text to musical information.", indent= 1, wrap=self.MENU_WIDTH-self.WINDOW_WRAP)
    
    def _btn_generate(self, sender, app_data):
        show_btn_save_flag = True

        # clear error messages
        for input_error_tag in ["__text_input_error", "__bpm_input_error", "__filename_input_error"]:
            dpg.configure_item(item=input_error_tag, show=False)

        values = dpg.get_values(["__text_input", "__bpm_input", "__filename_input"])
        
        # verify input values
        if not values[0]:
            self._show_error("__text_input_error", "Text input is required")
            show_btn_save_flag = False
        
        if not (self.MIN_BPM_VALUE <= int(values[1]) <= self.MAX_BPM_VALUE):
            self._show_error("__bpm_input_error", f'BPM value must be between {self.MIN_BPM_VALUE} and {self.MAX_BPM_VALUE}')
            show_btn_save_flag = False
        
        if not values[2]:
            self._show_error("__filename_input_error", "Filename is required and can't contain an extension in the name")
            show_btn_save_flag = False

        # TODO: generate the song (integrate with our application)
        if show_btn_save_flag:
            dpg.configure_item(item="btn_save", show=True)
            
    def _show_error(self, tag, text):
        dpg.configure_item(item=tag, default_value=text, show=True, color=(255, 0, 0, 255))

    def _btn_save(self):
        # TODO: check if was generated
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
            dpg.add_input_text(tag="__text_input", multiline=True)
            dpg.add_text(tag="__text_input_error", show=False)
            
            # Input BPM
            dpg.add_text("BPM")
            dpg.add_input_int(tag="__bpm_input", min_value=self.MIN_BPM_VALUE, max_value=self.MAX_BPM_VALUE, min_clamped=True, max_clamped=True)
            dpg.add_text(tag="__bpm_input_error", show=False)
            
            # Input Filename
            dpg.add_text("Filename")
            dpg.add_input_text(tag="__filename_input")
            dpg.add_text(tag="__filename_input_error", show=False)
            
            dpg.add_button(label="Generate", callback=self._btn_generate)
            
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

            dpg.add_button(tag="btn_save", label="Save", callback=self._btn_save, show=False)
