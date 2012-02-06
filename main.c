#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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

struct thing {
	unsigned	id;
	unsigned	this;
	char		*that_0;
	int		that_1;
};

/*lint -e{818} */
void
do_things_this(struct clikit_context *cc, unsigned a0)
{
	struct thing *tp;
	unsigned pfx;

	tp = CLIkit_Get_Instance(cc);
	pfx = CLIkit_Get_Prefix(cc);

	if (pfx == P_CONF) {
		(void)CLIkit_Printf(cc, "things %u this %u\n",
		    tp->id, tp->this);
	} else {
		tp->this = a0;
	}
}

void
do_things_that(struct clikit_context *cc, const char *a0, int a1)
{
	struct thing *tp;
	unsigned pfx;

	tp = CLIkit_Get_Instance(cc);
	pfx = CLIkit_Get_Prefix(cc);
	if (pfx == P_CONF) {
		if (tp->that_0 != NULL) 
			(void)CLIkit_Printf(cc, "things %u that \"%s\" %d\n",
			    tp->id, tp->that_0, tp->that_1);
	} else {
		printf("%s(%s, %d)\n", __func__, a0, a1);
		if (tp->that_0 != NULL)
			free(tp->that_0);
		tp->that_0 = strdup(a0);
		assert(tp->that_0);
		tp->that_1 = a1;
	}
}

void
pitch_it(struct clikit_context *cc, double a0)
{
	struct thing *tp;
	unsigned pfx;
	(void)cc;
	(void)a0;
	printf("%s(%g)\n", __func__, a0);
	tp = CLIkit_Get_Instance(cc);
	pfx = CLIkit_Get_Prefix(cc);
	printf("In %p pfx=%x\n", tp, pfx);

}

int
junk_instance(struct clikit_context *cc, const char *id, unsigned id2, void **ip)
{
	(void)cc;
	(void)ip;
	printf("%s(%s, %u)\n", __func__, id, id2);
	return (0);
}

int
things_instance(struct clikit_context *cc, unsigned id, void **ip)
{
	struct thing *tp;

	printf("%s(pfx=%x, %u)\n", __func__, CLIkit_Get_Prefix(cc), id);
	tp = calloc(1L, sizeof *tp);
	assert(tp);
	tp->id = id;
	*ip = tp;
	return (0);
}

static void
docmd(struct clikit_context *cc, const char *s)
{
	printf(">>> %s\n", s);
	CLIkit_Input(cc, s);
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

	assert(0 == CLIkit_Add_Prefix(ck, "help", P_HELP));
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
			docmd(cc, buf);
	} else {
		docmd(cc, "\n\n# Comment\nfoo\nthings 0 this 3\n");
		docmd(cc, "\nthings 1 that \"foobar\" -3\n");
		docmd(cc, "\nshow things\n");
		docmd(cc, "\nconf\n");
		docmd(cc, "\nconf things\n");
		docmd(cc, "\nbar 3.1415\n");
	}

	assert(0 == CLIkit_Del_Tree(ck, clikit_match, NULL));
	assert(0 == CLIkit_Del_Tree(ck, match_foo, "snafu"));
	assert(0 == CLIkit_Destroy_Context(cc));
	assert(0 == CLIkit_Del_Prefix(ck, "show"));
	assert(0 == CLIkit_Destroy(ck));

	return (0);
}
