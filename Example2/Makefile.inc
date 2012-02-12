
WARNS		?= 6
NO_MAN		?= sorry
INCL		= -I. -I.. -I${.CURDIR} -I${.CURDIR}/..
CFLAGS		+= ${INCL}

CLIKIT		= python ${.CURDIR}/../../CLIkit.py

flexelint: ${SRCS:M*.c}
	@if flexelint ${INCL} ${.ALLSRC} > _.flint ; then \
		echo "FlexeLint is happy" ; \
	else \
		cat _.flint ; \
	fi
	@rm -f _.flint

x:
	cd ${.CURDIR} && make cleandir
	cd ${.CURDIR} && make cleandir
	cd ${.CURDIR} && make obj
	cd ${.CURDIR} && make depend
	cd ${.CURDIR} && make
	ls -l
	cd ${.CURDIR} && make cleandir
	cd ${.CURDIR} && make cleandir
	cd ${.CURDIR} && make depend
	cd ${.CURDIR} && make
	ls -l
