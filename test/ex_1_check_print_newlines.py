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






def test_exercise_1_add_newlinetocode():
    global code
    code_to_add = """
a = 33
b = 44
display_results(a,b)

a = 3
b = 7
display_results(a,b)

"""
    code += code_to_add
    print(code)

    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        exec(code, globals())

    captured_output = f.getvalue()    
    print(captured_output)
    output = False
    if "33.00^2 + 44.00^2 = 55.00^2" in captured_output:
        if "3.00^2 + 7.00^2 = 7.62^2" in captured_output:
            output=True
    elif "33.00^2+44.00^2=55.00^2" in captured_output:
        if "3.00^2+7.00^2=7.62^2" in captured_output:
            output=True
            
    print(output)
    assert(output)


if __name__ == '__main__':
    test_exercise_1_add_newlinetocode()