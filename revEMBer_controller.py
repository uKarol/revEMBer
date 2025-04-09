# Filename: revEMBer_controller.py
# Author: Karol Ujda (uKarol)
# Description: Controller of revEMBer
from revember_view import *
from revember_file_manip.file_manip import CFileManip
from revember_function_parser.cascaded_extractor import *
from revember_view.revember_view import *


class revemberModel:

    def __init__(self):
        self.selected_files = []
        self.selected_functions = {} 
        self.to_be_added = {"inc" :  '#include "revEMBer.h"',
                            "begin" : 'REVEMBER_FUNCTION_ENTRY()',
                            "ret" : 'REVEMBER_FUNCTION_EXIT()',
                            "end" : 'REVEMBER_FUNCTION_EXIT()',
                            "warning" :'REVEMBER_GENERIC_WARNING'
        }   
        self.warnings = ['#warning "improper return statement - add revember macros manually"']
    
    def get_revember_warnigns(self):
        return self.warnings

    def get_revember_functions(self):
        return self.to_be_added

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

    def delete_all_functions(self):
        self.selected_files = []
        self.selected_functions = {} 


class revEMBer_controller:

    def __init__(self, model, view):
        self.model = revemberModel()
        self.view = view
        self.view.setup(self)
        self.current_file = ""

    def process_selected_functions(self):
        functions_to_be_changed = {}
        items = self.view.get_selected_functions()
        selection_mod = self.view.get_user_functions()
        user_function = self.model.get_revember_functions()
        fman = CFileManip()
        for file in items:
            for function in items[file]:
                functions_to_be_changed.update({function.name : self.model.get_function_data(file, function.name)})
            fman.add_dbg_functions(file, functions_to_be_changed, user_function, selection_mod)
            functions_to_be_changed= {}
        
        self.view.del_all_functions()
        self.process_selected_files()

    def process_selected_files(self):
        self.view.del_all_functions()
        self.model.delete_all_functions()
        selected_files = self.view.get_selected_files()
        for file in selected_files:
            self.model.add_file(file)
            self.search_file(file)

    def remove_debug_functions(self):
        functions_to_be_changed = {}
        items = self.view.get_selected_functions_del()
        fman = CFileManip()
        for file in items:
            for function in items[file]:
                functions_to_be_changed.update({function.name : self.model.get_function_data(file, function.name)})
            fman.remove_dbg_functions(file, functions_to_be_changed)
            functions_to_be_changed= {}
        self.view.del_all_functions()
        self.process_selected_files()

    def search_file(self, path):
        self.current_file = path
        self.func_finder = FunctionDetector(list(self.model.get_revember_functions().values()), self.model.get_revember_warnigns())
        self.func_finder.search_file(path)
        found_functions = self.func_finder.get_found_functions()
        self.view.add_file(path)
        self.view.add_file_unclear(path)
        for ffunction in found_functions:
            self.model.add_functions(path, ffunction, found_functions[ffunction])
            if found_functions[ffunction].revember_artifacts == []:
                self.view.add_function(path, found_functions[ffunction].name, found_functions[ffunction].begin, found_functions[ffunction].end, found_functions[ffunction].returns)
            else:
                self.view.add_function_unclear(path, found_functions[ffunction].name, found_functions[ffunction].begin, found_functions[ffunction].end, found_functions[ffunction].returns)


    def start_app(self):
        self.view.start()


my_view = revEMBer_view()

revember_ctl = revEMBer_controller(None, my_view)

revember_ctl.start_app()