#include <assert.h>
#include <stdio.h>

#include "clikit.h"
#include "test.h"

#define P_HELP		1
#define P_SHOW		(1<<1)
#define P_CONF		(1<<2)

/*lint -esym(534, printf)*/

void
do_foo(struct clikit_context *cc, int a0)
{
	(void)cc;
	printf("%s(pfx=%x, a0=%d)\n", __func__, CLIkit_Get_Prefix(cc), a0);
	(void)CLIkit_Error(cc, 7, "<%g>\n", 3.141592);
	(void)CLIkit_Printf(cc, "<%g>\n", 3.141592);
	(void)CLIkit_Puts(cc, "The end\n");
}

void
do_bar(struct clikit_context *cc, double a0)
{
	(void)cc;
	printf("%s(%g)\n", __func__, a0);
}

void
do_things_this(struct clikit_context *cc, unsigned a0)
{
	(void)cc;
	(void)a0;
	printf("%s(%u)\n", __func__, a0);
}

void
do_things_that(struct clikit_context *cc, const char *a0, int a1)
{
	(void)cc;
	(void)a0;
	(void)a1;
	printf("%s(%s, %d)\n", __func__, a0, a1);
}

void
pitch_it(struct clikit_context *cc, double a0)
{
	(void)cc;
	(void)a0;
	printf("%s(%g)\n", __func__, a0);
}

int
junk_instance(struct clikit_context *cc, const char *id, unsigned id2)
{
	(void)cc;
	(void)id;
	printf("%s(%s, %u)\n", __func__, id, id2);
	return (0);
}

int
things_instance(struct clikit_context *cc, unsigned id)
{
	(void)cc;
	(void)id;
	printf("%s(pfx=%x, %u)\n", __func__, CLIkit_Get_Prefix(cc), id);
	return (0);
}

int
main(int argc, char **argv)
{
	struct clikit *ck;
	struct clikit_context *cc;

	(void)argc;
	(void)argv;

	ck = CLIkit_New();
	assert(ck != NULL);

	assert(0 == CLIkit_Add_Prefix_Recurse(ck, "help", P_HELP));
	assert(0 == CLIkit_Add_Prefix(ck, "show", P_SHOW));
	assert(0 == CLIkit_Add_Prefix_Recurse(ck, "conf", P_CONF));

	assert(0 == CLIkit_Add_Tree(ck, clikit_match, NULL));
	assert(0 == CLIkit_Add_Tree(ck, match_foo, "snafu"));

	cc = CLIkit_New_Context(ck);
	assert(cc != NULL);

	CLIkit_Set_Puts(cc, NULL, NULL);

	if (argc > 1) {
		char buf[BUFSIZ];

		printf("Ready for interactive commands...\n");
		while (fgets(buf, (int)sizeof buf, stdin))
			CLIkit_Input(cc, buf);
	} else {
		CLIkit_Input(cc, "\n\n# Comment\nfoo\nthings 0 this 3\n");
		CLIkit_Input(cc, "\nthings 1 that \"foobar\" -3\n");
		CLIkit_Input(cc, "\nbar 3.1415\n");
	}

	assert(0 == CLIkit_Del_Tree(ck, clikit_match, NULL));
	assert(0 == CLIkit_Del_Tree(ck, match_foo, "snafu"));
	assert(0 == CLIkit_Destroy_Context(cc));
	assert(0 == CLIkit_Del_Prefix(ck, "show"));
	assert(0 == CLIkit_Destroy(ck));

	return (0);
}
