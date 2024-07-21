cp ../minishell .
chmod 755 minishell


TD=./tmp
MS=./minishell

PROMPT=$(echo -e "\nexit\n" | $MS | head -n 1 | sed "s/\x1B\[[0-9;]\{1,\}[A-Za-z]//g" )
PROMPT_NOENV=$(echo -e "\nexit\n" | env -i $MS | head -n 1 | sed "s/\x1B\[[0-9;]\{1,\}[A-Za-z]//g" )
BASH_PROMPT=$(echo -e "\nexit\n" | $MS | head -n 1 | sed "s/\x1B\[[0-9;]\{1,\}[A-Za-z]//g" )

#INPUT="ls\necho \$?\nexit"
mkdir ./tmp
rm ./tmp/*

TOTAL=0
OK=0
KO=0

function do_test {
	echo -e "${1}"
	INPUT="${1}\necho \$?\nexit"
	BASH_OUT=$(echo -e "$INPUT" | bash 2>/dev/null 1>$TD/bash_out)
	BASH_ERR=$(trap "" PIPE && echo -e "$INPUT" | bash 2>&1 > /dev/null | awk -F: '{print $NF}'> $TD/bash_error)

	MS_OUT=$(echo -e $INPUT | $MS 2>/dev/null | grep -vF "$PROMPT" | grep -vF "$PROMPT_NOENV" 1> $TD/ms_out)
	MS_ERR=$(echo -e $INPUT | $MS 2>&1 > /dev/null | awk -F: '{print $NF}' > $TD/ms_error)

	if ! diff --brief $TD/bash_out $TD/ms_out; then
		((KO++))
		echo "STDOUT KO: $INPUT"
	fi
	if ! diff --brief $TD/bash_error $TD/ms_error; then
		((KO++))
		echo "STDERR KO: $INPUT"
	fi
	((TOTAL++))
}

while IFS='' read -r LINE
do
	do_test "$LINE"
done < "tests.txt"

OK="$((TOTAL-KO))"
printf "OK: $OK, KO: $KO, TOTAL: $TOTAL"
