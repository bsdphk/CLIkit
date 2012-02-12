
C_ENUM foo {
	foo = L_FOO = 0x34
	bar = 24
	barf = L_BARF
	foobar = SNAFU
	snafu = FOOBAR = 1
}

INSTANCE meta foo {
	FUNC metafunc

	LEAF exclaim {
		FUNC exclaim
	}
}
	
