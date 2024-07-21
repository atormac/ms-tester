cp ../minishell .
chmod 755 minishell
MS=./minishell

PROMPT=$(echo -e "\nexit\n" | $MS | head -n 1 | sed "s/\x1B\[[0-9;]\{1,\}[A-Za-z]//g" )
PROMPT_NOENV=$(echo -e "\nexit\n" | env -i $MS | head -n 1 | sed "s/\x1B\[[0-9;]\{1,\}[A-Za-z]//g" )
BASH_PROMPT=$(echo -e "\nexit\n" | $MS | head -n 1 | sed "s/\x1B\[[0-9;]\{1,\}[A-Za-z]//g" )

INPUT="lsasdasd\nexit"

BASH_OUT=$(echo -e "$INPUT" | bash 2>./bash_error 1>./bash_out)
BASH_EXIT=$?
echo $BASH_OUT
echo $BASH_EXIT

MS_OUT=$(echo -e $INPUT | $MS 2>./ms_error | grep -vF "$PROMPT" | grep -vF "$PROMPT_NOENV" 1>./ms_out)
MS_EXIT=$?
echo $MS_OUT
echo $MS_EXIT

#exec_test 'echo abc 123'
