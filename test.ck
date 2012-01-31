
# Comment1
LEAF foo INT {
	# Comment2
	desc	"FOO is not bar"
	func	do_foo			# Comment3
	name	match_foo
}

LEAF bar REAL {
	desc	"BAR is not foo"
	func	do_bar
}

INSTANCE things UINT {
	desc	"THINGS"
	func	things_instance

	LEAF this UINT {
		desc "things this"
		func do_things_this
	}
	LEAF that WORD INT {
		desc "things that"
		func do_things_that
	}

	INSTANCE junk WORD {
		desc "junk"
		func junk_instance

		LEAF whatchamacallit REAL {
			desc "thingmajic"
			func pitch_it
		}
	}
}
