#include <assert.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>

#include <clikit.h>
#include "siggen.h"

#define N_SLOT			3
#define N_SIGNAL 		5

#define PFX_HELP		1
#define PFX_SHOW		2
#define PFX_NO			4

enum shape {sine, triangle, square};

struct sig {
	unsigned		magic;
#define SIG_MAGIC		0x19ed7550
	unsigned		slot;
	unsigned		sig;
	enum shape		shape;
	double			level;
	double			frequency;
};

struct slot {
	unsigned		magic;
#define SLOT_MAGIC		0xcac7a78e
	unsigned		slot;
	struct sig		sigs[N_SIGNAL];
};

static struct slot		slots[N_SLOT];
static struct clikit *ck;

/**********************************************************************/

/*lint -emacro({779},WRONG) */
/*lint -emacro({506},WRONG) */
#define WRONG(foo)	assert(foo == 0)

/**********************************************************************
 * Reset the configuration to default
 */

static void
reset_to_defaults(void)
{
	unsigned u, v;

	(void)memset(slots, 0, sizeof slots);
	for (u = 0; u < N_SLOT; u++) {
		slots[u].magic = SLOT_MAGIC;
		slots[u].slot = u + 1;
		for(v = 0; v < N_SIGNAL; v++) {
			slots[u].sigs[v].magic = SIG_MAGIC;
			slots[u].sigs[v].slot = u + 1;
			slots[u].sigs[v].sig = v + 1;
		}
		assert (slots[u].magic == SLOT_MAGIC);
	}
}

/**********************************************************************
 * Save configuration to file
 *
 * We create another CLIkit context, define a "puts" method that writes
 * into our file, and ask it to "show slot".
 */

static int
myputs(void *priv, int error, const char *str)
{
	FILE *f = priv;

	assert(error == 0);

	if (str != NULL)
		assert (fputs(str, f) >= 0);
	return (0);
}

/*lint -e{818} */
void
save_config(struct clikit_context *cc, const char *a0)
{
	struct clikit_context *cc2;
	FILE *f;

	// We don't care about prefix situations
	if (a0 == NULL)
		return;

	f = fopen(a0, "w");
	if (f == NULL) {
		(void)CLIkit_Error(cc, -1, "Cannot open file %s: %s",
		    a0, strerror(errno));
		return;
	}

	cc2 = CLIkit_New_Context(ck);
	assert(cc2 != NULL);
	CLIkit_Set_Puts(cc2, myputs, f);
	(void)CLIkit_Printf(cc2, "# Config saved YYMMDD-HHMMSS UTC\n");
	CLIkit_Input(cc2, "show slot\n");
	(void)CLIkit_Printf(cc2, "# End of saved config\n");
	assert(0 == CLIkit_Destroy_Context(cc2));
	assert(0 == fclose(f));
}

/**********************************************************************
 * Load configuration from file
 *
 * Reset config to default, create a CLIkit context and feed the file
 * to it.
 */

/*lint -e{818} */
void
load_config(struct clikit_context *cc, const char *a0)
{
	struct clikit_context *cc2;
	char buf[BUFSIZ];
	FILE *f;

	// We don't care about prefix situations
	if (a0 == NULL)
		return;

	f = fopen(a0, "r");
	if (f == NULL) {
		(void)CLIkit_Error(cc, -1, "Cannot open file %s: %s",
		    a0, strerror(errno));
		return;
	}
	cc2 = CLIkit_New_Context(ck);
	assert(cc2 != NULL);

	reset_to_defaults();
	while (fgets(buf, (int)sizeof buf, f))
		CLIkit_Input(cc2, buf);
	assert(0 == CLIkit_Destroy_Context(cc2));
	assert(0 == fclose(f));
}

/**********************************************************************
 * Not implemented Yet
 */

/*lint -e{818} */
void
do_slot_timeout(struct clikit_context *cc, double a0)
{
	(void)cc;
	(void)a0;
}

/**********************************************************************
 * Set the frequency
 */

/*lint -e{818} */
void
ctl_frequency(struct clikit_context *cc, double a0)
{
	struct sig *sp = CLIkit_Get_Instance(cc);
	unsigned pfx = CLIkit_Get_Prefix(cc);

	assert(sp != NULL);
	assert(sp->magic == SIG_MAGIC);

	if (pfx & PFX_SHOW) {
		if (sp->frequency == 0.)
			return;
		(void)CLIkit_Printf(cc,
		    "slot %u signal %u frequency %g\n",
		    sp->slot, sp->sig, sp->frequency);
	} else if (pfx & PFX_NO) {
		sp->frequency = 0.;
	} else
		sp->frequency = a0;
}

