from __future__ import annotations
from abc import ABC, abstractmethod
import re
from revember_function_parser.revember_function_parser_data_classes import *

SIGNLE_LINE_BLOCK = 0
BLOCK_BEGIN = 1
BLOCK_END = 2
NOT_DETECTED = 3


class BlockExtractorState(ABC):

    @property
    def context(self) -> BlockExtractor:
        return self._context
    
    @context.setter
    def context(self, context: BlockExtractor):
        self._context = context

    @abstractmethod
    def process_line(self, line, line_num) -> None:
        pass

    @abstractmethod
    def block_begin(self):
        pass

    @abstractmethod
    def block_end(self):
        pass

    @abstractmethod
    def semicolon_found(self):
        pass

class BlockExtractor:

    _state = None

    def __init__(self):
        self.transition_to(OutFunction())
        self.current_level = 0
        self.entry_level = 0

        #last values
        self.last_signature = ""
        self.function_begin_line = 0
        self.function_end_line = 0
        self.last_returns = []
        self.last_warnings = []
        #global data
        self.found_functions = {}


    def update_function_dict(self):
        new_fun = {self.last_signature : FUnctionParser_FunctData(self.last_signature,
                                                                            [],
                                                                            self.function_begin_line,
                                                                            self.function_end_line,
                                                                            self.last_returns,
                                                                            [],
                                                                            [],
                                                                            )}
        #print(new_fun)
        self.found_functions.update(new_fun)
        self.last_signature = ""
        self.function_begin_line = 0
        self.function_end_line = 0
        self.last_returns = []
        self.last_warnings = []
    
    def get_found_functions(self):
        return self.found_functions

    def transition_to(self, state : BlockExtractorState):
        self._state = state
        self._state.context = self

    def block_splitter(self, line):
        processed_line = []
        start = 0
        ctr = 0
        for ch in line:
            if ch == "{":
                processed_line.append(line[start:ctr])
                start = ctr + 1
                processed_line.append( "BLOCK START DETECTED" )
            elif ch == "}":
                processed_line.append(line[start:ctr])
                start = ctr + 1
                processed_line.append( "BLOCK END DETECTED" )
            elif ch == ";":
                processed_line.append(line[start:ctr])
                start = ctr + 1
                processed_line.append( "SEMICOLON DETECTED" )
            ctr = ctr+1
        processed_line.append(line[start:len(line)])
        return processed_line


    def process_line(self, line, line_num):

        if( "}" in line or "{" in line or ";" in line ):
            s_line = self.block_splitter(line)

            for s in s_line:
                if( s == "BLOCK START DETECTED" ):
                    self._state.block_begin(line_num)
                elif( s == "BLOCK END DETECTED" ):
                    self._state.block_end(line_num)
                elif( s == "SEMICOLON DETECTED" ):
                    self._state.semicolon_found(line_num)
                else:
                    self._state.process_line(" " + s, line_num)
        else:
            self._state.process_line(" " + line, line_num)

class InFunction(BlockExtractorState):

    def __init__(self):
        self.expression_begin = 0
        self.keyword_pos = 0
        self.expression_end = 0
        self.last_expression = ""

    def process_line(self, line, line_num) -> None:
        if line != "":
            if(self.expression_begin == 0):
                self.expression_begin = line_num
            self.last_expression = self.last_expression + " " + line

    def block_begin(self, line_num):
        self.context.current_level = self.context.current_level + 1
        self.expression_begin = 0
        self.last_expression = ""

    def block_end(self, line_num):
        self.context.current_level = self.context.current_level - 1
        if(self.context.current_level == self.context.entry_level):
            self.function_end_line = line_num
            self.context.update_function_dict()
            self.context.transition_to(OutFunction())
        self.expression_begin = 0

    def semicolon_found(self, line_num):
        self.expression_end = line_num
        ret = find_keywords(self.last_expression, self.expression_begin, self.expression_end)
        if(ret != None):
            self.context.last_returns.append(ret)
        self.keyword_pos = 0
        self.expression_end = 0
        self.last_expression = ""

class OutFunction(BlockExtractorState):

    def __init__(self):
        self.last_expression = ""

    def process_line(self, line, line_num) -> None:
        self.last_expression = self.last_expression + " " + line

    def block_begin(self, line_num):
        if( check_function_signature(self.last_expression) == True ):
            self.context.entry_level = self.context.current_level
            self.context.last_signature = self.last_expression
            self.context.transition_to(InFunction())
            self.function_begin_line = line_num
        self.context.current_level = self.context.current_level + 1

    def block_end(self, line_num):
        self.context.current_level = self.context.current_level - 1
        self.last_expression = ""

    def semicolon_found(self, line_num):
        self.last_expression = ""


def find_keywords(text, expression_begin, expression_end):
    return check_return(expression_begin, expression_end, text)


def check_return(start, end, block):  
    need_extra_brackets = False
    ret_warnings = ""
    pattern = r"return(.*?)\;"
    match = re.split(pattern, block)
    ret_val = None
    if (" return" in block or ")return" in block ) and len(match) > 1:
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

def check_function_signature(text):
    #print("checking signature")
    if( "(" in text) and (")" in text):
        print(text)
        return True
    else:
        return False

if __name__ == "__main__":

    cntx = BlockExtractor()
    cntx.process_line("void count();",0)
    cntx.process_line("void count2()",0)
    cntx.process_line("{",1)
    cntx.process_line("",2)
    cntx.process_line("add();",3)
    cntx.process_line("*/x--",4)
    cntx.process_line("xx}",5)
