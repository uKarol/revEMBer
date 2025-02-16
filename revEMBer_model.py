import revember_data_classes

class revember_model:

    def __init__(self):
        self.file_list = []
        self.function_list = []
        self.found_functions = {}

    def add_file(self, file):
        self.file_list.append[file]
        self.found_functions.update({file : None})

    def get_files(self):
        return self.file_list

    def get_functions_from_file(self, file_name):
        return self.found_functions[file_name]

    #def get_all_functions(self):

    def add_functions_to_file(self, file_name, function_name, function_data):
        self.found_functions[file_name].update({function_name : self.found_functions[function_name]})