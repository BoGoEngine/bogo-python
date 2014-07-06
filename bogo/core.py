# -*- coding: utf-8 -*-
#
# This file is part of ibus-bogo project.
#
# Copyright (C) 2012 Long T. Dam <longdt90@gmail.com>
# Copyright (C) 2012-2013 Trung Ngo <ndtrung4419@gmail.com>
# Copyright (C) 2013 Duong H. Nguyen <cmpitg@gmail.com>
#
# ibus-bogo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ibus-bogo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ibus-bogo.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Read the docstring for process_sequence() and process_key() first.
"""

from __future__ import unicode_literals
from bogo.validation import is_valid_combination
from bogo.syllable import Syllable
from bogo import utils, accent, mark
import sys
import string


Mark = mark.Mark
Accent = accent.Accent


class _Action:
    UNDO = 3
    ADD_MARK = 2
    ADD_ACCENT = 1
    ADD_CHAR = 0


def get_telex_definition(w_shorthand=True, brackets_shorthand=True):
    """Create a definition dictionary for the TELEX input method

    Args:
        w_shorthand (optional): allow a stand-alone w to be
            interpreted as an ư. Default to True.
        brackets_shorthand (optional, True): allow typing ][ as
            shorthand for ươ. Default to True.

    Returns a dictionary to be passed into process_key().
    """
    telex = {
        "a": "^",
        "o": "^",
        "e": "^",
        "w": ["*", "("],
        "d": "-",
        "f": "\\",
        "s": "/",
        "r": "?",
        "x": "~",
        "j": ".",
    }

    if w_shorthand:
        telex["w"].append('<ư')

    if brackets_shorthand:
        telex.update({
            "]": "<ư",
            "[": "<ơ",
            "}": "<Ư",
            "{": "<Ơ"
        })

    return telex


def get_vni_definition():
    """Create a definition dictionary for the VNI input method.

    Returns a dictionary to be passed into process_key().
    """
    return {
        "6": ["a^", "o^", "e^"],
        "7": ["u*", "o*"],
        "8": "a+",
        "9": "d-",
        "2": "\\",
        "1": "/",
        "3": "?",
        "4": "~",
        "5": "."
    }


def _accepted_chars(rules):
    if sys.version_info[0] > 2:
        accepted_chars = \
            string.ascii_letters + \
            ''.join(rules.keys())
    else:
        accepted_chars = \
            string.lowercase + \
            string.uppercase + \
            ''.join(rules.keys())

    return accepted_chars


def process_sequence(sequence,
                     rules=None,
                     skip_non_vietnamese=True):
    """\
    Convert a key sequence into a Vietnamese string with diacritical marks.

    Args:
        rules (optional): see docstring for process_key().
        skip_non_vietnamese (optional): see docstring for process_key().

    It even supports continous key sequences connected by separators.
    i.e. process_sequence('con meof.ddieen') should work.
    """
    result = ""
    result_parts = []
    if rules is None:
        rules = get_telex_definition()

    accepted_chars = _accepted_chars(rules)
    rules = Rule(rules)
    bg = BoGo(rules)

    for key in sequence:
        if key not in accepted_chars:
            result_parts.append(result)
            result_parts.append(key)
            result = ""
        else:
            result = bg.add_key(key)

    result_parts.append(result)
    return ''.join(result_parts)


class Transformation:

    def __init__(self, key):
        self.key = key

    def perform(self, syllable):
        raise NotImplementedError


class AddCharTransformation(Transformation):
    def __init__(self, key, char):
        super(AddCharTransformation, self).__init__(key)
        self.char = char

    def perform(self, syllable):
        return syllable.append_char(self.char)


class AddToneMarkTransformation(Transformation):
    def __init__(self, key, tone):
        super(AddToneMarkTransformation, self).__init__(key)
        self.tone = tone

    def perform(self, syllable):
        return accent.add_accent(syllable, self.tone)


class AddCharMarkTransformation(Transformation):
    def __init__(self, key, mark):
        super(AddCharMarkTransformation, self).__init__(key)
        self.mark = mark

    def perform(self, syllable):
        return mark.add_mark(syllable, self.mark)


class Rule:
    mark_action = {
        '^': Mark.HAT,
        '(': Mark.BREVE,
        '*': Mark.HORN,
        '-': Mark.BAR,
    }

    accent_action = {
        '\\': Accent.GRAVE,
        '/': Accent.ACUTE,
        '?': Accent.HOOK,
        '~': Accent.TIDLE,
        '.': Accent.DOT,
    }

    def __init__(self, rule_dict):
        self.rule_dict = rule_dict

    @staticmethod
    def parse_rule_action(rule_action, key):
        # Each typing rule consists of 2 parts: a predicate and
        # an action associated with that predicate.
        # e.g.: In the rule 'r -> ?', 'r' is the key, the predicate,
        #       and ? is the action (add a HOOK tone mark to the
        #       suitable vowel).

        if rule_action[0] == '<':
            # <ư
            trans = AddCharTransformation(key, rule_action[1])
        # elif rule_action[0] == "_":
        #     # _a^
        #     trans = Transformation(_Action.UNDO, rule_action[1:])
        elif rule_action in Rule.mark_action:
            # ^
            trans = AddCharMarkTransformation(
                key, Rule.mark_action[rule_action])
        elif rule_action in Rule.accent_action:
            # ?
            trans = AddToneMarkTransformation(
                key, Rule.accent_action[rule_action])
        else:
            # TODO ?
            raise ValueError

        if type(trans) is AddCharTransformation:
            if key.isupper():
                trans.key = trans.key.toupper()

        return trans

    def transformations_from_key(self, key):
        if key in self.rule_dict:
            return [self.parse_rule_action(rule_action, key)
                    for rule_action in self.rule_dict[key]]
        else:
            return [AddCharTransformation(key, key)]


class BoGo:
    def __init__(self, typing_rule):
        self.rule = typing_rule
        self.transformations = []
        self.syllable = Syllable('', '', '')

    def raw_string(self):
        return "".join([trans.key for trans in self.transformations])

    def result(self):
        return self.syllable.as_string()

    def best_transformation(self, transformations):
        return transformations[0]

    def add_key(self, key):
        transformation = self.best_transformation(
            self.rule.transformations_from_key(key))

        self.syllable = transformation.perform(self.syllable)
        self.transformations.append(transformation)

        return self.syllable.as_string()
