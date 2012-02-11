
# Comment1
LEAF foo INT {
	# Comment2
	DESC	"state of foobar"
	FUNC	do_foo			# Comment3
}

LEAF bar REAL ENUM { day year hour minute second } {
	DESC	"percentage of snafu"
	FUNC	do_bar
}

BRANCH {
	NAME	ignition

	LEAF fizzle WORD {
		DESC	"don't fire"
		FUNC	do_fizzle
	}
	LEAF boom WORD {
		DESC	"do fire"
		FUNC	do_boom
	}
}

INSTANCE things UINT {
	DESC	"things of sorts"
	FUNC	things_instance

	IMPORT ignition

	LEAF this UINT {
		DESC "what is this"
		FUNC do_things_this
	}
	LEAF that WORD INT {
		DESC "point to that"
		FUNC do_things_that
	}

	INSTANCE junk WORD UINT {
		DESC "junk"
		FUNC junk_instance

		LEAF whatchamacallit REAL {
			DESC "thingmajics"
			FUNC pitch_it
		}
	}
}
