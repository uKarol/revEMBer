import filecmp
import os



def get_files():

    test_dir = "test_outputs/"
    expected_results_dir = "expected_results/"
    expected = os.listdir(os.getcwd() + "\\expected_results")

    for file in expected:
        to_test = test_dir + file
        result = expected_results_dir + file
        print(f"FILE: {to_test} EXPECTED RESULT {result} VERDICT {filecmp.cmp(to_test, result)}")

get_files()