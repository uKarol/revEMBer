# Filename: keyword_analyzer.py
# Author: Karol Ujda (uKarol)
# Description: Searching keywords, checking code

from revember_function_parser.function_signature_analyzer import FunctionAnalyzer, ParenthesisProcessing


def keyword_variants_gen(basic_kw, rw):
    keyword_variants = []
    if(rw == 'w'):
        write_operators = [ "=", "|=" , "^=", "&=" ]
        for operator in write_operators:
            keyword_variants.append(basic_kw+operator)
            keyword_variants.append(basic_kw+" "+operator)
    elif(rw == 'w'):
        read_operators_left = [ "=", "!=" , "=="]
        read_operators_right = [ "==", "!="]
        for operator in read_operators_left:
            keyword_variants.append(basic_kw + operator)
            keyword_variants.append(basic_kw+" "+operator)

        for operator in read_operators_right:
            keyword_variants.append(operator + basic_kw)
            keyword_variants.append(operator+" "+ basic_kw)
    else:
        keyword_variants = [ f" {basic_kw} ", f"){basic_kw}(", f"){basic_kw} ", f" {basic_kw}(" ]

    return keyword_variants

class KeywordAnalyzer:

    def __init__(self, revember_artifacts):
        self.revember_artifacts = revember_artifacts # ["REVEMBER_FUNCTION_ENTRY", "REVEMBER_FUNCTION_EXIT"]

    def find_revember_artifacts(self, line, line_num, rev_art):
        if any(word in line for word in self.revember_artifacts):
            rev_art.append(line_num)

    def find_keywords(self, text, expression_begin, expression_end):
        text = text + " "
        keyword = "return"
        kw_variants = keyword_variants_gen(keyword, 0)
        if any(word in text for word in kw_variants):
            return self.check_return(expression_begin, expression_end, text, keyword)


    def check_return(self, start, end, block, keyword):  
        need_extra_brackets = False
        ret_warnings = ""
        match = block.split(keyword)
        ret_val = None
        pts = ParenthesisProcessing()
        to_be_checked = block
        if len(match) > 1:
            to_be_checked = match[1]
            if match[0].strip().endswith(")"):
                need_extra_brackets = True
            pts_ret = pts.process_expression(match[1])
            if(None == pts.process_expression(match[0])):
                ret_warnings = "improper return statement"
            elif pts_ret[0] > 0:
                ret_warnings = "compound return value"
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