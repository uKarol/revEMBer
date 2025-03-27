# Filename: keyword_analyzer.py
# Author: Karol Ujda (uKarol)
# Description: Searching keywords, checking code

from revember_function_parser.function_signature_analyzer import FunctionAnalyzer

class KeywordAnalyzer:

    def __init__(self):
        pass

    def find_keywords(self, text, expression_begin, expression_end):
        text = text + " "
        if(" return " in text or ")return " in text or " return(" in text ):
            return self.check_return(expression_begin, expression_end, text)


    def check_return(self, start, end, block):  
        need_extra_brackets = False
        ret_warnings = ""
        match = block.split("return")
        ret_val = None
        if len(match) > 1:
                if match[0].strip().endswith(")"):
                    need_extra_brackets = True
                outer_open_count = match[0].count('(')
                outer_close_count = match[0].count(')')
                inner_open_count = match[1].count('(')
                inner_close_count = match[1].count(')')
                if outer_open_count == outer_close_count:
                    if(inner_open_count == 0 and inner_open_count == 0 ):
                        ret_warnings = ""
                    elif(inner_open_count == inner_close_count):
                        ret_warnings = "compound return value"
                    else:
                        ret_warnings = "improper return statement"
                else:
                    ret_warnings = "improper return statement"

                ret_val = {"begin": start, "end" : end, "need_brackets" : need_extra_brackets, "returned_value" : match[1].strip(), "return_warning" : ret_warnings}
        return ret_val

    def check_function_signature(self, text, params_out):
        if( "(" in text) and (")" in text):
            analyzer = FunctionAnalyzer()
            ret = analyzer.process_function(text)
            params_out.append(ret)
            return True
        else:
            return False