from abc import ABC, abstractmethod

class DefineState:

    def __init__(self, context):
        self.context = context

    def process_line(self, line, line_num):
        pass 

class DefineDecoder:

    def __init__(self, next_stage_processing):
        self.current_state = NoDefineProcessing(self)
        self.next_stage_processing = next_stage_processing

    def next_state(self, state):
        self.current_state = state

    def process_line(self, line, line_num):
        self.current_state.process_line(line, line_num)

class NoDefineProcessing(DefineState):
    def __init__(self, context):
        super().__init__(context)

    def process_line(self, line, line_num):
        if line.startswith("#define"):
            if line.endswith("\\"):
                self.context.next_state(DefineMultilineProcessing(self.context))
        elif line.startswith("#"):
            pass
        else:
            self.context.next_stage_processing(line, line_num)


class DefineMultilineProcessing(DefineState):

    def __init__(self, context):
        super().__init__(context)

    def process_line(self, line, line_num):
        if line.endswith("\\"):
            pass
        else:
            self.context.next_state(NoDefineProcessing(self.context))




class CondState(ABC):

    def on_if(self, line, line_num):
        self._context.push_to_stack(self)
        self._context.next_state(IfProcessing())


    def on_elif(self, line, line_num):
        pass

    def on_endif(self, line, line_num):
        try:
            next_state = self._context.get_from_stack()
        except IndexError:
            next_state = UnconditionalProcessing()
        self._context.next_state(next_state)
        

    @property
    def context(self):
        return self._context
    
    @context.setter
    def context(self, context):
        self._context = context

    def no_prep(self, line, line_num):
        self.context.next_stage_processing(line, line_num)

    def on_else(self, line, line_num):
        print("NOT IMPLEMENTED!!!!!")

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

    def on_endif(self, line, line_num):
        super().on_endif(line, line_num)

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

    def on_endif(self, line, line_num):
        super().on_endif(line, line_num)

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
        directive : str
        if(line.startswith("#")):
            try: 
                directive = line.split()[0]
                meth = self.directives[directive]
                meth(line, line_num)

            except KeyError:
                self.current_state.no_prep(line, line_num)
        else:
            self.current_state.no_prep(line, line_num)
        