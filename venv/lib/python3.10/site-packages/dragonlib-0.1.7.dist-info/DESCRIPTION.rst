--------------------------
Dragon/CoCO Python Library
--------------------------

Python Modules/Tools Open source (GPL v3 or later) for 6809 based homecomputer like:

* ``Dragon 32`` : `http://en.wikipedia.org/wiki/Dragon_32 <http://en.wikipedia.org/wiki/Dragon_32>`_

* ``Tandy TRS-80 Color Computer`` (CoCo) : `http://en.wikipedia.org/wiki/TRS-80_Color_Computer <http://en.wikipedia.org/wiki/TRS-80_Color_Computer>`_

Used in:

``DragonPy`` - Emulator for 6809 CPU based system like Dragon 32 / CoCo written in Python:

* `https://github.com/jedie/DragonPy <https://github.com/jedie/DragonPy>`_

``DwLoadServer`` - DWLOAD server implemented in Python

* `https://github.com/DWLOAD/DwLoadServer <https://github.com/DWLOAD/DwLoadServer>`_

Tested with Python 3.4, 2.7 and PyPy 2

+-----------------------------------+----------------------------------+
| |Build Status on travis-ci.org|   | `travis-ci.org/6809/dragonlib`_  |
+-----------------------------------+----------------------------------+
| |Coverage Status on coveralls.io| | `coveralls.io/r/6809/dragonlib`_ |
+-----------------------------------+----------------------------------+

.. |Build Status on travis-ci.org| image:: https://travis-ci.org/6809/dragonlib.svg
.. _travis-ci.org/6809/dragonlib: https://travis-ci.org/6809/dragonlib/
.. |Coverage Status on coveralls.io| image:: https://coveralls.io/repos/6809/dragonlib/badge.svg
.. _coveralls.io/r/6809/dragonlib: https://coveralls.io/r/6809/dragonlib

run unittests
=============

::

    /home/FooBar$ cd DragonPy_env
    /home/FooBar/DragonPy_env$ source bin/activate
    (DragonPy_env)~/DragonPy_env$ cd src/dragonlib
    (DragonPy_env)~/DragonPy_env/src/dragonlib$ ./setup.py nosetests

-------
History
-------

* `21.08.2015 - v0.1.7 <https://github.com/6809/dragonlib/compare/v0.1.6...v0.1.7>`_:

    * Bugfixes: Disable logging, again ;)

    * remove own six and add it to setup.py "install_requires"

    * cleanup code

* `19.08.2015 - v0.1.6 <https://github.com/6809/dragonlib/compare/v0.1.5...v0.1.6>`_:

    * Bugfixes: Disable logging

    * use nose to run unittests

* 26.05.2015 - v0.1.5 - `Bugfixes to support Py2, too. <https://github.com/6809/dragonlib/compare/v0.1.4...v0.1.5>`_

* 26.05.2015 - v0.1.4 - `Update test code, use travis-ci.org and coveralls.io <https://github.com/6809/dragonlib/compare/v0.1.3...v0.1.4>`_

* 15.12.2014 - v0.1.3 - `Add a Pygments Lexer <https://github.com/6809/dragonlib/compare/v0.1.2...v0.1.3>`_

* 19.11.2014 - v0.1.2 - `Bugfix "api.bin2bas()" and "api.bas2bin()" <https://github.com/6809/dragonlib/compare/v0.1.1...v0.1.2>`_

* 15.11.2014 - v0.1.1 - Add ``api.bin2bas()`` and ``api.bas2bin()`` for Dragon DOS Binary <-> ASCII listing

* 25.08.2014 - Split from DragonPy project

* TODO: Add old history ;)

------
Links:
------

+--------+--------------------------------------------+
| Forum  | `http://forum.pylucid.org/`_               |
+--------+--------------------------------------------+
| IRC    | `#pylucid on freenode.net`_                |
+--------+--------------------------------------------+
| Jabber | pylucid@conference.jabber.org              |
+--------+--------------------------------------------+
| PyPi   | `https://pypi.python.org/pypi/DragonLib/`_ |
+--------+--------------------------------------------+
| Github | `https://github.com/6809/dragonlib`_       |
+--------+--------------------------------------------+

.. _http://forum.pylucid.org/: http://forum.pylucid.org/
.. _#pylucid on freenode.net: http://www.pylucid.org/permalink/304/irc-channel
.. _https://pypi.python.org/pypi/DragonLib/: https://pypi.python.org/pypi/DragonLib/
.. _https://github.com/6809/dragonlib: https://github.com/6809/dragonlib

--------
donation
--------

* Send `Bitcoins <http://www.bitcoin.org/>`_ to `1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F <https://blockexplorer.com/address/1823RZ5Md1Q2X5aSXRC5LRPcYdveCiVX6F>`_

