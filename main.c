#include <assert.h>
#include <stdio.h>

#include "clikit.h"

#define P_SHOW		(1<<1)

int
main(int argc, char **argv)
{
	struct clikit *ck;
	struct clikit_context *cc;

	(void)argc;
	(void)argv;

	ck = CLIkit_New();
	assert(ck != NULL);

	assert(0 == CLIkit_Add_Prefix(ck, "show", P_SHOW));

	cc = CLIkit_New_Context(ck);
	assert(cc != NULL);


	assert(0 == CLIkit_Destroy_Context(cc));
	assert(0 == CLIkit_Del_Prefix(ck, "show"));
	assert(0 == CLIkit_Destroy(ck));

	return (0);
}
