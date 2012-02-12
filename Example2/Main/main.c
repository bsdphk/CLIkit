#include <assert.h>
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <string.h>

#include <ntpns.h>
#include <cmd_main.h>

struct clikit *main_clikit;

void
module_ctor(clikit_match_f *func)
{
	assert(0 == CLIkit_Add_Tree(main_clikit, func, NULL));
}

void
cmd_exit(struct clikit_context *cc)
{

	(void)cc;
	assert(0 == fclose(stdin));
}

/*lint -e{818} */
void
cmd_load(struct clikit_context *cc, const char *a0)
{
	void *dlp;

	(void)CLIkit_Printf(cc, "LOAD %s\n", a0);

	dlp = dlopen(a0, RTLD_NOW);
	(void)CLIkit_Printf(cc, "LOAD %s = %p (%s)\n\t%s\n",
	    a0, dlp, strerror(errno), dlerror());
	if (dlp == NULL)
		(void)fclose(stdin);
	
}

int
main(int argc, const char * const *argv)
{
	struct clikit_context *cc;
	char buf[BUFSIZ];

	(void)argc;
	(void)argv;

	main_clikit = CLIkit_New();
	assert(main_clikit != NULL);
	assert(0 == CLIkit_Add_Prefix(main_clikit, "help", 1));
	assert(0 == CLIkit_Add_Tree(main_clikit, cfg_main, NULL));

	cc = CLIkit_New_Context(main_clikit);
	assert(cc != NULL);

	(void)CLIkit_Printf(cc, "Hello World\n");
	CLIkit_Input(cc, "help\n");
	CLIkit_Input(cc, "load ../Dummy/ntpns_dummy\n");

	while (fgets(buf, (int)sizeof buf, stdin))
		CLIkit_Input(cc, buf);

	return (0);
}
