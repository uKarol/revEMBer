# Filename: cfile_detector.py
# Author: Karol Ujda (uKarol)
# Description: searching functions definitions in selected c file

from enum import Enum
from splitter import *


class CommentStatus(Enum):
    ONE_LINE_COMMENT = 0
    COMMENT_BEGIN = 1
    COMMENT_END = 2
    NOT_COMMENT = 3

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

        curly_bracket_begin = '{'
        curly_bracket_end = '}'
        if curly_bracket_begin in line and curly_bracket_end in line: 
            return BraceStatus.BRACE_OPEN_CLOSE
        elif curly_bracket_begin in line:
            return BraceStatus.BRACE_OPEN
        elif curly_bracket_end in line:    
            return BraceStatus.BRACE_CLOSE
        else:
            return BraceStatus.NO_BRACE 
    
    def next_process(self, line, found_functions : list, line_num):
        splitter_status = self.spt.c_splitter(line, line_num)
        if(splitter_status == SUCCESS):
            found_functions.update({self.spt.get_function_signature() : self.spt.get_function_begin()})

    def process_line(self, line, found_functions, line_num):

        if self.current_state == BracketState.IN_BRACKETS:
            
            if('return' in line):
                self.next_process(line, found_functions, line_num)

            if self.brace_detector(line) == BraceStatus.BRACE_CLOSE:
                self.depth = self.depth - 1
                if self.depth == 0:
                    self.current_state = BracketState.OUT_BRACKETS
                    self.next_process(line, found_functions, line_num)
            elif self.brace_detector(line) == BraceStatus.BRACE_OPEN:
                self.depth = self.depth + 1
            else:
                pass
        
        else:

            if self.brace_detector(line) == BraceStatus.BRACE_OPEN:
                self.next_process(line, found_functions, line_num)
                self.current_state = BracketState.IN_BRACKETS
                self.depth = self.depth + 1
            else:
                self.next_process(line, found_functions, line_num)        



class CommentState(Enum):
    IN_COMMENT = 0
    IN_CODE = 1

class Comment_Extractor:

    current_state: CommentState
    def __init__(self):
        self.current_state = CommentState.IN_CODE
        self.brace_extractor = Bracket_Extractor()

    def multiline_comment_detection(self, line:str):
        comment_begin = '/*'
        comment_end = '*/'

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

    def line_processing(self, line:str, found_functions, line_num): #in comment
        if(self.current_state == CommentState.IN_COMMENT):
            if(self.multiline_comment_detection(line) == CommentStatus.COMMENT_END):
                self.current_state = CommentState.IN_CODE

        else:  # in code
            if(self.multiline_comment_detection(line) == CommentStatus.COMMENT_BEGIN):
                self.current_state = CommentState.IN_COMMENT
            else:
                self.brace_extractor.process_line(line, found_functions, line_num)


class cascaded_function_finder:

    def __init__(self):
        self.found_functions = {}

    def remove_preprocessor_and_comments_empty_lines(self, line:str):

        comment_begin = '/*'
        comment_end = '*/'
        one_line_comment = '//'
        preprocessor_directive_begin = '#'

        stripped_line = line.strip()
        if(stripped_line.startswith(one_line_comment)):
            return True
        elif(stripped_line.startswith(comment_begin) and  stripped_line.endswith(comment_end)):
            return True
        elif(stripped_line.startswith(preprocessor_directive_begin)):
            return True
        elif(stripped_line == ''):
            return True
        else:
            return False


    def search_file(self, cfile):
        extractor = Comment_Extractor()
        line_num = 0
        with open(cfile, 'r') as file:
            for line in file:
                if(self.remove_preprocessor_and_comments_empty_lines(line) == False):
                    extractor.line_processing(line, self.found_functions, line_num)
                line_num = line_num + 1
                
    def get_found_functions(self):
        return self.found_functions


