# -*- coding: utf-8 -*-

"""\
BoGo is a Python 3 Vietnamese input method conversion library. This library
is intentionally functional with no internal state and side-effect.

Usage
-----

>>> import bogo
>>> bogo.process_sequence('meof')
'mèo'
>>> bogo.process_sequence('meo2', rules=bogo.get_vni_definition())
'mèo'
```

Some functions from bogo.bogo are exported to package toplevel:

    - process_key()
    - process_sequence()
    - get_telex_definition()
    - get_vni_definition()

Read help(bogo.bogo) for more help.
"""

from bogo.bogo import \
    process_key, \
    process_sequence, \
    get_telex_definition, \
    get_vni_definition
