        LEAF save_config INT {
                # Comment2
                DESC    "Save configuration to permanent storage"
                FUNC    save_config             # Comment3
        }

        LEAF load_config REAL {
                DESC    "Load configuration from permanent storage"
                FUNC    load_config
        }

        INSTANCE slot UINT {
                DESC    "Per slot configuration"
                FUNC    slot_instance

                LEAF timeout REAL {
                        DESC "Timeout in seconds"
                        FUNC do_slot_timeout
                }

                INSTANCE signal UINT {
                        DESC "Per signal configuration"
                        FUNC signal_instance

                        LEAF frequency REAL {
                                DESC "Frequency in Hz"
                                FUNC ctl_frequency
                        }
                        LEAF shape ENUM { triangle ramp square sine } {
                                DESC "Curve shape"
                                FUNC ctl_shape
                        }
                        LEAF level REAL ENUM { Vpp Vrms dBm } {
                                DESC "Signal Level"
                                FUNC ctl_level
                        }
                }
        }

