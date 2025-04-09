import sys
import os
# setting path
sys.path.append('..')

from cascaded_extractor import *
import dataclasses 
import json
import os
import filecmp

if __name__ == "__main__":

    
    basic_files = "\\testing\\testing_files\\"
    results_dir = '\\testing\\tests_output\\'
    expected_dir = '\\testing\\expected_results\\'
    test_files = os.listdir(os.getcwd()+basic_files)

    for file in test_files:
        to_be_added = {"inc" :  '#include "revEMBer.h"',
                            "begin" : 'REVEMBER_FUNCTION_ENTRY()',
                            "ret" : 'REVEMBER_FUNCTION_EXIT()',
                            "end" : 'REVEMBER_FUNCTION_EXIT()',
                            "warning" :'#warning "improper return statement - add revember macros manually"'
        } 
        detector = FunctionDetector(list(to_be_added.values()))
        detector.search_file(os.getcwd()+basic_files+file)
        f_dict = detector.get_found_functions()
        detector.clear_results()
        result_file_name = os.getcwd()+results_dir+file+".json"
        #print(f_dict)
        out_file = open(result_file_name, "w+")
        out_file.truncate(0)
        out_file.close()
        out_file = open(result_file_name, "a")
        for function in f_dict:
            json.dump( dataclasses.asdict(f_dict[function]), out_file, indent=6)
        out_file.close()
        expected_file_name = os.getcwd()+expected_dir+file+".json"
        try:
            print(f'file {file} verdict: {filecmp.cmp(result_file_name, expected_file_name)}')
        except FileNotFoundError: 
            print(f'file {file} not found')
        