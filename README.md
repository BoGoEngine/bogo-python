BoGo
====

[![Build Status](https://travis-ci.org/BoGoEngine/bogo-python.svg?branch=master)](https://travis-ci.org/BoGoEngine/bogo-python)
[![Coverage Status](https://coveralls.io/repos/BoGoEngine/bogo-python/badge.png?branch=master)](https://coveralls.io/r/BoGoEngine/bogo-python?branch=master)

BoGo is a Python 3 Vietnamese input method conversion library. This library
is intentionally functional with no internal state and side-effect.

Usage
-----

```python
>>> import bogo
>>> bogo.process_sequence('meof')
'mèo'
>>> bogo.process_sequence('meo2', rules=bogo.get_vni_definition())
'mèo'
```


Some functions from bogo.bogo are exported to package toplevel:

- `process_key()`
- `process_sequence()`
- `get_telex_definition()`
- `get_vni_definition()`

Read `help(bogo.bogo)` in the Python interpreter for more help.

BoGo is extensively tested with Python 3.2 and Python 3.3.
