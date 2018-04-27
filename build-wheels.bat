@echo off

:: https://en.wikibooks.org/wiki/Windows_Batch_Scripting#Command-line_arguments

if -%1-==-- (
    echo Usage: %0 ^<Python version^> [^<Python version^> ...]
    exit /b 1
)

echo Building PDCurses

:: nmake doesn't seem to have an option for switching the working directory
pushd PDCurses\wincon
nmake -f Makefile.vc WIDE=y UTF8=y
if %errorlevel% neq 0 (
    popd
    exit /b %errorlevel%
)
popd

:nextarg
if -%1-==-- goto end

echo Building wheel for Python %1

py -%1 setup.py bdist_wheel build_ext --include-dirs=PDCurses --library-dirs=PDCurses\wincon
if %errorlevel% neq 0 exit /b %errorlevel%

shift
goto nextarg
:end
