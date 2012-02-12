
PROG		= NTPns

SRCS		= main.c

clikit.c clikit.h:
	${CLIKIT} --code
	mv clikit.h ..

SRCS		+= clikit.c
CLEANFILES	+= clikit.c ../clikit.h


cmd_main.c cmd_main.h:	cmd_main.ck
	${CLIKIT} --tree ${.CURDIR}/cmd_main.ck

SRCS		+= cmd_main.c
CLEANFILES	+= cmd_main.[ch]

CFLAGS		+=	-export-dynamic

.include <bsd.prog.mk>

test:	${PROG}
	./${PROG}
