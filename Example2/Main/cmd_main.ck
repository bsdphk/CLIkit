BRANCH {
	NAME	cfg_main

	LEAF exit {
		FUNC	cmd_exit
	}

	LEAF quit {
		FUNC	cmd_exit
	}

	LEAF logout {
		FUNC	cmd_exit
	}

	LEAF load STRING {
		FUNC	cmd_load
	}
}
