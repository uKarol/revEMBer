import sys
sys.path.append('..')
import re
from revember_function_parser.code_process import BlockExtractor
from revember_function_parser.comment_extractor import CommentExtractor 
from revember_function_parser.experimantal_preprocessing import *
from revember_function_parser.revember_function_parser_data_classes import *
from revember_function_parser.keyword_analyzer import KeywordAnalyzer
from revember_function_parser.multiline_directive_processing import DirectiveDecoder
class CascadedExtractor:

    def __init__(self, next_stage_processing):
        self.next_stage_processing = next_stage_processing

    def remove_single_block_comments(self,line, line_num):
        extracted = re.sub('/(.+?)\*/', '', line)
        if(len(extracted) > 0):
            self.next_stage_processing(extracted, line_num)

    def remove_single_line_comments(self,line:str, line_num):
        splitted = line.split("//")[0]
        if(len(splitted) > 0):
            self.next_stage_processing(splitted, line_num)


    def process_line(self, line, line_num):
        line_to_process = line.strip()
        
        if("//" in line_to_process):
            self.remove_single_line_comments(line_to_process, line_num)

        elif ("/*" in line_to_process) and ("*/" in line_to_process):
            self.remove_single_block_comments(line_to_process, line_num)

        elif len(line_to_process) > 0:
            self.next_stage_processing(line_to_process, line_num)


class FunctionDetector:

    def __init__(self, keywords_to_be_found, warnings):
        self.keyword_analyzer = KeywordAnalyzer(keywords_to_be_found)
        self.block_extr = BlockExtractor(self.keyword_analyzer)
        self.conditional_extractor = ConditionalCompilationDecoder(self.block_extr.process_line)
        self.prep = DirectiveDecoder(self.conditional_extractor) 
        self.comment_extr = CommentExtractor(self.prep.process_line)
        self.extractor = CascadedExtractor(self.comment_extr.process_line) 
        self.found_functions = {}

        

    def get_found_functions(self):
        return self.found_functions

    def clear_results(self):
        self.found_functions = {}

    def search_file(self, cfile):
        line_num = 0
        with open(cfile, 'r') as file:
            for line in file:
                self.extractor.process_line(line, line_num)
                line_num = line_num+1
        self.found_functions = self.block_extr.get_found_functions()



if __name__ == "__main__":
    out_file = open("result.json", "w")
    
    detector = FunctionDetector()
    detector.search_file("testing/testing_files/stm32g4xx_hal_uart.c")
    f_dict = detector.get_found_functions()
    for function in f_dict:
        print(f_dict[function])

    detector.clear_results()
    print("________NEXT FILE _________________")
    detector.search_file("testing/testing_files/stm32g4xx_hal_dma.c")
    f_dict = detector.get_found_functions()
    for function in f_dict:
        print(f_dict[function])
 
        