Python curses wheels for Windows
================================

This is the repository for the [windows-curses wheels on
PyPI](https://pypi.org/project/windows-curses). The wheels are based on the
[wheels on Christoph Gohlke's
page](https://www.lfd.uci.edu/~gohlke/pythonlibs/#curses).

Only `build-wheels.bat` is original work.

Wheels built from this repository can be installed with this command:

    pip install windows-curses

Starting with version 2.0, these wheels include a hack to make resizing work
for Python applications that haven't been specifically adapted for PDCurses.
See commit 30ca08b ("Automatically call resize\_term(0, 0) for
get{ch,key,\_wch}()") and the project description on PyPI. This hack is not in
Gohlke's wheels.

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
UTF-8. Remove `UTF8=y` from the `nmake` line in `build-wheels.bat` to use the
default system encoding instead.

Build instructions
------------------

 1. Clone the repository with the following command:

        git clone --recurse-submodules https://github.com/ulfalizer/windows-curses-wheels.git

    `--recurse-submodules` pulls in the required PDCurses Git submodule.

 2. Install compilers compatible with the Python versions that you want to
    builds wheel for by following the instructions at
    https://wiki.python.org/moin/WindowsCompilers.

    Visual Studio 2019 will work for Python 3.5-3.8. For Python 3.5 support,
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

    Use the 32-bit version (`x86 Native Tools Command Prompt for VS 2019`) to build wheels for 32-bit
    Python versions, and the 64-bit version (e.g.
    `x64 Native Tools Command Prompt for VS 2019`) to build wheels for 64-bit Python versions.

    For Python 2.7, the Developer Prompt is called `Visual C++ 2008 32/64-bit` command prompt.

 7. Run `build-wheels.bat`, passing it the Python version you're building a
    wheel for. For example, the following command will build a wheel for
    Python 3.5:

        build-wheels.bat 3.5

    If you have both 32-bit and 64-bit versions of the same Python version
    installed and are building a 32-bit wheel, add "-32" to the version
    number, like in the following example:

        build-wheels.bat 3.5-32

    If you are building multiple wheels for Python versions that are all
    compatible with the same compiler, you can list all of them in the same
    command:

        build-wheels.bat 3.5 3.6

    `build-wheels.bat` first cleans and rebuilds PDCurses, and then builds and
    links the source code in `pyXY\` for each of the specified Python versions,
    producing wheels as output in `dist\`.

### Rebuilding the wheels for Python 2.7, 3.5, 3.6, 3.7, and 3.8

In `Visual C++ 2008 32-bit Command Prompt`:

    build-wheels.bat 2.7-32


In `Visual C++ 2008 64-bit Command Prompt`:

    build-wheels.bat 2.7


In `x86 Native Tools Command Prompt for VS 2019`:

    build-wheels.bat 3.5-32 3.6-32 3.7-32 3.8-32


In `x64 Native Tools Command Prompt for VS 2019`:

    build-wheels.bat 3.5 3.6 3.7 3.8


This gives a set of wheels in `dist\`.

Compatibility note
------------------

This building scheme above should be the safest one to use. In practice, many
of the resulting wheels seem to be forwards- and backwards-compatible.

Troubleshooting
---------------

 - Python 2.7 wants to install both the 32- and 64-bit versions into the same
   directory by default. They must be installed into different directories.
   The Python launcher will still find them via `py -2.7` and `py -2.7-32`.

 - Windows SDK 7.1 (which has Visual C++ 10.0, needed for Python 3.4) might
   refuse to install when Visual Studio 2019 is installed, giving an error
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

Adding support for a new Python version
---------------------------------------

1. Create a new directory for the Python version, e.g. `py39\`

2. Copy `Modules\_cursesmodule.c` from the CPython source code to `py39\_cursesmodule.c`

3. Apply the patches from commit b1cf4e1 ("Add 3.8 curses patch") and commit 30ca08b ("Automatically call resize\_term(0, 0) for get{ch,key,\_wch}()")

4. Copy `Modules\_curses_panel.c`, `Modules\clinic\_cursesmodule.c.h`, and `Modules\clinic\_curses_panel.c.h` from the CPython sources to `py39\_curses_panel.c`, `py39\clinic\_cursesmodule.c.h` and `py39\clinic\_curses_panel.c.h`, respectively

In practise, `Modules\_cursesmodule.c` from newer Python 3 versions is likely to be compatible with older Python 3 versions too. The Python 3.4, 3.5, 3.6, and 3.7 wheels are currently built from identical `_cursesmodule.c` files (but not the Python 3.8 wheels, though they probably could be).
