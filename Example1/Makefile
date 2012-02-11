

calc:	siggen.ck main.c
	python ../CLIkit.py --code
	python ../CLIkit.py --tree siggen.ck
	cc -o siggen -Wall -Werror -I. clikit.c siggen.c main.c

test:	siggen
	./siggen

clean:
	rm -f siggen *.o clikit.[ch] siggen.[ch] _.flint

flexelint:
	if flexelint -I. main.c siggen.c > _.flint ; then \
		echo "FlexeLint is happy" ; \
	else \
		cat _.flint ; \
	fi
	rm -f _.flint

