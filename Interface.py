import dearpygui.dearpygui as dpg

class Interface:
    """
    Interface: a classe gerencia a criação e interação com a interface gráfica usando Dear PyGui.
    Contém os métodos para ler o texto de entrada do usuário.
    """

    # Initializes Dear PyGui context and setup interface (public)
    def __init__(self):
        dpg.create_context()
        self._setup_interface()
        dpg.create_viewport(title='Title', width=720, height=720)
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
        width = 500
        height = 400
        with dpg.window(label="Help Window", width=width, height=height, show=True, no_collapse=True, no_resize=False):
            with dpg.group(width=width):
                dpg.add_text("The main goal of the software is to generate music from text.", wrap=width-20)
                dpg.add_separator()
                dpg.add_text("The software receives as input an unstructured text (like a short story or newspaper page) and generates a set of notes corresponding to the text according to some parameters (like timbre, rhythm, BPM). The parameters are defined via a mapping of text to musical information.", indent= 1, wrap=width-20)

    # Buttons Functions (private)
    def _btn_generate(self):
        values = dpg.get_values(["__text_input", "__bpm_input", "__filename_input"])
        if (values[0] and values[1] and values[2]):
            # TODO: add loading indicator, set UserInput
            print("penis certo")
            pass
        else:
            # TODO: add popup not valid
            print("penis errado")
            pass

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

            dpg.add_text("Your Text")
            dpg.add_input_text(tag="__text_input", multiline=True)
            dpg.add_text("BPM")
            dpg.add_input_int(tag="__bpm_input", min_value=0, max_value=200, min_clamped=True, max_clamped=True)
            dpg.add_text("Filename")
            dpg.add_input_text(tag="__filename_input")
            dpg.add_button(label="Generate", callback=self._btn_generate)
            dpg.add_separator()
            dpg.add_button(label="Save", callback=self._btn_save)
