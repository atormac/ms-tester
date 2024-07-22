import subprocess
import os
import shutil

cmd = ['./minishell']
bash = ['bash']

COUNTER = 1
OK = 0
KO = 0

def strip_prefix(s, p):
   return s.replace(p,'') if s.startswith(p) else s

def get_ms_output(s):
    output = ""
    output = '\n'.join(line for line in s.splitlines() if '@minishell:' not in line)
    return output

def run_bash(input_str):
    b = subprocess.Popen(["bash"], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = b.communicate(input_str.encode())
    bash_exitcode = b.returncode
    bash_stdout = stdout.decode().rstrip()
    bash_stderr = strip_prefix(stderr.decode(), "bash: line 1: ")
    bash_stderr = strip_prefix(bash_stderr, "bash: ")
    return bash_stdout, bash_stderr, bash_exitcode

def run_minishell(input_str):
    b = subprocess.Popen(["./minishell"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = b.communicate(input_str.encode())
    ms_exitcode = b.returncode
    ms_stdout = get_ms_output(stdout.decode())
    ms_stderr = strip_prefix(stderr.decode(), "minishell: ")
    return ms_stdout, ms_stderr, ms_exitcode

def do_test(input_str):
    global COUNTER

    error = 0
    bash_stdout, bash_stderr, bash_exitcode = run_bash(input_str)
    ms_stdout, ms_stderr, ms_exitcode = run_minishell(input_str)
    if (bash_stdout != ms_stdout):
        error = 1
        print("STDOUT:")
        print("bash: " + bash_stdout)
        print("ms: " + ms_stdout)
    if (bash_stderr != ms_stderr):
        error = 1
        print("STDERR:")
        print("bash: " + bash_stderr)
        print("ms: " + ms_stderr)
    if (bash_exitcode != ms_exitcode):
        error = 1
        print("EXITCODE: bash: " + str(bash_exitcode) + "ms: " + str(ms_exitcode))
    if (error == 1):
        print("ERROR [" + str(COUNTER) + "]: " + repr(input_str))
    else:
        print("OK [" + str(COUNTER) + "]: " + repr(input_str))
    COUNTER += 1

def init_tester():
    global COUNTER
    COUNTER = 1
    shutil.copyfile("../minishell", "./minishell")

def run_tests():
    try:
        f = open('./tests.txt', 'r')
        lines = f.readlines()
        for line in lines:
            do_test(line)
        f.close()
    except Exception as e:
        print("Error occured: ", e)

init_tester()
run_tests()
