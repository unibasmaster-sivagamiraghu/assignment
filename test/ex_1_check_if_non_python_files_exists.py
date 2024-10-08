from utils import *

def test_exercise_1_check_if_file_exists():
    directory = str(input())
    assert(has_files_without_extensions(directory))