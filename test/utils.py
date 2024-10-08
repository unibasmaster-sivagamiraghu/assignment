import numpy as np
import git
import openai as ai
import os


########################################################################
#### Exercise 2.1 ######################################################
########################################################################


def check_if_file_exists(file_name):
    try:
        with open(file_name, "r") as f:
            print(file_name+" exists")
            return(True)
    except:
        print(file_name+" does not exist")
        return(False)
    



def has_files_without_extensions(directory, extensions=('.py', '.ipynb')):
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)) and not filename.endswith(extensions):
            return True
    return False











########################################################################
#### Exercise 2.2 ######################################################
########################################################################




# Define the symbol to number mapping
symbol_to_number = {
    '*': 0,
    '|': 1,
    '/': 2,
    '\\': 3
}

true_graph = """
*
|\\
|*
*|
|\\\\
|*|
*||
|||*
|||*
|||/
||/|
|*|
|*|
|//
*/
|/
*
*
*
*
"""



def get_git_structure(repo_path="."):
    repo = git.Repo(repo_path)
    
    # Checkout to main branch
    repo.heads.main.checkout()

    # Generate the log graph structure
    log_graph = repo.git.log('--graph', '--oneline', '--all').splitlines()

    # Process each line and keep only the desired characters
    processed_lines = [''.join(char for char in line if char in ['*', '/', '|', '\\']) for line in log_graph]

    return "\n".join(processed_lines)


def transform_pattern_to_matrix(pattern_str):
    # Split the pattern string into lines
    content_lines = pattern_str.strip().split('\n')

    # Determine the number of rows and columns
    num_rows = len(content_lines)
    num_cols = max(len(line) for line in content_lines)
    
    # Initialize the matrix with placeholder "-1" as strings
    matrix_str = np.full((num_rows, num_cols), "-1", dtype=object)
    
    # Populate the matrix with symbols from the pattern
    for i, line in enumerate(content_lines):
        for j, symbol in enumerate(line):
            matrix_str[i][j] = symbol
    
    # Convert the matrix using the mapping, ensuring any missing symbols return -1
    matrix_num = np.vectorize(lambda x: symbol_to_number.get(x, -1))(matrix_str)
    
    return matrix_num



def similarity(true_pattern, test_pattern):

    total_score = np.sum(true_pattern >= 0)



    # check if test_pattern is at least the shape of true_pattern, otherwise add -2 padding
    if test_pattern.shape[0] < true_pattern.shape[0]:
        test_pattern = np.pad(test_pattern, ((0, true_pattern.shape[0]-test_pattern.shape[0]), (0, 0)), 'constant', constant_values=-2)
    if test_pattern.shape[1] < true_pattern.shape[1]:
        test_pattern = np.pad(test_pattern, ((0, 0), (0, true_pattern.shape[1]-test_pattern.shape[1])), 'constant', constant_values=-2)

    score = 0
    for i in range(test_pattern.shape[0]-true_pattern.shape[0]+1):
        for j in range(test_pattern.shape[1]-true_pattern.shape[1]+1):
            # check if true_pattern is in test pattern, and ignore -1 and -2 values
            _score = np.sum(true_pattern == test_pattern[i:i+true_pattern.shape[0], j:j+true_pattern.shape[1]])

            # count all the -1 score

            remove = np.sum((true_pattern == -1 )*(test_pattern[i:i+true_pattern.shape[0], j:j+true_pattern.shape[1]]==-1))

            _score = _score - remove
            if _score > score:
                score = _score


    return round(score/total_score*10)


def evaluate_similarity():
    test_graph = get_git_structure()
    matrix1 = transform_pattern_to_matrix(true_graph)
    matrix2 = transform_pattern_to_matrix(test_graph)
    results = similarity(matrix1, matrix2)
    print(matrix2)
    print("Exercise 2.2 you got "+str(results)+"/10 Points")
    return results


########################################################################
#### Exercise 2.3 ######################################################
########################################################################



ai.api_key =  '' 

task = """ You are a reviewer and have to give up to 5 Points for the follwing task:
Use only the commands from the terminal for the following tasks:

"Look at the documentation of github Readme.md and create a Readme.md file in your GitHub repository. Write a
step-by-step explanation of the commands you use to solve the following problem:
Task Use only the commands from the terminal for the following tasks:
(i) create a folder called exercise2.3 in your GitHub repository and enter it.
(ii) create a folder called data
(iii) create a folder called tmp
(iv) add the logfile.log into the folder data
(v) add the data.txt file into the data folder
(vi) copy the data.txt file into the tmp folder
(vii) move the logfile.log into the tmp folder
(viii) copy the folder data into the tmp folder and name it tmp_data"

The Student will hand it in as a Readme.md. 
So you have to check if the commands are correct and if the folder structure is correct. 
In addition, Please check, if the formating is nice

You should be a very strick reviewer and give only 5 points if everything is correct.

Output: a single integer number betqween 0 and 5
"""




def evaluate_readme_chatgpt():
    ## load Readme.md file as a string
    with open("README.md", "r") as f:
        student = f.read()
    
    
    
    
    response = ai.ChatCompletion.create(
    model="gpt-4",
    messages=[{
        "role": "system",
        "content": task},{
        "role": "user",
        "content": student
        }],

    temperature=0,
    max_tokens=1
    )

    text = response['choices'][0]['message']['content']
    print("Exercise 2.3 you got "+str(text)+"/5 Points")
    return (int(text))


def evaluate_readme():
    ## load Readme.md file as a string
    with open("README.md", "r") as f:
        student = f.read()

    points = 0
    if 'mkdir' in student:
        points += 0.5
    if 'cp -r' in student:
        points += 0.5
    if 'mv' in student:
        points += 0.5
    
    if check_if_file_exists('exercise2_3/data/data.txt'):
        if check_if_file_exists('exercise2_3/tmp/data.txt'):
            points += 0.5
    if check_if_file_exists('exercise2_3/tmp/logfile.log'):
        if not check_if_file_exists('exercise2_3/data/logfile.log'):
            points += 0.5
    if check_if_file_exists('exercise2_3/tmp/tmp_data/data.txt'):
        points += 0.5

     # Common Markdown symbols for formatting
    symbols = ["#", "*", "_", "![", "[](", "```", ">"]

    for symbol in symbols:
        if symbol in student:
            points += 0.5

    points = int(min(points, 5))

    print("Exercise 2.3 you got "+str(points)+"/5 Points")
    return points

def check_sha256():
    ## load Readme.md file as a string
    with open("README.md", "r") as f:
        student = f.read()
    sha256 = "ef78cd4c515dbca06b10d9d3bc3ecabaf5f10ac0f466242a1f96d396b0570eef"
    if sha256 in student:
        print("Exercise 2.4 you got 1/1 Point")
        return True
    else:
        print("Exercise 2.4 you got 0/1 Point")
        return False

if __name__ == '__main__':

   print("--------------------")
   evaluate_similarity()
   print("--------------------")
   evaluate_readme()
   print("--------------------")
   check_sha256()
   print("--------------------")
