

all:
	python CLIkit.py --code
	python CLIkit.py --tree test.ck
	cc -g -c -Wall -Werror clikit.c
	cc -g -c -Wall -Werror main.c
	cc -g -o a.out main.o clikit.o
	./a.out
	flexelint -I. clikit.c main.c
