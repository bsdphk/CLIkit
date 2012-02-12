
#include "clikit.h"

void module_ctor(clikit_match_f *);

extern struct clikit *main_clikit;

#define MODULE(nm, init)					\
	/*lint -esym(528, mod_##nm##_ctor)*/			\
	static void __attribute__((constructor))		\
	mod_##nm##_ctor(void)					\
	{							\
		module_ctor(clikit_match);			\
		init;						\
	}
