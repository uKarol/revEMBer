from file_manip import *
from detector import *
from testing_gui import *

class experimental_controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.setup(self)
        self.current_file = ""

    def get_selected_items(self):
        items = self.view.get_selected_item()
        temp_dict = {}
        for item in items:
            temp_dict.update({item : self.found_functions[item]})
        fman = CFileManip()
        fman.add_dbg_functions(self.current_file, temp_dict)


    def process_selected_functions(self):
        print(self.view.get_selected_functions())

    def process_selected_files(self):
        selected_files = self.view.get_selected_files()
        for file in selected_files:
            self.search_file(file)

    def search_file(self, path):
        self.current_file = path
        self.func_finder = cascaded_function_finder()
        self.func_finder.search_file(path)
        found_functions = self.func_finder.get_found_functions()
        self.view.add_file(path)
        for ffunction in found_functions:
            self.view.add_function(path, found_functions[ffunction].name, found_functions[ffunction].begin, found_functions[ffunction].end, found_functions[ffunction].returns)

    def start_app(self):
        self.view.start()


my_view = mainviev()

revember_ctl = experimental_controller(None, my_view)

revember_ctl.start_app()