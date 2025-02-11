from enum import Enum

from splitter import *

comment_begin = '/*'
comment_end = '*/'
one_line_comment = '//'

curly_bracket_begin = '{'
curly_bracket_end = '}'

parenthesis_open =  '('
parenthesis_close = ')'

statement_ending = ';'


# class PatternDetector(Enum):

#     ONE_LINE_FUNCTION = 0 # NAME ARGS BODY IN SINGLE LINE - symbols ( ) and { }
#     NAME_AND_ARGS_IN_THE_SAME_LINE = 1  # symbols () and {
#     NAME_AND_ARGS_IN_THE_SAME_LINE = 2 # symbols ()
    


class StatementState(Enum):
    BEGIN = 0,
    GETTING_NAME = 1,
    GETTING_ARGS = 2,
    BODY_START = 3,

    

class CommentStatus(Enum):
    ONE_LINE_COMMENT = 0
    COMMENT_BEGIN = 1
    COMMENT_END = 2
    NOT_COMMENT = 3


def multiline_comment_detection(line:str):
    if( comment_begin in line and comment_end in line ):
        if( line.rstrip().startswith(comment_begin) ):
            return CommentStatus.ONE_LINE_COMMENT
        else:
            return CommentStatus.NOT_COMMENT
    elif(comment_begin in line):
        return CommentStatus.COMMENT_BEGIN
    elif(comment_end in line):
        return CommentStatus.COMMENT_END
    else:
        return CommentStatus.NOT_COMMENT
    

class BracketState(Enum):
    IN_BRACKETS = 0
    OUT_BRACKETS = 1

class BraceStatus(Enum):
    BRACE_OPEN = 0
    BRACE_CLOSE = 1
    BRACE_OPEN_CLOSE = 2
    NO_BRACE = 3

class Bracket_Extractor:
    current_state: BracketState
    depth: int

    def __init__(self):
        self.current_state = BracketState.OUT_BRACKETS
        self.depth = 0
        self.spt = cascased_split()

    def brace_detector(self, line):
        if curly_bracket_begin in line and curly_bracket_end in line: 
            return BraceStatus.BRACE_OPEN_CLOSE
        elif curly_bracket_begin in line:
            return BraceStatus.BRACE_OPEN
        elif curly_bracket_end in line:    
            return BraceStatus.BRACE_CLOSE
        else:
            return BraceStatus.NO_BRACE 
    
    def next_process(self, line):
        if(self.spt.c_splitter(line) == SUCCESS):
            print(self.spt.get_function_signature())
            print("")

    def process_line(self, line):

        if self.current_state == BracketState.IN_BRACKETS:

            if self.brace_detector(line) == BraceStatus.BRACE_CLOSE:
                self.depth = self.depth - 1
                if self.depth == 0:
                    self.current_state = BracketState.OUT_BRACKETS
                    self.next_process(line)
            elif self.brace_detector(line) == BraceStatus.BRACE_OPEN:
                self.depth = self.depth + 1
            else:
                pass
        
        else:

            if self.brace_detector(line) == BraceStatus.BRACE_OPEN:
                self.next_process(line)
                self.current_state = BracketState.IN_BRACKETS
                self.depth = self.depth + 1
            else:
                self.next_process(line)        



class CommentState(Enum):
    IN_COMMENT = 0
    IN_CODE = 1

class Comment_Extractor:

    current_state: CommentState


    def __init__(self):
        self.current_state = CommentState.IN_CODE
        self.brace_extractor = Bracket_Extractor()

    def comment_processing(self, line:str): #in comment
        if(self.current_state == CommentState.IN_COMMENT):
            if(multiline_comment_detection(line) == CommentStatus.COMMENT_END):
                self.current_state = CommentState.IN_CODE

        else:  # in code
            if(multiline_comment_detection(line) == CommentStatus.COMMENT_BEGIN):
                self.current_state = CommentState.IN_COMMENT
            else:
                #print(line)
                self.brace_extractor.process_line(line)



def remove_preprocessor_and_comments_empty_lines(line:str):
    stripped_line = line.strip()
    if(stripped_line.startswith(one_line_comment)):
        return True
    elif(stripped_line.startswith(comment_begin) and  stripped_line.endswith(comment_end)):
        #print(" COMMENTED OUT LINE " + stripped_line)
        return True
    elif(stripped_line.startswith('#')):
        return True
    elif(stripped_line == ''):
        return True
    else:
        return False


def tests(cfile):
    extractor = Comment_Extractor()
    with open(cfile, 'r') as file:
        for line in file:
            if(remove_preprocessor_and_comments_empty_lines(line) == False):
                extractor.comment_processing(line)


#tests("stm32g4xx_nucleo.c")
#tests("stm32g4xx_hal_dma.c")
tests("stm32g4xx_hal_cortex.c")
#tests("main.cpp")