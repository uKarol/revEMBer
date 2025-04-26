from revember_data_classes import FunctObject

class CFileManip:

    def __init__(self):

        self.comment = "/* \nTHIS FILE HAS ADDED DEBUG INFORMATIONS \n revEMBer projct in github: https://github.com/uKarol/revEMBer \njefvcoe oefpm d actmdhsae\n*/\n"
        self.to_be_added = {}   

    def add_include_info(self, lines):
        lines[0] = self.comment + self.to_be_added["inc"] + '\n' + lines[0]
    

    def add_params(self, param_list):
        param_num = len(param_list[0])
        str_to_add = ""
        if(param_num == 1) and (param_list[0][0]["param_name"] ==""):
            pass
        elif(param_num > 0):
            str_to_add = f"REVEMBER_FUNCTION_PARAMETERS({param_num}"
            for param in param_list[0]:
                if param["param_type"] == "" or param["param_name"] =="":
                    continue
                if param["param_type"] == "function_ptr":
                    param_t = "FUNCTION_POINTER"
                elif '*' in param["param_type"]: 
                    param_t = "VARIABLE_POINTER"
                else:
                    param_t = "RAW_VALUE"
                to_be_added = f', {param_t}, {param["param_name"]}'
                str_to_add = str_to_add + to_be_added
            str_to_add = str_to_add + ')\n'
        return str_to_add

    def add_sequence_in_begin(self, line:str, sequence_to_add: str):
        ret_val = line
        if '{' in line:
            if line.strip().endswith('{'):
                ret_val = f"{line.rstrip()}\n{sequence_to_add}"
            else:
                substrs = line.split('{', maxsplit= 1)
                ret_val = f"{substrs[0]} {{\n {sequence_to_add} {substrs[1]} "
        return ret_val
    
    def add_sequence_in_end(self, line: str, sequence_to_add: str):
        ret_val = line
        if '}' in line:
            if line.strip().startswith('}'):
                ret_val = sequence_to_add + line
            else:
                substrs = line.split('}', maxsplit= 1)
                ret_val = f"{substrs[0]} \n {sequence_to_add} {substrs[1]} }}"
        return ret_val

    def add_sequence_in_keyword(self, line: str, sequence_to_add: str, add_brace, keyword):
        ret_val = line 
        prefix = ""
        if(add_brace == True):
            prefix = "{\n"
        if keyword in line:
            if line.strip().startswith(keyword):
                ret_val =  prefix + sequence_to_add + line
            else:
                substrs = line.split(keyword, maxsplit= 1)
                ret_val = substrs[0] + prefix + sequence_to_add + " " +keyword+ substrs[1]
        else:
            ret_val = line + prefix + sequence_to_add 
        return ret_val
    
    def add_return_sequence(self, lines, ret):
        add_ex = True
        if ret["return_warning"] == "improper return statement":
            lines[ret["begin"]] = '#warning "improper return statement - add revember macros manually" \n' + lines[ret["begin"]] 
        else:
            if ret["returned_value"] != "":
                add_ex = False
            need_braces = ret["need_brackets"]
            if need_braces == False:
                lines[ret["begin"]] = self.add_sequence_in_keyword(lines[ret["begin"]], self.to_be_added["ret"] + ' \n', need_braces, "return")
            else:
                for idx in range (ret["begin"], ret["end"] + 1):
                    if( "return" in lines[idx] ):
                        break
                lines[idx] = self.add_sequence_in_keyword(lines[idx], self.to_be_added["ret"] + ' \n', need_braces, "return")
                lines[ret["end"]] = lines[ret["end"]] + " }\n"
        return add_ex

    def add_dbg_fun(self, functions_to_change, lines, mod_selection):
            function_begin_ln = functions_to_change.begin
            function_rets = functions_to_change.returns
            function_end_ln = functions_to_change.end
            add_ex = True
            params = ""

            if(mod_selection["param"]):
                params = self.add_params(functions_to_change.parameters)    

            if(mod_selection["begin"]):
                lines[function_begin_ln] = self.add_sequence_in_begin(lines[function_begin_ln], self.to_be_added["begin"] + ' \n') + params

            if(mod_selection["ret"]):
                for ret in function_rets:
                    add_ex = self.add_return_sequence(lines, ret)
                
            if add_ex and mod_selection["end"]:
                lines[function_end_ln] = self.add_sequence_in_end(lines[function_end_ln], self.to_be_added["end"] + ' \n')


    def add_dbg_functions(self, filepath, functions_to_change: list, user_functions: dict, mod_selection):

        self.to_be_added = user_functions
        add_header = True
        with open(filepath, 'r+') as file:
            content = file.read()
            if self.to_be_added["inc"] in content :
                add_header = False

        with open(filepath, 'r+') as file:
            
            lines = file.readlines()
            if add_header == True:
                self.add_include_info(lines)
            for function_obj in functions_to_change:
                self.add_dbg_fun(functions_to_change[function_obj], lines, mod_selection)

            file.seek(0)
            
            file.writelines(lines)


    def remove_dbg_functions(self, filepath, functions_to_change: list):

        with open(filepath, 'r+') as file:
            lines = file.readlines()
            for function_obj in functions_to_change:
                self.remove_dbg_fun(functions_to_change[function_obj], lines)
            file.seek(0)
            file.truncate()
            file.writelines(lines)

    def remove_dbg_fun(self, functions_to_change, lines):

            for ln in functions_to_change.revember_artifacts:
                lines[ln] = ""