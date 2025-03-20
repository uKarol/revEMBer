# Filename: splitter.py
# Author: Karol Ujda (uKarol)
# Description: Searching function begin, end and return statements

from revember_function_parser.revember_function_parser_data_classes import FunctionParser_FunctObject

SUCCESS = 0
INCOMPLETE = 1
FAILURE = 2

class FunctionExtractor:

    def __init__(self):
        self.fun_list = ['','','','']
        self.unallowed_words_in_stage = ['=',';']
        self.last_result = []
        self.function_begin = 0
        self.function_end = 0
        self.last_returns = []
        self.last_status = FAILURE

    def token_validate(self, token):
        ret_val = True
        if( any(wrd in token for wrd in self.unallowed_words_in_stage) ):
            ret_val = False
        return ret_val


    def function_signature_validate(self):
        signature = self.fun_list[0]
        if( len(signature) > 0) and ('(' in signature) and ( ')' in signature ):
            return True
        else:
            return False 

    def reset_variables(self):
        self.fun_list = ['','','','']

    def add_val(self, new_val):
        to_be_added = self.fun_list[0]
        new_val = to_be_added + new_val
        self.fun_list[0] = new_val
    
    def get_function_begin(self):
        return FunctionParser_FunctObject(self.last_result[0], [] , self.function_begin, self.function_end)

    def get_function_signature(self):
        return self.last_result[0]
    
    def block_begin(self, line_num):
        if(self.function_signature_validate() == True):
            self.last_status = SUCCESS
            self.function_begin = line_num
        else:    
            self.last_status = FAILURE
            self.reset_variables()

    def block_end(self, line_num):
        if self.last_status == SUCCESS:
            self.function_end = line_num
            self.function_end = line_num
            self.last_result = self.fun_list
            self.reset_variables()
        return self.last_status

    def process_line(self, line, line_num):
        if self.token_validate(line) == True:
            self.last_status = INCOMPLETE
            self.add_val(line)
        else:
            self.last_status = FAILURE
            self.reset_variables()
