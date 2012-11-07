#-*- coding: utf-8
# New BoGo Engine - Vietnamese Text processing engine
#
# Copyright (c) 2012- Long T. Dam <longdt90@gmail.com>,
#                     Trung Ngo <ndtrung4419@gmail.com>
#
# This file is part of BoGo IBus Engine Project BoGo IBus Engine is
# free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# IBus-BoGo is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with IBus-BoGo. If not, see <http://www.gnu.org/licenses/>.

import utils

class Accent:
    GRAVE = 5
    ACUTE = 4
    HOOK = 3
    TIDLE= 2
    DOT = 1
    NONE = 0

def add_accent(components, accent):
    """
    Add accent to the given components.  The parameter components is
    the result of function separate()
    """
    vowel = components[1]
    last_consonant = components[2]
    if accent == Accent.NONE:
        vowel = utils.join([add_accent_char(c, Accent.NONE) for c in vowel])
        return [components[0], vowel, last_consonant]

    if vowel == u"":
        return components
    #raw_string is a list, not a str object
    raw_string = utils.join([add_accent_char(c, Accent.NONE).lower() for c in vowel])
    new_vowel = u""
    # Highest priority for ê and ơ
    index = max(raw_string.find(u"ê"), raw_string.find(u"ơ"))
    if index != -1:
        new_vowel = vowel[:index] + add_accent_char(vowel[index], accent) + vowel[index+1:]
    elif len(vowel) == 1 or (len(vowel) == 2 and last_consonant == u""):
        new_vowel =add_accent_char(vowel[0], accent) + vowel[1:]
    else:
        new_vowel = vowel[:1] + add_accent_char(vowel[1], accent) + vowel[2:]
    return [components[0], new_vowel, components[2]]

def add_accent_char(char, accent):
    """
    Add accent to a single char.  Parameter accent is member of class
    Accent
    """
    if char == u'':
        return u'';
    case = char.islower()
    char = char.lower()
    index = utils.VOWELS.find(char)
    if (index != -1):
        index = index - index % 6 + 5
        char = utils.VOWELS[index - accent]
    return utils.change_case(char, case)

def get_accent_char(char):
    """
    Get accent of an single char
    """
    index = utils.VOWELS.find(char.lower())
    if (index != -1):
        return 5 - index % 6
    else:
        return Accent.NONE
        
def add_accent_at(string, mark, accent):
    """
    Add mark to the index-th character of the given string.  Return
    the new string after applying change.
    """
    if index == -1:
        return string
    # Python can handle the case which index is out of range of given string
    return string[:index] + accent.accent.add_accent_char(string[index], accent) \
        + string[index+1:]
