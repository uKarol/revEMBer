from __future__ import annotations
from abc import ABC, abstractmethod
import re
from revember_function_parser.revember_function_parser_data_classes import *

SIGNLE_LINE_BLOCK = 0
BLOCK_BEGIN = 1
BLOCK_END = 2
NOT_DETECTED = 3


class BlockExtractorState(ABC):

    def block_detector(self, text:str):
        block_begin = '{'
        block_end = '}'
        if(block_begin in text.strip()) and (block_end in text.strip()):
            return SIGNLE_LINE_BLOCK
        
        elif block_begin in text.strip():
            return BLOCK_BEGIN
        
        elif block_end in text.strip():
            return BLOCK_END

        else:
            return NOT_DETECTED

    @property
    def context(self) -> BlockExtractor:
        return self._context
    
    @context.setter
    def context(self, context: BlockExtractor):
        self._context = context

    @abstractmethod
    def process_line(self, line, line_num) -> None:
        pass

class BlockExtractor:

    _state = None

    def __init__(self, out_block_processing, block_begin_cb, block_end_cb, in_block_processing):
        self.transition_to(OUTSIDE_BLOCK())
        self.out_block_processing = out_block_processing
        self.block_begin_cb = block_begin_cb 
        self.block_end_cb = block_end_cb
        self.in_block_processing = in_block_processing

    def transition_to(self, state : BlockExtractorState):
        self._state = state
        self._state.context = self

    def process_line(self, line, line_num):
        self._state.process_line(line, line_num)



class OUTSIDE_BLOCK(BlockExtractorState):

    def process_line(self, line, line_num) -> None:
        if(self.block_detector(line) == BLOCK_BEGIN):
            
            sp_line = line.split("{")
            self._context.out_block_processing(sp_line[0], line_num)
            self._context.block_begin_cb(line_num)
            self._context.in_block_processing("{" +sp_line[1], line_num)
            self.context.transition_to(IN_BLOCK())
        elif(self.block_detector(line) == SIGNLE_LINE_BLOCK):
            strs = re.split(r'[{}]', line)
            self._context.out_block_processing(strs[0], line_num)
            self._context.block_begin_cb(line_num)
            self._context.in_block_processing("{" +strs[1], line_num)
            self._context.block_end_cb(line_num)
            self._context.out_block_processing(strs[2], line_num)
        else:
            self._context.out_block_processing(line, line_num)

class IN_BLOCK(BlockExtractorState):

    def __init__(self):
        self._depth = 1

    def process_line(self, line, line_num) -> None:

        block_status = self.block_detector(line)
        if(block_status == BLOCK_END):
            self._depth = self._depth - 1
            if(self._depth == 0):
                sp_line = line.split("}")
                self._context.in_block_processing(sp_line[0], line_num)
                self._context.block_end_cb(line_num)
                self._context.out_block_processing(sp_line[1] , line_num)
                self.context.transition_to(OUTSIDE_BLOCK())
        else:
            self._context.in_block_processing(line, line_num)
            if(block_status == BLOCK_BEGIN):
                self._depth = self._depth + 1


class BlockCodeDiscriminator():
    
    def __init__(self):
        self.reset_vals()

    def get_found_rets(self):
        return FunctionParser_FunctDetails(self.rets, self.warnings, [])
    
    def check_return(self, start, end, block):  
        need_extra_brackets = False
        ret_warnings = ""
        pattern = r"return(.*?)\;"
        match = re.split(pattern, block)

        if (" return" in block or ")return" in block or "{return" in block )  and len(match) > 1:
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

            self.rets.append({"begin": start, "end" : end, "need_brackets" : need_extra_brackets, "returned_value" : match[1].strip(), "return_warning" : ret_warnings})
        else:
            pass



    def reset_vals(self):
        self.rets = []
        self.prev_line ="{"
        self.assembled_block = ""
        self.statement_start = 0
        self.statement_end = 0
        self.warnings = []
        self.started = False

    def process_line_in_block(self, line, line_num):

    
        if( ";" in line or "{" in line):
            if self.started == False:
                self.started = True
                self.statement_start = line_num

            self.started = False
            self.statement_end = line_num
            self.assembled_block = self.assembled_block + " " + line
            if( "return " in self.assembled_block) or ("return(" in self.assembled_block) or("return;" in self.assembled_block):
                self.check_return(self.statement_start, self.statement_end, self.assembled_block)

            self.assembled_block = " "
        else:
            if self.started == False:
                self.started = True
                self.statement_start = line_num
            self.assembled_block = self.assembled_block + " " + line
                    

if __name__ == "__main__":

    cntx = BlockExtractor(print)

    cntx.process_line("void count()", 0)
    cntx.process_line("{",1)
    cntx.process_line("x++",2)
    cntx.process_line("add()",3)
    cntx.process_line("x--",4)
    cntx.process_line("xx}",5)
    cntx.process_line("void count2(){ }",6)