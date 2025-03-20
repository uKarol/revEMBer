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

    detector = FunctionDetector()
    basic_files = "\\testing\\testing_files\\"
    results_dir = '\\testing\\tests_output\\'
    expected_dir = '\\testing\\expected_results\\'
    test_files = os.listdir(os.getcwd()+basic_files)

    for file in test_files:
        detector.search_file(os.getcwd()+basic_files+file)
        f_dict = detector.get_found_functions()
        result_file_name = os.getcwd()+results_dir+file+".json"
        out_file = open(result_file_name, "r+")
        out_file.truncate(0)
        out_file.close()
        out_file = open(result_file_name, "a")
        for function in f_dict:
            json.dump( dataclasses.asdict(f_dict[function]), out_file, indent=6)
        out_file.close()
        expected_file_name = os.getcwd()+expected_dir+file+".json"
        print(f'file {file} verdict: {filecmp.cmp(result_file_name, expected_file_name)}')
        detector.clear_results()