

all:
	python CLIkit.py --code
	cc -g -c -Wall -Werror clikit.c
	cc -g -c -Wall -Werror main.c
	cc -g -o a.out main.o clikit.o
	./a.out
	flexelint -I. clikit.c main.c
