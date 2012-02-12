#include <stdio.h>

#include "ntpns.h"
#include "cmd_dummy.h"

/*lint -e{818}*/
void
cmd_dummy(struct clikit_context *cc)
{
	(void)CLIkit_Printf(cc, "Dummy!\n");
}

static void
init(void)
{
	(void)printf("Dummy in da house\n");
}

MODULE(dummy, init())
