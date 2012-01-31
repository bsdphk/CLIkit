#include <assert.h>
#include <stdio.h>

#include "clikit.h"
#include "test.h"

#define P_SHOW		(1<<1)


void
do_foo(struct clikit_context *cc)
{
	(void)cc;
	printf("%s()\n", __func__);
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
	printf("%s()\n", __func__);
}

void
do_things_that(struct clikit_context *cc, const char *a0, int a1)
{
	(void)cc;
	(void)a0;
	(void)a1;
	printf("%s()\n", __func__);
}

void
pitch_it(struct clikit_context *cc, double a0)
{
	(void)cc;
	(void)a0;
	printf("%s()\n", __func__);
}

int
junk_instance(struct clikit_context *cc, const char *id)
{
	(void)cc;
	(void)id;
	printf("%s()\n", __func__);
	return (0);
}

int
things_instance(struct clikit_context *cc, unsigned id)
{
	(void)cc;
	(void)id;
	printf("%s()\n", __func__);
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

	assert(0 == CLIkit_Add_Prefix(ck, "show", P_SHOW));

	assert(0 == CLIkit_Add_Tree(ck, clikit_match, NULL));
	assert(0 == CLIkit_Add_Tree(ck, match_foo, NULL));

	cc = CLIkit_New_Context(ck);
	assert(cc != NULL);

	if (argc > 1) {
		char buf[BUFSIZ];
		while (fgets(buf, sizeof buf, stdin))
			CLIkit_Input(cc, buf);
	} else {
		CLIkit_Input(cc, "\n\n# Comment\nfoo\nthings 0 this 3\n");
		CLIkit_Input(cc, "\nthings 1 that \"foobar\" -3\n");
		CLIkit_Input(cc, "\nbar 3.1415\n");
	}

	assert(0 == CLIkit_Del_Tree(ck, clikit_match, NULL));
	assert(0 == CLIkit_Del_Tree(ck, match_foo, NULL));
	assert(0 == CLIkit_Destroy_Context(cc));
	assert(0 == CLIkit_Del_Prefix(ck, "show"));
	assert(0 == CLIkit_Destroy(ck));

	return (0);
}
