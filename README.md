Python curses wheels for Windows
================================

This repository has the source code for the Python curses wheels provided by
Christoph Gohlke, set up for easy rebuilding.

Unless you want to build the wheels yourself, it will be easier to get them
from https://www.lfd.uci.edu/~gohlke/pythonlibs/#curses.

Background
----------

The `curses` module is in the Python standard library, but is not available on
Windows. Trying to import `curses` gives an import error for `_curses`, which
is provided by `Modules/_cursesmodule.c` in the CPython source code.

The wheels provided here are based on patches from
https://bugs.python.org/issue2889, which make minor modifications to
`_cursesmodule.c` to make it compatible with Windows and the
[PDCurses](https://pdcurses.sourceforge.io) curses implementation.  `setup.py`
defines `HAVE_*` macros for features available in PDCurses and makes some minor
additional compatibility tweaks.

The patched `_cursesmodule.c` is linked against PDCurses to produce a wheel
that provides the `_curses` module on Windows and allows the standard `curses`
module to run.

Unicode support
---------------

The wheels are built with wide character support and force the encoding to
UTF-8. Remove `UTF8=y` from the `nmake` line in `build_wheels.bat` to use the
default system encoding instead.

Build instructions
------------------

 1. Clone the repository with the following command:

        git clone --recurse-submodules https://github.com/ulfalizer/windows-curses-wheels.git

    `--recurse-submodules` pulls in the required PDCurses Git submodule.

 2. Install compilers compatible with the Python versions that you want to
    build wheels for by following the instructions at
    https://wiki.python.org/moin/WindowsCompilers.

 3. Install Python 3.3 or later to get
    [the Python launcher for Windows](https://docs.python.org/3/using/windows.html#launcher).

 4. Install any other Python versions you want to build wheels for.

    Only the Python X.Y versions that have pyxy\ directories are supported.

 5. Install the `wheel` package for all Python versions. Taking Python 3.4
    as an example, the following command will do it:

        py -3.4 -m pip install wheel

    `py` is the Python launcher, which makes it easy to run a particular Python
    version.

 6. Run `build-wheels.bat` in the Visual Studio
    [Developer Command Prompt](https://docs.microsoft.com/en-us/dotnet/framework/tools/developer-command-prompt-for-vs),
    passing it the Python versions you want to build wheels for. For example,
    the following command will builds wheels for the Python 3.4 and the 32-bit
    version of Python 3.6:

        build_wheels.bat 3.4 3.6-32

    `build-wheels.bat` first builds PDCurses, and then builds and links the
    source code in pyXY\ for each of the specified Python version, producing
    wheels as output. The wheels are stored in dist\.

Compatibility note
------------------

This building scheme above should be the safest one to use. In practice, many
of the resulting wheels seem to be forwards- and backwards-compatible.
