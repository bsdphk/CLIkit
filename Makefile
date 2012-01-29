

all:
	python CLIkit.py --code
	cc -c -Wall -Werror clikit.c
	flexelint -I. clikit.c
