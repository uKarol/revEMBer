import re
from dataclasses import dataclass

@dataclass
class FunctionParam:
    type_name:str
    param_name:str 

        
class ParamExtractor:

    def __init__(self):
        self.br_ctr = 0
        self.param_list = []

    def bracket_counter(self, ch):
        if(ch == '('):
            self.br_ctr = self.br_ctr + 1
        elif(ch == ')'):
            self.br_ctr = self.br_ctr - 1

    def split_params(self, params):
        for param in params:
            
            if re.search(r'\(*\)', param):
                param = param.split(')')[0]
                param = param.replace("(", "")    
            
            ptr = re.search(r'[*]+', param)
            if ptr:
                strs = re.split(r'[*]+', param)
                self.param_list.append(FunctionParam(strs[0] + ptr.group(0), strs[1]))
            else:
                strs = param.split()
                self.param_list.append(FunctionParam(strs[0], strs[1]))         


    def process_function(self, function_str):
        divided_fun = self.pts_divider(function_str)
        temp_param_list = self.parse_params(divided_fun[len(divided_fun)-1])
        self.split_params(temp_param_list)


    def parse_params(self, param_str):
        start = 0
        temp_param_list = []
        for i in range(0, len(param_str)):
            self.bracket_counter(param_str[i])
            if(param_str[i] == ",") and (self.br_ctr == 0):
                temp_param_list.append(param_str[start:i])
                start = i+1
        temp_param_list.append(param_str[start:len(param_str)])
        self.br_ctr = 0
        return temp_param_list

    def pts_divider(self, str):
        ret_val = []
        divided = str.split("(", maxsplit = 1)
        ret_val.append(divided[0])
        str2 = divided[1]
        ctr = 1
        start = 0
        for i in range(0, len(str2)):
            if(str2[i] == '('):
                if(ctr == 0):
                    start = i+1
                ctr = ctr + 1
            elif(str2[i] == ')'):
                ctr = ctr - 1
                if(ctr == 0):
                    ret_val.append(str2[start:i])  
        return ret_val
    
    def get_params(self):
        ret_val = self.param_list
        self.param_list = []
        return ret_val
    
if __name__ == "__main__":
    fun = "int* (*(*fpData)(const char *))(int (*paIndex)[3] , int (* fpMsg) (const char *), int (* fpCalculation[3]) (const char *), int x);"
    fun2 = "void calc(int a, int b, int (*op)(int, int), char     cc)"
    fun3 = "int32_t BSP_COM_RegisterMspCallbacks(COM_TypeDef COM , BSP_COM_Cb_t *Callback)"

    extr = ParamExtractor()
    extr.process_function(fun)
    for param in extr.get_params():
        print(param)

    extr.process_function(fun2)
    for param in extr.get_params():
        print(param)
            
    extr.process_function(fun3)
    for param in extr.get_params():
        print(param)

