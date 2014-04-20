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
>>> bogo.process_key(string='ca', key='s', fallback_sequence='ca')
('cá', 'cas')
>>> bogo.process_key(string='cá', key='n', fallback_sequence='cas')
('cán', 'casn')
```

`process_key()` is intended to be called successively on each keystroke with
the following arguments.

- `string`: The previously processed string or "".
- `key`: The keystroke.
- `fallback_sequence`: The previous keystrokes.
- `input_method_definition` (optional): A dictionary listing
  transformation rules. Defaults to the value returned by `get_telex_definition()`.
- `skip_non_vietnamese` (optional): Whether to skip results that
  doesn't seem like Vietnamese. Defaults to True.

It returns a tuple. The first item of which is the processed
Vietnamese string, the second item is the next fallback sequence.
The two items are to be fed back into the next call of process_key()
as `string` and `fallback_sequence`. If `skip_non_vietnamese` is
True and the resulting string doesn't look like Vietnamese,
both items contain the `fallback_sequence`.

Note that when a key is an undo key, it won't get appended to
`fallback_sequence`.

```python
>>> process_key('â', 'a', 'aa')
(aa, aa)
```

`input_method_definition` is a dictionary that maps keystrokes to
their effect string. The effects can be one of the following:

- 'a^': a with circumflex (â), only affect an existing 'a family'
- 'a+': a with breve (ă), only affect an existing 'a family'
- 'e^': e with circumflex (ê), only affect an existing 'e family'
- 'o^': o with circumflex (ô), only affect an existing 'o family'
- 'o*': o with horn (ơ), only affect an existing 'o family'
- 'd-': d with bar (đ), only affect an existing 'd'
- '/': acute (sắc), affect an existing vowel
- '\\': grave (huyền), affect an existing vowel
- '?': hook (hỏi), affect an existing vowel
- '~': tilde (ngã), affect an existing vowel
- '.': dot (nặng), affect an existing vowel
- '<ư': append ư
- '<ơ': append ơ

A keystroke entry can have multiple effects, in which case the
dictionary entry's value should be a list of the possible
effect strings. Although you should try to avoid this if
you are defining a custom input method rule.

We have already defined input method definitions for TELEX and VNI with the
`get_telex_definition()` and `get_vni_definition()` functions.

More help is available as docstring for each module and function.

BoGo is well tested with Python 3.2 and Python 3.3.
