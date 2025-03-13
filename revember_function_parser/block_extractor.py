from __future__ import annotations
from abc import ABC, abstractmethod
import re

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
        #self.next_stage_processing = next_stage_processing
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
            self._context.out_block_processing(sp_line[0]+"{", line_num)
            self._context.block_begin_cb()
            self._context.in_block_processing(sp_line[1], line_num)
            self.context.transition_to(IN_BLOCK())
        elif(self.block_detector(line) == SIGNLE_LINE_BLOCK):
            strs = re.split(r'[{}]', line)
            self._context.out_block_processing(strs[0]+"{", line_num)
            self._context.block_begin_cb()
            self._context.in_block_processing(strs[1], line_num)
            self._context.block_end_cb()
            self._context.out_block_processing("}" + strs[2], line_num)
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
                self._context.block_end_cb()
                self._context.out_block_processing('}' + sp_line[1] , line_num)
                self.context.transition_to(OUTSIDE_BLOCK())
        else:
            self._context.in_block_processing(line, line_num)
            if(block_status == BLOCK_BEGIN):
                self._depth = self._depth + 1


class BlockCodeDiscriminator():
    
    def __init__(self):
        self.rets = []

    def get_found_rets(self):
        ret_val = self.rets
        self.rets = []
        return ret_val

    def process_line_in_block(self, line, line_num):

        if(line.startswith("return ") or line.startswith("return(") or line.startswith("return;") or " return;" in line or
           " return " in line or " return(" in line ) and line.endswith(";"):
            self.rets.append(line_num)



if __name__ == "__main__":

    cntx = BlockExtractor(print)

    cntx.process_line("void count()", 0)
    cntx.process_line("{",1)
    cntx.process_line("x++",2)
    cntx.process_line("add()",3)
    cntx.process_line("x--",4)
    cntx.process_line("xx}",5)
    cntx.process_line("void count2(){ }",6)