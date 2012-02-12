
SHLIB_NAME	?= ntpns_${MOD}

cmd_${MOD}.c cmd_${MOD}.h: cmd_${MOD}.ck
	pwd ; ${CLIKIT} --tree ${.CURDIR}/cmd_${MOD}.ck
	ls -l 
SRCS		+= cmd_${MOD}.c
CLEANFILES	+= cmd_${MOD}.[ch]

INCL		=	-I. -I${.CURDIR} -I${.CURDIR}/..
CFLAGS		+=	${INCL}

.include <bsd.lib.mk>
