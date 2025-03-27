import re

class ParenthesisProcessing:

    def __init__(self):
        self.max_depth = 0
        self.found_substrings = [[]]
        self.processed_subs = []


    def process_expression(self, expression):
        if(self.process_string(expression)):
            self.reprocess_string()
            ret_val = self.get_substrings()
        else:
            ret_val = None
            self.max_depth = 0
            self.found_substrings = [[]]
            self.processed_subs = []
        return ret_val 

    def process_string(self, text):
        
        stage_params = []
        current_depth = 0
        ctr = 0
        self.found_substrings[0].append(text)
        stage_params.append({})
        ret_val = 1
        if(text.count("(") == text.count(")") ): 
            try:    
                for ch in text:
                    if ch == '(':
                        current_depth = current_depth + 1
                        if(self.max_depth < current_depth):
                            self.max_depth = current_depth
                            self.found_substrings.append([])
                            stage_params.append({})
                        stage_params[current_depth].update({"begin": ctr})
                    
                    elif ch == ')':
                        stage_params[current_depth].update({"end": ctr+1})
                        self.found_substrings[current_depth].append(text[ stage_params[current_depth]["begin"] : stage_params[current_depth]["end"] ])
                        current_depth = current_depth - 1
                    ctr = ctr + 1
            except KeyError:
                self.found_substrings = ["FAILURE"]
                self.max_depth = 0
                ret_val = 0
        else:
            self.found_substrings = ["FAILURE"]
            self.max_depth = 0
            ret_val = 0
        return ret_val
    
    def reprocess_string(self):
        
        for i in range(0, self.max_depth):
            self.processed_subs.append([])
            temp = []
            for string in self.found_substrings[i]:
                
                ctr = 0
                for strx in self.found_substrings[i+1]:
                    if strx in string:
                        string = string.replace(strx, f" #substituted_{i+1}_{ctr} ")
                    ctr = ctr + 1
                temp.append(string)
            self.processed_subs[i] = temp
        self.processed_subs.append(self.found_substrings[self.max_depth])
                
    def get_substrings(self):
        ret_val = (self.max_depth, self.found_substrings , self.processed_subs)
        self.max_depth = 0
        self.found_substrings = [[]]
        self.processed_subs = []
        return ret_val
    

class FunctionAnalyzer:
    
    def process_function(self, function_signature):
        ret_val = None
        pts_parser = ParenthesisProcessing()
        result = pts_parser.process_expression(function_signature)
        if(result != None):
            (max_depth, self.found_substrings, processed_subs) = result
            params = processed_subs[1][-1]
            ret_val = self.split_params(params)
        return ret_val

    def preprocess_param(self, param):
        param = param.strip()
        if "(" in param:
            param = param.replace("(", "")
        if ")" in param:
            param = param.replace(")", "")
        return param

    
    def split_params(self, params):
        param_name = ""
        param_type = ""
        ret_params = []
        param_list = params.split(",")
        for param in param_list:
            param = self.preprocess_param(param)

            splitted_params = param.split()
            if len(splitted_params) == 0:
                pass
            elif len(splitted_params) == 1:
                param_type = splitted_params[0]
            elif len(splitted_params) == 2:
                param_type = splitted_params[0]
                param_name = splitted_params[1]
                
            else:
                function_name = splitted_params[1] 
                if ("#substituted_" in function_name):
                    name_pos = function_name.split("#substituted_")[1]
                    name_pos = name_pos.split("_")
                    function_name = self.found_substrings[int(name_pos[0])][int(name_pos[1])]
                    function_name = self.preprocess_param(function_name)
                    function_name = function_name.replace("*", "")
                    param_type = "function_ptr"
                    param_name = function_name
                else:
                    param_type = splitted_params[0]
                    for i in range(1, len(splitted_params)-1): 
                        param_type = param_type+" " + splitted_params[i]
                    param_name = splitted_params[-1]

            
            if("*" in param_name):
                match = re.search(r'[*]+', param_name)
                param_type = param_type + match.group(0)
                param_name = param_name.replace(match.group(0), "")

            ret_params.append({"param_type": param_type, "param_name": param_name})
        return ret_params



if __name__ == "__main__":

    def pretty_print(params):
        (max_depth, found_substrings, processed_subs) = params
        print("  substrings  ")
        for subs in found_substrings:
            print(subs)
        for subs in processed_subs:
            print(subs)
        print(found_substrings[max_depth])


    #pts_parser = ParenthesisProcessing()

    fun = "int* (*(*fpData)(const char *))(int (*paIndex)[3] , int (* fpMsg) (const char *), int (* fpCalculation[3]) (const char *, int x), int x);"
    fun2 = "void calc(int a, int b, int (*op)(int, int), char     cc)"
    fun3 = "int32_t BSP_COM_RegisterMspCallbacks(COM_TypeDef COM , BSP_COM_Cb_t *Callback)"


    # pretty_print(pts_parser.process_expression("int search(void)"))
    # print()

    # pretty_print(pts_parser.process_expression(fun))
    # print()
    # ()

    # pretty_print(pts_parser.process_expression(fun2))
    # print()

    # pretty_print(pts_parser.process_expression(fun3))
    # print()

    parser = FunctionAnalyzer()

    print(parser.process_function("int search(void)"))
    print(parser.process_function(fun))
    print(parser.process_function(fun2))
    print(parser.process_function(fun3))