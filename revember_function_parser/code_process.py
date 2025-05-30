# Filename: code_process.py
# Author: Karol Ujda (uKarol)
# Description: Searching function begin, end and return statements

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

    def __init__(self, keyword_analyzer):
        self.transition_to(OutFunction())
        self.current_level = 0
        self.entry_level = 0
        self.repetition_ctr = 0
        self.keyword_analyzer = keyword_analyzer

        self.last_signature = ""
        self.function_begin_line = 0
        self.function_end_line = 0
        self.last_returns = []
        self.last_warnings = []
        self.found_functions = {}
        self.last_found_parametrers = []
        self.last_revember_artifacts = []

    def update_function_dict(self):
        fn_key = self.last_signature
        if(fn_key in self.found_functions):
            fn_key = fn_key+str(self.repetition_ctr)
            self.repetition_ctr = self.repetition_ctr + 1
        new_fun = {fn_key : FUnctionParser_FunctData(fn_key,
                                                     self.last_found_parametrers,
                                                     self.function_begin_line,
                                                     self.function_end_line,
                                                     self.last_returns,
                                                     [],
                                                     self.last_revember_artifacts,
                                                    )}
        self.found_functions.update(new_fun)
        self.last_signature = ""
        self.function_begin_line = 0
        self.function_end_line = 0
        self.last_returns = []
        self.last_warnings = []
        self.last_found_parametrers = []
        self.last_revember_artifacts = []
    
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
        if line.strip() != "":
            if(self.expression_begin == 0):
                self.expression_begin = line_num
            
            if(self.context.keyword_analyzer.find_revember_artifacts(line, line_num, self.context.last_revember_artifacts)== False):
                self.last_expression = self.last_expression + line

    def block_begin(self, line_num):
        self.context.current_level = self.context.current_level + 1
        self.expression_begin = 0
        self.last_expression = ""

    def block_end(self, line_num):
        self.context.current_level = self.context.current_level - 1
        if(self.context.current_level == self.context.entry_level):
            self.context.function_end_line = line_num
            self.context.update_function_dict()
            self.context.transition_to(OutFunction())
        self.expression_begin = 0

    def semicolon_found(self, line_num):
        self.expression_end = line_num
        ret = self.context.keyword_analyzer.find_keywords(self.last_expression, self.expression_begin, self.expression_end)
        if(ret != None):
            self.context.last_returns.append(ret)
        self.expression_begin = 0    
        self.keyword_pos = 0
        self.expression_end = 0
        self.last_expression = ""

class OutFunction(BlockExtractorState):

    def __init__(self):
        self.last_expression = ""

    def process_line(self, line, line_num) -> None:
        self.last_expression = self.last_expression + line

    def block_begin(self, line_num):
        if( self.context.keyword_analyzer.check_function_signature(self.last_expression, self.context.last_found_parametrers) == True ):
            self.context.entry_level = self.context.current_level
            self.context.last_signature = self.last_expression.strip()
            self.context.function_begin_line = line_num
            self.context.transition_to(InFunction())
        else:
            self.context.last_found_parametrers = []
        self.last_expression = ""
        self.context.current_level = self.context.current_level + 1
        


    def block_end(self, line_num):
        self.context.current_level = self.context.current_level - 1
        self.last_expression = ""

    def semicolon_found(self, line_num):
        self.last_expression = ""




if __name__ == "__main__":

    cntx = BlockExtractor()
    cntx.process_line("void count();",0)
    cntx.process_line("void count2()",0)
    cntx.process_line("{",1)
    cntx.process_line("",2)
    cntx.process_line("add();",3)
    cntx.process_line("*/x--",4)
    cntx.process_line("xx}",5)
