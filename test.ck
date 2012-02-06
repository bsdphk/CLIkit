
# Comment1
LEAF foo INT {
	# Comment2
	desc	"state of foobar"
	func	do_foo			# Comment3
	name	match_foo
}

LEAF bar REAL {
	desc	"percentage of snafu"
	func	do_bar
}

INSTANCE things UINT {
	desc	"things of sorts"
	func	things_instance

	LEAF this UINT {
		desc "what is this"
		func do_things_this
	}
	LEAF that WORD INT {
		desc "point to that"
		func do_things_that
	}

	INSTANCE junk WORD UINT {
		desc "junk"
		func junk_instance

		LEAF whatchamacallit REAL {
			desc "thingmajics"
			func pitch_it
		}
	}
}
