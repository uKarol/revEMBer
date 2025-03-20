# Filename: revEMBer_controller.py
# Author: Karol Ujda (uKarol)
# Description: Controller of revEMBer
from revember_view import *
from revember_file_manip.file_manip import CFileManip
from revember_function_parser.cascaded_extractor import *
from revember_view.testing_gui import *


class revemberModel:

    def __init__(self):
        self.selected_files = []
        self.selected_functions = {} 

    def add_file(self, file):
        self.selected_functions.update({file : {}})

    def add_functions(self, file, function_name, function_data):
        self.selected_functions[file].update({function_name:function_data})
    
    def get_files(self):
        return self.selected_functions.keys()

    def get_functions(self, file):
        return self.selected_functions[file].keys()

    def get_function_data(self, file, function):
        return self.selected_functions[file][function]


class revEMBer_controller:

    def __init__(self, model, view):
        self.model = revemberModel()
        self.view = view
        self.view.setup(self)
        self.current_file = ""

    def process_selected_functions(self):
        functions_to_be_changed = {}
        items = self.view.get_selected_functions()
        user_function = self.view.get_user_functions()
        fman = CFileManip()
        for file in items:
            for function in items[file]:
                functions_to_be_changed.update({function.name : self.model.get_function_data(file, function.name)})
            #print("FILE" + file)
            #print(functions_to_be_changed)
            fman.add_dbg_functions(file, functions_to_be_changed, user_function)
            functions_to_be_changed= {}

    def process_selected_files(self):
        selected_files = self.view.get_selected_files()
        for file in selected_files:
            self.model.add_file(file)
            self.search_file(file)

    def search_file(self, path):
        self.current_file = path
        self.func_finder = FunctionDetector()
        self.func_finder.search_file(path)
        found_functions = self.func_finder.get_found_functions()
        self.view.add_file(path)
        for ffunction in found_functions:
            self.model.add_functions(path, ffunction, found_functions[ffunction])
            self.view.add_function(path, found_functions[ffunction].name, 0, 0, 0)

    def start_app(self):
        self.view.start()


my_view = revEMBer_view()

revember_ctl = revEMBer_controller(None, my_view)

revember_ctl.start_app()