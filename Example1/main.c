#include <assert.h>
#include <stdio.h>

#include <clikit.h>
#include "siggen.h"


void
save_config(struct clikit_context *cc, int a0)
{
}
void
load_config(struct clikit_context *cc, double a0)
{
}
void
do_slot_timeout(struct clikit_context *cc, double a0)
{
}
void
ctl_frequency(struct clikit_context *cc, double a0)
{
}
void
ctl_shape(struct clikit_context *cc, const char *a0)
{
}
void
ctl_level(struct clikit_context *cc, double a0, const char *a1)
{
}
int
signal_instance(struct clikit_context *cc, unsigned a0, void **ip)
{
	return (0);
}
int
slot_instance(struct clikit_context *cc, unsigned a0, void **ip)
{
	return (0);
}

int
main(int argc, const char * const *argv)
{
	char buf[BUFSIZ];
	struct clikit *ck;
	struct clikit_context *cc;

	(void)argc;
	(void)argv;

	ck = CLIkit_New();
	assert(ck != NULL);

	assert(0 == CLIkit_Add_Prefix(ck, "help", 1));
	assert(0 == CLIkit_Add_Tree(ck, clikit_match, NULL));

	cc = CLIkit_New_Context(ck);
	assert(cc != NULL);

	(void)CLIkit_Printf(cc, "Hello World\n");

	while (fgets(buf, (int)sizeof buf, stdin))
		CLIkit_Input(cc, buf);
	
	return (0);
}

