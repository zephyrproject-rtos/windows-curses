Python curses wheels for Windows
================================

This repository has the source code for the Python curses wheels provided by
Christoph Gohlke, set up for easy rebuilding. Only `build-wheels.bat` is
original work.

Wheels built from this repository are made available
[on PyPI](https://pypi.org/project/windows-curses/) and can be installed
with this command:

    pip install windows-curses

You can also download wheels from
[Gohlke's page](https://www.lfd.uci.edu/~gohlke/pythonlibs/#curses).

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

    Visual Studio 2017 will work for Python 3.5-3.7. For Python 3.5 support,
    you will need to check `VC++ 2015.3 v140 toolset for desktop (x86,x64)`
    during installation.

    *Note: It is a good idea to install older compilers before newer ones. See the Troubleshooting section.*

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

    Use the 32-bit version (`x86 Native Tools Command Prompt for VS 2017`) to build wheels for 32-bit
    Python versions, and the 64-bit version (e.g.
    `x64 Native Tools Command Prompt for VS 2017`) to build wheels for 64-bit Python versions.

    For Python 2.7, the Developer Prompt is called `Visual C++ 2008 32/64-bit` command prompt.

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

Rebuilding the wheels for Python 2.7, 3.5, 3.6, and 3.7
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In `Visual C++ 2008 32-bit Command Prompt`:

    build_wheels.bat 2.7-32


In `Visual C++ 2008 64-bit Command Prompt`:

    build_wheels.bat 2.7


In `x86 Native Tools Command Prompt for VS 2017`:

    build_wheels.bat 3.5-32 3.6-32 3.7-32


In `x64 Native Tools Command Prompt for VS 2017`:

    build_wheels.bat 3.5 3.6 3.7


This gives a set of wheels in `dist\`.

Compatibility note
------------------

This building scheme above should be the safest one to use. In practice, many
of the resulting wheels seem to be forwards- and backwards-compatible.

Troubleshooting
---------------

 - Python 2.7 wants to install both the 32- and 64-bit versions into the same
   directory by default. They must be installed into different directories.
   The Python launcher will still find them via `py -2.7` and and `py -2.7-32`.

 - Windows SDK 7.1 (which has Visual C++ 10.0, needed for Python 3.4) might
   refuse to install when Visual Studio 2017 is installed, giving an error
   related to a pre-release version of .NET Framework 4.

   I don't know if the problem also affects the full Visual Studio 2010.

   There is a
   [registry hack](https://stackoverflow.com/questions/31455926/windows-sdk-7-1-setup-failure)
   that seems to fix it. If you get a permission error trying to edit the registry
   key, see
   [this article](https://www.howtogeek.com/262464/how-to-gain-full-permissions-to-edit-protected-registry-keys/).

   Microsoft recommends installing earlier versions of Visual Studio before
   later ones. That might be the least-hassle solution.

   Also note that the x64 (64-bit) Visual C++ 10.0 compiler isn't freely
   available.

Uploading to PyPI
-----------------

Don't forget to bump the version number in `setup.py` before building new
wheels. [Semantic versioning](https://semver.org/) is intended.

Once the wheels are built, follow the instructions
[here](https://packaging.python.org/tutorials/distributing-packages/#uploading-your-project-to-pypi)
to upload them to PyPI.

`pip`/PyPI will look at the wheel metadata and automatically install the right
version of the wheel.
