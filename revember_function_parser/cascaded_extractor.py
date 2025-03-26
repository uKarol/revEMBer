import sys
sys.path.append('..')
import re
from revember_function_parser.code_process import BlockExtractor
from revember_function_parser.comment_extractor import CommentExtractor 
#from revember_function_parser.block_extractor import BlockExtractor, BlockCodeDiscriminator
from revember_function_parser.function_extractor import *
from revember_function_parser.experimantal_preprocessing import *
from revember_function_parser.revember_function_parser_data_classes import *

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

    def __init__(self):
        
        #self.code_disc = BlockCodeDiscriminator() 
        self.fun_extractor = FunctionExtractor()
        self.block_extr = BlockExtractor()
        #block_extr = BlockExtractor(self.fun_extractor.process_line, self.fun_extractor.block_begin, self._function_extracting, self.code_disc.process_line_in_block)
        self.prep = DefineDecoder(self.block_extr.process_line) 
        self.conditional_extractor = ConditionalCompilationDecoder(self.prep.process_line)
        self.comment_extr = CommentExtractor(self.conditional_extractor.process_line)
        self.extractor = CascadedExtractor(self.comment_extr.process_line) 
        self.found_functions = {}

        
    # def _function_extracting(self, line_num):
    #     splitter_status = self.fun_extractor.block_end(line_num)
    #     if(splitter_status == SUCCESS):
            
    #         signature = self.fun_extractor.get_function_signature()
    #         function_data = self.fun_extractor.get_function_begin()
    #         function_details = self.code_disc.get_found_rets()
    #         self.found_functions.update({signature : FUnctionParser_FunctData(function_data.name,
    #                                                                         function_data.parameters,
    #                                                                         function_data.begin,
    #                                                                         function_data.end,
    #                                                                         function_details.returns,
    #                                                                         function_details.warnings,
    #                                                                         function_details.revember_artifacts
    #                                                                         )})
    #         self.code_disc.reset_vals()

    #     else:
    #         self.code_disc.get_found_rets()
    #         self.code_disc.reset_vals()

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
 
        