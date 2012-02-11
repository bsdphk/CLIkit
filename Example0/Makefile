

calc:	calc.ck main.c
	python ../CLIkit.py --code
	python ../CLIkit.py --tree calc.ck
	cc -o calc -Wall -Werror -I. clikit.c calc.c main.c

test:	calc
	./calc

clean:
	rm -f calc *.o clikit.[ch] calc.[ch] _.flint

flexelint:
	if flexelint -I. main.c calc.c > _.flint ; then \
		echo "FlexeLint is happy" ; \
	else \
		cat _.flint ; \
	fi
	rm -f _.flint

