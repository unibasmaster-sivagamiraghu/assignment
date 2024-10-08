import os
import sys
import subprocess
import io
import contextlib


# Get the current script's directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Compute the path to the parent directory and add it to sys.path
parent_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir)

with open('exercise2_1/pythagorean.py', 'r') as file:
    code = file.read()

def test_exercise_1_check_if_correct_print_exists():
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        exec(code, globals())
    captured_output = f.getvalue()    
    print(captured_output)
    if "33^2 + 44^2 = 55^2" in captured_output:
        assert(True)
    elif "33^2+44^2=55^2" in captured_output:
        assert(True)
    else:
        assert(False)




if __name__ == '__main__':
    test_exercise_1_check_if_correct_print_exists()

    