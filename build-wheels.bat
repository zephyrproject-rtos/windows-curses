@echo off

if -%1-==-- (
    echo Usage: %0 ^<Python version^> [^<Python version^> ...]
    exit /b 1
)


::
:: Build PDCurses
::

:: nmake doesn't seem to have an option for switching the working directory
pushd PDCurses\wincon

:: Always build PDCurses from scratch. This avoids issues with doing a 32-bit
:: build after a 64-bit build for example.

echo Cleaning PDCurses

nmake -f Makefile.vc clean

echo Building PDCurses

nmake -f Makefile.vc WIDE=y UTF8=y
if %errorlevel% neq 0 (
    popd
    echo Check that you're using the Developer Command Prompt
    exit /b %errorlevel%
)

popd


::
:: Build wheels
::

:: Process arguments one by one
:nextarg
if -%1-==-- goto end

echo Building wheel for Python %1

py -%1 setup.py clean --all bdist_wheel build_ext
if %errorlevel% neq 0 (
    echo Check that you have the 'wheel' module installed for Python %1 and are
    echo building with the right compiler
    exit /b %errorlevel%
)

shift
goto nextarg
:end
