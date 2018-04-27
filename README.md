Python curses wheels for Windows
================================

This repository has the source code for the Python curses wheels provided by
Christoph Gohlke, set up for easy rebuilding. Only `build-wheels.bat` is
original work.

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
    builds wheel for by following the instructions at
    https://wiki.python.org/moin/WindowsCompilers.

 3. Install Python 3.3 or later to get
    the [Python launcher for Windows](https://docs.python.org/3/using/windows.html#launcher).

 4. Install any other Python versions you want to build wheels for.

    Only the Python X.Y versions that have `pyXY\` directories are supported.

 5. Install the `wheel` package for all Python versions. Taking Python 3.4
    as an example, the following command will do it:

        py -3.4 -m pip install wheel

    `py` is the Python launcher, which makes it easy to run a particular Python
    version.

 6. Open the Visual Studio
    [Developer Command Prompt](https://docs.microsoft.com/en-us/dotnet/framework/tools/developer-command-prompt-for-vs)
    of the compiler required by the version of Python that you want to build
    a wheel for.

    Use the 32-bit version (e.g. `VS2015 x86 Native Tools Command Prompt`) to build wheels for 32-bit
    Python versions, and the 64-bit version (e.g.
    `VS2015 x64 Native Tools Command Prompt`) to build wheels for 64-bit Python versions.

 7. Run `build-wheels.bat`, passing it the Python version you're building a
    wheel for. For example, the following command will build a wheel for
    Python 3.5:

        build_wheels.bat 3.5

    If you have both 32-bit and 64-bit versions of the same Python version
    installed and are building a 32-bit wheel, add "-32" to the version
    number, like in the following example:

        build_wheels.bat 3.5-32

    If you are building multiple wheels for Python versions that are all
    compatible with the same compiler, you can list all of them in the same
    command:

        build_wheels.bat 3.5 3.6

    `build-wheels.bat` first cleans and rebuilds PDCurses, and then builds and
    links the source code in `pyXY\` for each of the specified Python versions,
    producing wheels as output in `dist\`.

Compatibility notes
-------------------

- This building scheme above should be the safest one to use. In practice, many
  of the resulting wheels seem to be forwards- and backwards-compatible.
