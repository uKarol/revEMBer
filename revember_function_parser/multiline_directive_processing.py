# Filename: experimental_preprocessing.py
# Author: Karol Ujda (uKarol)
# Description: Checking preprocessor directives

from abc import ABC, abstractmethod
from typing import Protocol

class NextStagePreprocessing(Protocol):

    def process_line(self, line: str, line_num: int):
        ...
    
    def process_directive(self, directive: str, statement: str, line_num: int):
        ...


#abstract state class 
class DirectiveState(ABC):

    def __init__(self, context):
        self.context = context

    def process_line(self, line: str, line_num: int):
        self.context.next_stage.process_line(line, line_num)

    def process_directive(self, line: str, line_num: int):
        pass

#context class
class DirectiveDecoder:

    def __init__(self, next_stage : NextStagePreprocessing):
        self.current_state = SimpleDirectiveProcessing(self)
        self.next_stage = next_stage
        self.last_directive = ""

    def next_state(self, state):
        self.current_state = state

    def process_line(self, line, line_num):
        if line.startswith("#"):
            self.current_state.process_directive(line, line_num)
        else:
            self.current_state.process_line(line, line_num)

class SimpleDirectiveProcessing(DirectiveState):
    def __init__(self, context):
        super().__init__(context)

    def process_directive(self, line: str, line_num: int):
        if line.endswith("\\"):
            self.context.last_directive = line
            self.context.next_state(MultilineDirectiveProcessing(self.context))
        else:
            (directive, statement) = line.split(maxsplit=1)
            self.context.next_stage.process_directive(directive, statement, line_num)


class MultilineDirectiveProcessing(DirectiveState):

    def __init__(self, context):
        super().__init__(context)

    def process_line(self, line: str, line_num: int):
        self.context.last_directive = self.context.last_directive + line
        if line.endswith("\\"):
            pass
        else:
            (directive, statement) = self.context.last_directive.split(maxsplit=1)
            self.context.last_directive = ""
            self.context.next_stage.process_directive(directive, statement, line_num)
            self.context.next_state(SimpleDirectiveProcessing(self.context))


if __name__ == "__main__":

    class test_next_stage:
        def process_line(self, line: str, line_num: int):
            print(f"line: {line}")
    
        def process_directive(self, directive: str, statement: str, line_num: int):
            print(f"directive: {directive} statement: {statement}")

    
    test_decoder = DirectiveDecoder(test_next_stage())

    test_decoder.process_line("#define DUPA 0", 0)
    test_decoder.process_line("int DUPA 0", 0)
    test_decoder.process_line("#define DUPA_MACRO \\", 0)
    test_decoder.process_line("int DUPA 0\\", 1)
    test_decoder.process_line("int DUPA++", 1)