# Filename: splitter.py
# Author: Karol Ujda (uKarol)
# Description: Searching function begin, end and return statements

from revember_data_classes import FunctObject

SUCCESS = 0
INCOMPLETE = 1
FAILURE = 2

class cascased_split:

    def __init__(self):
        self.stage = 0
        self.splitt_str = ['{', '}']
        self.fun_list = ['','','','']
        self.unallowed_words_in_stage = [ ['=',';'],[], [] ]
        self.last_result = []
        self.function_begin = 0
        self.function_end = 0
        self.return_statements = []
        self.last_returns = []

        self.token_validation = [self.token_stage0_validate, self.token_stage1_validate]
        self.stage_validation = [self.stage_0_validate, self.stage_1_validate]

    def token_stage0_validate(self, token, line_num):
        ret_val = True
        if( any(wrd in token for wrd in self.unallowed_words_in_stage[self.stage]) ):
            ret_val = False
        return ret_val

    def token_stage1_validate(self, token, line_num):
        if('return' in token):
            self.return_statements.append(line_num)
        return True

    def stage_1_validate(self, line_num):
        return True

    def stage_0_validate(self, line_num):
        self.function_begin = line_num
        signature = self.fun_list[0]
        if( len(signature) > 0) and ('(' in signature) and ( ')' in signature ):
            return True
        else:
            return False 

    def reset_variables(self):
        self.fun_list = ['','','','']
        self.stage = 0
        self.return_statements = []

    def add_val(self, new_val):
        to_be_added = self.fun_list[self.stage]
        new_val = to_be_added + new_val
        self.fun_list[self.stage] = new_val

    
    def validate_stage(self, line_num):
        if self.stage == 0:
            self.function_begin = line_num
            return self.stage_0_validate()
        else: 
            return True

    
    def get_function_begin(self):
        return FunctObject(self.last_result[0], self.function_begin, self.last_returns, self.function_end)

    def get_function_signature(self):
        return self.last_result[0]

    def c_splitter(self, line, line_num):

        to_be_added: str
        next_token = "test"
        state_transition = False
        while(len(next_token) > 0):

            if(self.splitt_str[self.stage] in line):
                splitted = line.split(self.splitt_str[self.stage]) 
                to_be_added = splitted[0]
                next_token = splitted[1]
                state_transition = True
            else:
                to_be_added = line
                state_transition = False

            if self.token_validation[self.stage](to_be_added, line_num) == True:
                self.add_val(to_be_added)
            else:
                self.reset_variables()
                return FAILURE 

            if(state_transition == True):
                if(self.stage_validation[self.stage](line_num) == True):
                    self.stage = self.stage + 1

                    if(self.stage == len(self.splitt_str)):
                        self.function_end = line_num
                        self.last_result = self.fun_list
                        self.last_returns = self.return_statements
                        self.reset_variables()
                        return SUCCESS
                    else:
                        line = next_token
                else:
                    self.reset_variables()
                    return FAILURE
            else:
                return INCOMPLETE    
