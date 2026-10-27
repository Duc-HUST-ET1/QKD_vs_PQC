"""Shared pytest setup."""

import matplotlib

# Tests only write image files. Selecting Agg before pyplot is imported avoids intermittent
# Tk/Tcl failures ("invalid command name tcl_findLibrary") seen with the default TkAgg backend.
matplotlib.use("Agg")
