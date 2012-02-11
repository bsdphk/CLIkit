#include <assert.h>
#include <stdio.h>

#include <clikit.h>
#include "calc.h"

#define STACK_DEPTH	5

static double stack[STACK_DEPTH];

static void
show_stack(const struct clikit_context *cc)
{
	int i;

	for (i = STACK_DEPTH - 1; i >= 0; i--)
		if (CLIkit_Printf(cc, "%.3lf\n", stack[i]))
			return;
}

/*lint -e{818} */
void
do_enter(struct clikit_context *cc, double a0)
{
	int i;

	for (i = STACK_DEPTH - 1; i > 0; i--)
		stack[i] = stack[i - 1L];
	stack[0] = a0;
	show_stack(cc);
}

/*lint -e{818} */
void
do_add(struct clikit_context *cc)
{
	int i;

	stack[0] += stack[1];
	for (i = 1; i < STACK_DEPTH - 1; i++)
		stack[i] = stack[i + 1L];
	show_stack(cc);
}

/*lint -e{818} */
void
do_mul(struct clikit_context *cc)
{
	int i;

	stack[0] *= stack[1];
	for (i = 1; i < STACK_DEPTH - 1; i++)
		stack[i] = stack[i + 1L];
	show_stack(cc);
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
	show_stack(cc);

	while (fgets(buf, (int)sizeof buf, stdin))
		CLIkit_Input(cc, buf);
	
	return (0);
}

