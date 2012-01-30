

all:
	python CLIkit.py --code
	cat test.ck
	python CLIkit.py --tree test.ck
	@echo "-------------------------------"
	sed 1,27d test.h
	@echo "-------------------------------"
	sed 1,27d test.c
	@echo "-------------------------------"
	cc -g -c -Wall -Werror clikit.c
	cc -g -c -Wall -Werror main.c
	cc -g -c -Wall -Werror test.c
	cc -g -o a.out main.o clikit.o test.o
	./a.out
	flexelint -I. clikit.c main.c test.c

clean:
	rm -f clikit.[ch]
	rm -f test.[ch]
	rm -f *.o
	rm -f a.out
