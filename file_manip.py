from revember_data_classes import FunctObject

class CFileManip:

    def __init__(self):
        self.include = '#include "revEMBer.h"\n'
        self.comment = "/* \nTHIS FILE HAS ADDED DEBUG INFORMATIONS \n revEMBer projct in github: https://github.com/uKarol/revEMBer \njefvcoe oefpm d actmdhsae\n*/\n"
        
        self.to_be_added = { "begin" : ' /* function begin */ ',
                             "ret" : ' /* function return */ ',
                             "end" : '/* function end */ ',
        }   

    def add_include_info(self, lines):
        lines[0] = self.comment + self.include + lines[0]

    def add_sequence_in_begin(self, line:str, sequence_to_add: str):
        
        ret_val = line

        if '{' in line:
            if line.strip().endswith('{'):
                ret_val = line + sequence_to_add
            else:
                substrs = line.split('{', maxsplit= 1)
                ret_val = substrs[0] + '{\n' + sequence_to_add + substrs[1]
        
        return ret_val
    

    def add_sequence_in_end(self, line: str, sequence_to_add: str):
        
        ret_val = line

        if '}' in line:
            if line.strip().startswith('}'):
                ret_val = sequence_to_add + line
            else:
                substrs = line.split('}', maxsplit= 1)
                ret_val = substrs[0] + '\n' + sequence_to_add + substrs[1] + '}'
        
        return ret_val

    def add_sequence_in_return(self, line: str, sequence_to_add: str):
        ret_val = line 
        if 'return' in line:
            if line.strip().startswith('return'):
                ret_val =  sequence_to_add + line
            else:
                substrs = line.split('return', maxsplit= 1)
                ret_val = substrs[0] + sequence_to_add + "return " + substrs[1]

        return ret_val

    def add_dbg_fun(self, functions_to_change: FunctObject, lines):
            
            function_begin_ln = functions_to_change.begin
            function_rets = functions_to_change.returns
            function_end_ln = functions_to_change.end
            
            lines[function_begin_ln] = self.add_sequence_in_begin(lines[function_begin_ln], self.to_be_added["begin"] + ' \n')

            if type(function_rets) == int: 
                lines[function_rets] = self.add_sequence_in_return(lines[function_rets], self.to_be_added["ret"] + ' \n')
            elif len(function_rets) > 0:
                for ret in function_rets.split():
                    ret = int(ret)
                    lines[ret] = self.add_sequence_in_return(lines[ret], self.to_be_added["ret"] + ' \n')
            
            else: 
                print(function_rets.split())
                lines[function_end_ln] = self.add_sequence_in_end(lines[function_end_ln], self.to_be_added["end"] + ' \n')


    def add_dbg_functions(self, filepath, functions_to_change: list):

        with open(filepath, 'r+') as file:
            
            lines = file.readlines()
            
            self.add_include_info(lines)

            for function_obj in functions_to_change:
                self.add_dbg_fun(function_obj, lines)

            file.seek(0)
            
            file.writelines(lines)

# fman = CFileManip()

# fun0 = FunctObject("intializer", 37, [41], 42)
# fun1 = FunctObject("pattern7", 90, [], 91)
# fun2 = FunctObject("pattern8", 97, [], 99)
# fun3 = FunctObject("pattern9", 106, [], 108)

# fdict = {"initializer" : fun0,
#          "pattern7" : fun1,
#          "pattern8" : fun2,
#          "pattern9" : fun3,
#          }

# fman.add_dbg_functions("main.cpp", fdict)



 