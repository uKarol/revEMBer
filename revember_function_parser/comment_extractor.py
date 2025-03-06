from __future__ import annotations
from abc import ABC, abstractmethod

COMMENT_BEGIN_CODE_IN_LINE = 0  # code /* commented code
COMMENT_BEGIN = 1               # /* commented code
COMMENT_END = 2                 # comented code */
COMMENT_END_CODE_IN_LINE = 3    # comented code */ code
COMMENT_NOT_DETECTED = 4

#signle line comments removed at previous stage 

class CommentExtractorState(ABC):

    def comment_detector(self, text:str):
        multiline_comment_begin = '/*'
        multiline_comment_end = '*/'
        text_to_check = text.strip()
        if multiline_comment_begin in text_to_check:
            if text_to_check.startswith(multiline_comment_begin):
                return COMMENT_BEGIN
            else:
                return COMMENT_BEGIN_CODE_IN_LINE
        elif multiline_comment_end in text_to_check:
            if text_to_check.startswith(multiline_comment_begin):
                return COMMENT_END
            else:
                return COMMENT_END_CODE_IN_LINE
        else:
            return COMMENT_NOT_DETECTED

    @property
    def context(self) -> CommentExtractor:
        return self._context
    
    @context.setter
    def context(self, context: CommentExtractor):
        self._context = context

    @abstractmethod
    def process_line(self, line, line_num) -> None:
        pass

class CommentExtractor:

    _state = None

    def __init__(self, next_stage_processing):
        self.transition_to(IN_CODE())
        self.next_stage_processing = next_stage_processing

    def transition_to(self, state : CommentExtractorState):
        self._state = state
        self._state.context = self

    def process_line(self, line, line_num):
        self._state.process_line(line, line_num)

class IN_COMMENT(CommentExtractorState):

    def process_line(self, line, line_num) -> None:
        if(self.comment_detector(line) == COMMENT_END):
            self.context.transition_to(IN_CODE())
        if(self.comment_detector(line) == COMMENT_END_CODE_IN_LINE):
            self.context.transition_to(IN_CODE())
            self._context.next_stage_processing(line.split('*/')[1], line_num)

class IN_CODE(CommentExtractorState):

    def process_line(self, line, line_num) -> None:
        comment_status = self.comment_detector(line)
        if(comment_status == COMMENT_BEGIN):
            self.context.transition_to(IN_COMMENT())
        elif(comment_status == COMMENT_BEGIN_CODE_IN_LINE):
            self._context.next_stage_processing(line.split('/*')[0], line_num)
            self.context.transition_to(IN_COMMENT())
        else:
            self._context.next_stage_processing(line, line_num)


if __name__ == "__main__":

    cntx = CommentExtractor(print)

    cntx.process_line("void count()",0)
    cntx.process_line("{",1)
    cntx.process_line("/*x++",2)
    cntx.process_line("add()",3)
    cntx.process_line("*/x--",4)
    cntx.process_line("xx}",5)
    cntx.process_line("void count2(){/* }",6)
    cntx.process_line("domment",7)
    cntx.process_line("*/ z++",8)
    cntx.process_line("z++}",9)