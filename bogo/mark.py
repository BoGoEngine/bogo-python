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
Utility functions to deal with marks, which are diacritical markings
to change the base sound of a character but not its tonal quality.
E.g. the hat mark in â.
"""

from __future__ import unicode_literals

from bogo import accent, utils
from bogo.syllable import Syllable
Accent = accent.Accent


class Mark:
    HAT = 4
    HORN = 3
    BREVE = 2
    BAR = 1
    NONE = 0


FAMILY_A = "aăâ"
FAMILY_E = "eê"
FAMILY_O = "oơô"
FAMILY_U = "uư"
FAMILY_D = "dđ"


def get_mark_char(char):
    """
    Get the mark of a single char, if any.
    """
    char = accent.remove_accent_char(char.lower())
    if char == "":
        return Mark.NONE
    if char == "đ":
        return Mark.BAR
    if char in "ă":
        return Mark.BREVE
    if char in "ơư":
        return Mark.HORN
    if char in "âêô":
        return Mark.HAT
    return Mark.NONE


# TODO: Monstrous code. Needs refactoring.
def add_mark(syllable, mark):
    new_initial_consonant, new_vowel, new_final_consonant = syllable

    if mark == Mark.BAR and \
            syllable.initial_consonant and \
            syllable.initial_consonant[-1].lower() in FAMILY_D:
        new_initial_consonant = add_mark_at(
            syllable.initial_consonant,
            len(syllable.initial_consonant) - 1,
            Mark.BAR)
    else:
        raw_vowel = strip(syllable.vowel).lower()
        if mark == Mark.HAT:
            pos = max(raw_vowel.find("a"), raw_vowel.find("o"),
                      raw_vowel.find("e"))
            new_vowel = add_mark_at(syllable.vowel, pos, Mark.HAT)
        elif mark == Mark.BREVE:
            if raw_vowel != "ua":
                new_vowel = add_mark_at(
                    syllable.vowel, raw_vowel.find("a"), Mark.BREVE)
        elif mark == Mark.HORN:
            if raw_vowel in ("uo", "uoi", "uou"):
                new_vowel = "".join(
                    [add_mark_char(c, Mark.HORN) for c in syllable.vowel[:2]]) \
                    + syllable.vowel[2:]
            elif raw_vowel == "oa":
                new_vowel = add_mark_at(syllable.vowel, 1, Mark.HORN)
            else:
                pos = max(raw_vowel.find(""), raw_vowel.find("o"))
                new_vowel = add_mark_at(syllable.vowel, pos, Mark.HORN)
    if mark == Mark.NONE:
        if not raw_vowel == syllable.vowel.lower():
            new_vowel = raw_vowel
        elif syllable.initial_consonant and \
                syllable.initial_consonant[-1] == "đ":
            new_initial_consonant = syllable.initial_consonant[:-1] + "d"

    return Syllable(new_initial_consonant, new_vowel, new_final_consonant)


def add_mark_at(string, index, mark):
    """
    Add mark to the index-th character of the given string. Return the new string after applying change.
    Notice: index > 0
    """
    if index == -1:
        return string
    # Python can handle the case which index is out of range of given string
    return string[:index] + add_mark_char(string[index], mark) + string[index+1:]


def add_mark_char(char, mark):
    """
    Add mark to a single char.
    """
    if char == "":
        return ""
    case = char.isupper()
    ac = accent.get_accent_char(char)
    char = accent.add_accent_char(char.lower(), Accent.NONE)
    new_char = char
    if mark == Mark.HAT:
        if char in FAMILY_A:
            new_char = "â"
        elif char in FAMILY_O:
            new_char = "ô"
        elif char in FAMILY_E:
            new_char = "ê"
    elif mark == Mark.HORN:
        if char in FAMILY_O:
            new_char = "ơ"
        elif char in FAMILY_U:
            new_char = "ư"
    elif mark == Mark.BREVE:
        if char in FAMILY_A:
            new_char = "ă"
    elif mark == Mark.BAR:
        if char in FAMILY_D:
            new_char = "đ"
    elif mark == Mark.NONE:
        if char in FAMILY_A:
            new_char = "a"
        elif char in FAMILY_E:
            new_char = "e"
        elif char in FAMILY_O:
            new_char = "o"
        elif char in FAMILY_U:
            new_char = "u"
        elif char in FAMILY_D:
            new_char = "d"

    new_char = accent.add_accent_char(new_char, ac)
    return utils.change_case(new_char, case)


def is_valid_mark(syllable, mark_trans):
    """
    Check whether the mark given by mark_trans is valid to add to the components
    """
    if mark_trans == "*_":
        return True

    if mark_trans[0] == 'd' and syllable.initial_consonant \
            and syllable.initial_consonant[-1].lower() in ("d", "đ"):
        return True
    elif syllable.vowel and \
            strip(syllable.vowel).lower().find(mark_trans[0]) != -1:
        return True
    else:
        return False


def remove_mark_char(char):
    """Remove mark from a single character, if any."""
    return add_mark_char(char, Mark.NONE)


def remove_mark_string(string):
    return utils.join([remove_mark_char(c) for c in string])


def strip(string):
    """
    Strip a string of all marks and accents.
    """
    return remove_mark_string(accent.remove_accent_string(string))
