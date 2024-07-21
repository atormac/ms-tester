cp ../minishell .
chmod 755 minishell
MS=./minishell

PROMPT=$(echo -e "\nexit\n" | $MS | head -n 1 | sed "s/\x1B\[[0-9;]\{1,\}[A-Za-z]//g" )
PROMPT_NOENV=$(echo -e "\nexit\n" | env -i $MS | head -n 1 | sed "s/\x1B\[[0-9;]\{1,\}[A-Za-z]//g" )
BASH_PROMPT=$(echo -e "\nexit\n" | $MS | head -n 1 | sed "s/\x1B\[[0-9;]\{1,\}[A-Za-z]//g" )

INPUT="lsasdasd\nexit"

BASH_OUT=$(echo -e "$INPUT" | bash 2>./bash_error 1>./bash_out)
BASH_EXIT=$?
echo $BASH_EXIT

MS_OUT=$(echo -e $INPUT | $MS 2>/dev/null | grep -vF "$PROMPT" | grep -vF "$PROMPT_NOENV" 1>./ms_out)
MS_ERR=$(echo -e $INPUT | $MS 2>./ms_error)
MS_EXIT=$?
echo $MS_EXIT

diff ./bash_out ./ms_out
#exec_test 'echo abc 123'
