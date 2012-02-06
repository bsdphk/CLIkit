
CC=	gcc

all:
	python CLIkit.py --code
	@echo "-------------------------------"
	python CLIkit.py --tree test.ck
	@echo "-------------------------------"
	${CC} -g -c -Wall -Werror clikit.c
	${CC} -g -c -Wall -Werror main.c
	${CC} -g -c -Wall -Werror test.c
	${CC} -g -o a.out main.o clikit.o test.o
	./a.out
	if flexelint -I. clikit.c main.c test.c > _.flint ; then \
		echo "FlexeLint is happy" ; \
	else \
		cat _.flint ; \
	fi

clean:
	rm -f clikit.[ch]
	rm -f test.[ch]
	rm -f *.o
	rm -f a.out
