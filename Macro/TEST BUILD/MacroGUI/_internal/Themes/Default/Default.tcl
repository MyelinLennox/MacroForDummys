source [file join [file dirname [info script]] theme breeze.tcl]
source [file join [file dirname [info script]] theme equilux.tcl]

proc set_theme {mode} {
	if {$mode == "dark"} {
		ttk::style theme use "equilux"

	} elseif {$mode == "light"} {
		ttk::style theme use "breeze"

	}
}
