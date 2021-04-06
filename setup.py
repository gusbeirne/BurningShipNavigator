import cx_Freeze

import cx_Freeze

executables = [cx_Freeze.Executable("BurningShipNavigator.py")]

cx_Freeze.setup(
    name="Burning Ship Navigator",
    options={"build_exe": {"packages": ["pygame", "math", "collections"]}},
    executables=executables

    )
