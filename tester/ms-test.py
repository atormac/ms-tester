import subprocess
import os
import shutil
import sys
import filecmp

global ms_prompt
ms_prompt = "empty"
COUNTER = 0
VALGRIND = 0
OK = 0
KO = 0

valgrind_cmd = ["valgrind", "--tool=memcheck", "--leak-check=yes",
"--trace-children=yes", "--trace-children-skip=/usr/bin/*,/bin/*",
"--track-fds=yes", "-q", "./minishell"]

def strip_prefix(s, p):
   return s.replace(p,'') if s.startswith(p) else s

def get_ms_output(s):
    global ms_prompt
    lines = s.splitlines()
    filtered = [line for line in lines if not line.startswith(ms_prompt)]
    return '\n'.join(filtered)

def run_bash(input_str):
    try:
        b = subprocess.Popen(["bash"], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = b.communicate(input_str.encode(), timeout=5)
        bash_exitcode = b.returncode
        bash_stdout = stdout.decode().rstrip()
        bash_stderr = strip_prefix(stderr.decode(), "bash: line 1: ")
        bash_stderr = strip_prefix(bash_stderr, "bash: ")
        bash_stderr = bash_stderr.partition('\n')[0]
    except Exception as e:
        print("Error occured: ", e)
    return bash_stdout, bash_stderr, bash_exitcode

def run_minishell(input_str):
    try:
        if (VALGRIND == 1):
            cmd = valgrind_cmd
            timeout_seconds = 30
        else:
            cmd = ["./minishell"]
            timeout_seconds = 5
        b = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = b.communicate(input_str.encode(), timeout=timeout_seconds)
        ms_exitcode = b.returncode
        ms_stdout = get_ms_output(stdout.decode())
        ms_stderr = strip_prefix(stderr.decode(), "minishell: ")
        ms_stderr = ms_stderr.partition('\n')[0]
    except Exception as e:
        print("Error occured: ", e)
    return ms_stdout, ms_stderr, ms_exitcode

def print_error_info(type_str, bash_str, ms_str):
    print("--- " + type_str + " ---")
    print("BASH: " + bash_str)
    print("MINISHELL: " + ms_str)
    print("------------------------")

def do_test(input_str):
    global COUNTER
    global OK
    global KO

    error = 0
    error_outfile = 0
    dir = './outfiles'
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

    bash_stdout, bash_stderr, bash_exitcode = run_bash(input_str)
    if (os.path.exists(dir + "/outfile")):
        os.rename(dir + "/outfile", dir + "/bash_out")
    ms_stdout, ms_stderr, ms_exitcode = run_minishell(input_str)
    if (bash_stdout != ms_stdout or bash_stderr != ms_stderr or bash_exitcode != ms_exitcode):
        error = 1
    if (os.path.exists(dir + "/bash_out")):
        if not (filecmp.cmp(dir + "/bash_out", dir + "/outfile", shallow=False)):
            error = 1
            error_outfile = 1
    if (error == 1):
        KO += 1
        print("ERROR [" + str(COUNTER) + "]: " + repr(input_str))
        if (bash_stdout != ms_stdout):
            print_error_info("STDOUT", bash_stdout, ms_stdout);
        if (bash_stderr != ms_stderr):
            print_error_info("STDERR", bash_stderr, ms_stderr);
        if (bash_exitcode != ms_exitcode):
            print_error_info("EXITCODE", str(bash_exitcode), str(ms_exitcode));
        if (error_outfile == 1):
            print("OUTFILE")
    else:
        OK += 1
        print("OK [" + str(COUNTER) + "]: " + repr(input_str))
    COUNTER += 1

def init_tester():
    global COUNTER
    global VALGRIND
    shutil.copyfile("../minishell", "./minishell")
    os.chmod("./minishell", 0o0755)
    if not os.path.exists("./infiles/noaccess"):
        shutil.copyfile("./infiles/f1", "./infiles/noaccess")
        os.chmod("./infiles/noaccess", 0o0000)
    if (len(sys.argv) == 2 and sys.argv[1] == "valgrind"):
        VALGRIND = 1
        print("VALGRIND ENABLED")
        print(*valgrind_cmd)

def get_prompt():
    stdout, stderr, ret = run_minishell("exit\n")
    return stdout.split(':')[0] + ":"

def run_tests():
    try:
        f = open('./tests.txt', 'r')
        lines = f.readlines()
        for line in lines:
            do_test(line)
        f.close()
        print("\n--- SUMMARY ---")
        print("TOTAL:\t" + str(COUNTER) + "\tOK:\t" + str(OK) + "\tERROR:\t" + str(KO))
    except Exception as e:
        print("Error occured: ", e)

init_tester()
ms_prompt = get_prompt()
run_tests()
