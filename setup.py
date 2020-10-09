import sys

from setuptools import setup, Extension

libraries = ['pdcurses', 'user32', 'advapi32', 'gdi32', 'comdlg32', 'shell32']

define_macros = [
    ('PDC_WIDE', None),
    ('HAVE_NCURSESW', None),
    ('HAVE_TERM_H', None),
    ('HAVE_CURSES_IS_TERM_RESIZED', None),
    ('HAVE_CURSES_RESIZE_TERM', None),
    ('HAVE_CURSES_TYPEAHEAD', None),
    ('HAVE_CURSES_HAS_KEY', None),
    ('HAVE_CURSES_FILTER', None),
    ('HAVE_CURSES_WCHGAT', None),
    ('HAVE_CURSES_USE_ENV', None),
    ('HAVE_CURSES_IMMEDOK', None),
    ('HAVE_CURSES_SYNCOK', None),
    # ('HAVE_CURSES_IS_PAD', None),
    ('WINDOW_HAS_FLAGS', None),
    ('NCURSES_MOUSE_VERSION', 2),
    ('_ISPAD', 0x10),
    ('is_term_resized', 'is_termresized'),
]

srcdir = 'py%i%i//' % sys.version_info[:2]

include_dirs = ["PDCurses", "."]
library_dirs = ["PDCurses/wincon"]

LONG_DESCRIPTION = """
Adds support for the standard Python `curses` module on Windows. Based on
[these wheels](https://www.lfd.uci.edu/~gohlke/pythonlibs/#curses). Uses the
PDCurses curses implementation.

The wheels are built from [this GitHub
repository](https://github.com/zephyrproject-rtos/windows-curses).

PDCurses is compiled with wide character support, meaning `get_wch()` is
available. UTF-8 is forced as the encoding.

Starting from windows-curses 2.0, in the name of pragmatism, these wheels (but
not Gohlke's) include a hack to make resizing work for applications developed
against ncurses without Python code changes: Whenever `getch()`, `getkey()`, or
`get_wch()` return `KEY_RESIZE`, `resize_term(0, 0)` is called automatically.
This gives behavior similar to the automatic `SIGWINCH` handling in ncurses
(see PDCurses' `resize_term()` documentation). [This
commit](https://github.com/zephyrproject-rtos/windows-curses/commit/30ca08bfbcb7a332228ddcde026181b2009ea0a7)
implements the hack.

To add the same hack in Python code (which is harmless, and needed if you want
resizing to work with older windows-curses versions or with Gohlke's wheels),
call `curses.resize_term(0, 0)` after receiving `KEY_RESIZE`, and ignore any
`curses.error` exceptions. ncurses reliably fails and does nothing for
`resize_term(0, 0)`, so this is safe on *nix.

Please tell me if the `resize_term(0, 0)` hackery causes you any trouble.
"""[1:-1]

setup(
    name='windows-curses',
    version='2.2.0',
    description="Support for the standard curses module on Windows",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/zephyrproject-rtos/windows-curses",
    license='PSF2',
    ext_modules=[
        Extension('_curses',
                  # term.h and terminfo.c was removed from PDCurses in commit
                  # 6b569295 ("Eliminated term.h, terminfo.c; moved mvcur() to
                  # move.c"). They provide functions that are called
                  # unconditionally by _cursesmodule.c, so we keep a copy of
                  # the last versions in this repo.
                  #
                  # See https://github.com/wmcbrine/PDCurses/issue/55.
                  sources=[srcdir + '_cursesmodule.c', 'terminfo.c'],
                  define_macros=define_macros,
                  include_dirs=include_dirs,
                  library_dirs=library_dirs,
                  libraries=libraries),
        Extension('_curses_panel',
                  sources=[srcdir + '_curses_panel.c'],
                  define_macros=define_macros,
                  include_dirs=include_dirs,
                  library_dirs=library_dirs,
                  libraries=libraries)
    ],
    project_urls={
        "GitHub repository": "https://github.com/zephyrproject-rtos/windows-curses",
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console :: Curses',
        'Environment :: Win32 (MS Windows)',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
)
