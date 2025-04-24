# Filename: experimental_preprocessing.py
# Author: Karol Ujda (uKarol)
# Description: Checking preprocessor directives

from abc import ABC, abstractmethod

class CondState(ABC):

    def on_if(self, line, line_num):
        self._context.push_to_stack(self)
        self._context.next_state(IfProcessing())

    def on_if_0(self, line, line_num):
        self._context.push_to_stack(self)
        self._context.next_state(If_0_Processing())

    def on_elif(self, line, line_num):
        pass

    def on_endif(self, line, line_num):
        try:
            next_state = self._context.get_from_stack()
        except IndexError:
            next_state = UnconditionalProcessing()
        self._context.next_state(next_state)
        
    def on_else(self, line, line_num):
        print("NOT IMPLEMENTED!!!!!")

    def no_prep(self, line, line_num):
        self.context.next_stage_processing(line, line_num)

    @property
    def context(self):
        return self._context
    
    @context.setter
    def context(self, context):
        self._context = context

    def check_braces(self, line, line_num):
        if(self.b_open > self.b_close):
            for i in range(0, (self.b_open - self.b_close)):
                self.context.next_stage_processing("}", line_num)
                
    def count_braces(self, line, line_num):
        if "{" in line:
            self.b_open = self.b_open + 1
        if "}" in line:
            self.b_close = self.b_close + 1

class UnconditionalProcessing(CondState):

    def __init__(self):
        pass

    def on_if(self, line, line_num):
        self.context.next_state(IfProcessing())


class ElseProcessing(CondState):

    def __init__(self):
        pass

class If_0_Processing(CondState):

    def __init__(self):
        pass

    def on_if(self, line, line_num):
        pass

    def on_if_0(self, line, line_num):
        pass

    def on_elif(self, line, line_num):
        pass
   
    def on_else(self, line, line_num):
        pass

    def no_prep(self, line, line_num):
        pass

class ElifProcessing(CondState):

    def __init__(self):
        self.b_open = 0
        self.b_close = 0

    def no_prep(self, line, line_num):
        self.count_braces(line, line_num)
        self.context.next_stage_processing(line, line_num)

    def on_elif(self, line, line_num):
        self.check_braces(line, line_num)
        self.context.next_state(ElifProcessing())


    def on_else(self, line, line_num):
        self.check_braces(line, line_num)
        self.context.next_state(ElseProcessing())

class IfProcessing(CondState):

    def __init__(self):
        self.b_open = 0
        self.b_close = 0

    def no_prep(self, line, line_num):
        self.count_braces(line, line_num)
        self.context.next_stage_processing(line, line_num)

    def on_elif(self, line, line_num):
        self.check_braces(line, line_num)
        self.context.next_state(ElifProcessing())

    def on_else(self, line, line_num):
        self.check_braces(line, line_num)
        self.context.next_state(ElseProcessing())
    

class ConditionalCompilationDecoder:

    def __init__(self, next_stage_processing):
        self.next_state(UnconditionalProcessing())
        self.next_stage_processing = next_stage_processing
        self.stack = []

    def push_to_stack(self, data):
        self.stack.append(data)

    def get_from_stack(self):
        return self.stack.pop()

    def next_state(self, state):
        self.current_state = state
        self.current_state.context = self 
        self.directives = {"#if": self.current_state.on_if,
                           "#else": self.current_state.on_else, 
                           "#endif": self.current_state.on_endif, 
                           "#elif": self.current_state.on_elif,
                           "#ifdef": self.current_state.on_if,
                           "#ifndef": self.current_state.on_if}        

    def process_line(self, line, line_num):
        self.current_state.no_prep(line, line_num)
        
    def process_directive(self, directive: str, statement: str, line_num: int):

            try: 
                if directive == "#if":
                    if statement == "0":
                        self.current_state.on_if_0(statement, line_num)
                    else:
                        self.current_state.on_if(statement, line_num)
                else:    
                    meth = self.directives[directive]
                    meth(statement, line_num)

            except KeyError:
                pass #unhandled directive
