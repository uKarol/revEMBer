from __future__ import annotations
from abc import ABC, abstractmethod

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

    def __init__(self, next_stage_processing):
        self.transition_to(OUTSIDE_BLOCK())
        self.next_stage_processing = next_stage_processing

    def transition_to(self, state : BlockExtractorState):
        self._state = state
        self._state.context = self

    def process_line(self, line, line_num):
        self._state.process_line(line, line_num)



class OUTSIDE_BLOCK(BlockExtractorState):

    def process_line(self, line, line_num) -> None:
        self._context.next_stage_processing(line, line_num)
        if(self.block_detector(line) == BLOCK_BEGIN):
            self.context.transition_to(IN_BLOCK())


class IN_BLOCK(BlockExtractorState):

    def __init__(self):
        self._depth = 1

    def process_line(self, line, line_num) -> None:
        if("return" in line): 
            self._context.next_stage_processing(line, line_num)
        block_status = self.block_detector(line)
        if(block_status == BLOCK_BEGIN):
            self._depth = self._depth + 1
        elif(block_status == BLOCK_END):
            self._depth = self._depth - 1
            if(self._depth == 0):
                self._context.next_stage_processing(line, line_num)
                self.context.transition_to(OUTSIDE_BLOCK())


if __name__ == "__main__":

    cntx = BlockExtractor(print)

    cntx.process_line("void count()", 0)
    cntx.process_line("{",1)
    cntx.process_line("x++",2)
    cntx.process_line("add()",3)
    cntx.process_line("x--",4)
    cntx.process_line("xx}",5)
    cntx.process_line("void count2(){ }",6)