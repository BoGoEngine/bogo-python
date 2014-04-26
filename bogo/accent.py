# -*- coding: utf-8 -*-
#
# This file is part of ibus-bogo project.
#
# Copyright (C) 2012 Long T. Dam <longdt90@gmail.com>
# Copyright (C) 2012-2014 Trung Ngo <ndtrung4419@gmail.com>
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
Utility functions to deal with accents (also called tones),
which are diacritical markings that changes the pitch of a character.
E.g. the acute accent in á.
"""

# TODO: add is_valid_accent() to be on par with mark.py and use it
# at the end of new_bogo_engine.transform()

from __future__ import unicode_literals
from bogo import utils
from bogo.syllable import Syllable


class Accent:
    MAX_VALUE = 6
    GRAVE = 5
    ACUTE = 4
    HOOK = 3
    TIDLE = 2
    DOT = 1
    NONE = 0


def get_accent_char(char):
    """
    Get the accent of an single char, if any.
    """
    index = utils.VOWELS.find(char.lower())
    if (index != -1):
        return 5 - index % 6
    else:
        return Accent.NONE


def get_accent_string(string):
    """
    Get the first accent from the right of a string.
    """
    accents = list(filter(lambda accent: accent != Accent.NONE,
                          map(get_accent_char, string)))
    return accents[-1] if accents else Accent.NONE


def add_accent(syllable, accent):
    """
    Add accent to the given syllable.
    """
    vowel = syllable.vowel

    if not vowel:
        return syllable

    if accent == Accent.NONE:
        vowel = remove_accent_string(vowel)
        return Syllable(syllable.initial_consonant, vowel, syllable.final_consonant)

    vowel_wo_accent = remove_accent_string(vowel).lower()
    new_vowel = ''
    
    # Highest priority for ê and ơ
    index = max(vowel_wo_accent.find("ê"), vowel_wo_accent.find("ơ"))
    found_e_hat_or_o_horn = index != -1
    
    if found_e_hat_or_o_horn:
        # Add accent mark to the found ê or ơ
        new_vowel = \
            vowel[:index] + \
            add_accent_char(vowel[index], accent) + \
            vowel[index + 1:]
    elif len(vowel) == 1 or (len(vowel) == 2 and not syllable.final_consonant):
        # cá
        # cháo
        first_vowel_char = vowel[0]
        first_vowel_char_with_accent = add_accent_char(first_vowel_char, accent)
        new_vowel = first_vowel_char_with_accent + vowel[1:]
    else:
        # biến
        # khuỷu
        second_vowel_char = vowel[1]
        second_vowel_char_with_accent = add_accent_char(second_vowel_char, accent)
        new_vowel = vowel[:1] + second_vowel_char_with_accent + vowel[2:]

    return Syllable(syllable.initial_consonant, new_vowel, syllable.final_consonant)


@utils.keep_case
def add_accent_char(char, accent):
    """
    Add accent to a single char.
    
    Args:
        accent: an Accent enum value
    """
    if not (char and accent in range(0, Accent.MAX_VALUE + 1)):
        return char

    index = utils.VOWELS.find(char)
    if (index != -1):
        index = index - index % 6 + 5
        char = utils.VOWELS[index - accent]

    return char


def remove_accent_char(char):
    """
    Remove accent from a single char, if any.
    """
    return add_accent_char(char, Accent.NONE)


def remove_accent_string(string):
    """
    Remove all accent from a whole string.
    """
    return utils.join([add_accent_char(c, Accent.NONE) for c in string])
