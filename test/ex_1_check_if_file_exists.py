from utils import *


def test_exercise_1_check_if_file_exists():
    file_name = str(input())
    assert(check_if_file_exists(file_name))