/**********************************************************************
 * Set the shape
 */

/*lint -e{818} */
void
ctl_shape(struct clikit_context *cc, const char *a0)
{
	struct sig *sp = CLIkit_Get_Instance(cc);
	unsigned pfx = CLIkit_Get_Prefix(cc);
	const char *s;

	assert(sp != NULL);
	assert(sp->magic == SIG_MAGIC);

	if (pfx & PFX_SHOW) {
		if (sp->shape == sine)
			return;
		switch (sp->shape) {
		case triangle:	s = "triangle"; break;
		case square:	s = "square"; break;
		case sine:	s = "sine"; break;
		default:	WRONG("sp->shape is illegal");
		}
		(void)CLIkit_Printf(cc, "slot %u signal %u shape %s\n",
		    sp->slot, sp->sig, s);
	} else if (pfx & PFX_NO) {
		sp->shape = sine;
	} else {
		assert(a0 != NULL);
		if (!strcmp(a0, "sine"))
			sp->shape = sine;
		else if (!strcmp(a0, "triangle"))
			sp->shape = triangle;
		else if (!strcmp(a0, "square"))
			sp->shape = square;
		else
			WRONG("CLIkit messed up enum");
	}
}

/**********************************************************************
 * Not implemented Yet
 */

/*lint -e{818} */
void
ctl_level(struct clikit_context *cc, double a0, const char *a1)
{
	(void)cc;
	(void)a0;
	(void)a1;
}

/**********************************************************************
 * Find the pointer to a signal, give a slot instance and the number
 */

/*lint -e{818} */
int
signal_instance(struct clikit_context *cc, unsigned a0, void **ip)
{
	struct slot *sp = CLIkit_Get_Instance(cc);

	assert(sp != NULL);
	assert(sp->magic == SLOT_MAGIC);

	if (a0 == 0 || a0 > N_SIGNAL) {
		(void)CLIkit_Error(cc, -1, "Invalid signal number ([1...%d])\n",
		    N_SIGNAL);
		return (1);
	}
	*ip = &sp->sigs[a0 - 1];
	return (0);
}

/**********************************************************************
 * Find the pointer to a slot, given its number.
 */

/*lint -e{818} */
int
slot_instance(struct clikit_context *cc, unsigned a0, void **ip)
{
	if (a0 == 0 || a0 > N_SLOT) {
		(void)CLIkit_Error(cc, -1, "Invalid slot number ([1...%d])\n",
		    N_SLOT);
		return (1);
	}
	*ip = &slots[a0 - 1];
	return (0);
}

/**********************************************************************
 * Main function
 *
 * Initialize,
 * Execute a couple of hardwired commands,
 * Then Read commands from stdin...
 */

int
main(int argc, const char * const *argv)
{
	char buf[BUFSIZ];
	struct clikit_context *cc;

	(void)argc;
	(void)argv;

	reset_to_defaults();

	ck = CLIkit_New();
	assert(ck != NULL);

	assert(0 == CLIkit_Add_Prefix(ck, "help", PFX_HELP));
	assert(0 == CLIkit_Add_Prefix_Recurse(ck, "show", PFX_SHOW));
	assert(0 == CLIkit_Add_Prefix_Recurse(ck, "no", PFX_NO));
	assert(0 == CLIkit_Add_Tree(ck, clikit_match, NULL));

	cc = CLIkit_New_Context(ck);
	assert(cc != NULL);

	(void)CLIkit_Printf(cc, "Default configuration is:\n");
	CLIkit_Input(cc, "slot 2 signal 3 frequency 1e3\n");
	CLIkit_Input(cc, "slot 3 signal 4 frequency 1e4\n");
	CLIkit_Input(cc, "slot 1 signal 2 frequency 1e2\n");
	CLIkit_Input(cc, "show slot\n");
	(void)CLIkit_Printf(cc, "Ready for commands... (hint: type help)\n");

	while (fgets(buf, (int)sizeof buf, stdin))
		CLIkit_Input(cc, buf);

	return (0);
}
