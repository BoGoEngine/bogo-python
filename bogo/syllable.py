import collections
from bogo import utils


Syllable = \
    collections.namedtuple('Syllable',
                           ['initial_consonant', 'vowel', 'final_consonant'])


def parse_syllable(string):
    """\
    Make a Syllable from a string.

    Args:
        - string: the string to be parsed

    Returns:
        a Syllable

    >>> parse_syllable('tuong')
    ('t','uo','ng')
    >>> parse_syllable('ohmyfkinggod')
    ('ohmyfkingg','o','d')
    """

    def atomic_separate(string, last_chars, last_is_vowel):
        if string == "" or (last_is_vowel != utils.is_vowel(string[-1])):
            return (string, last_chars)
        else:
            return atomic_separate(string[:-1],
                                   string[-1] + last_chars, last_is_vowel)

    head, last_consonant = atomic_separate(string, "", False)
    first_consonant, vowel = atomic_separate(head, "", True)

    if last_consonant and not (vowel + first_consonant):
        first_consonant = last_consonant
        last_consonant = ''

    # 'gi' and 'qu' are considered qualified consonants.
    # We want something like this:
    #     ['g', 'ia', ''] -> ['gi', 'a', '']
    #     ['q', 'ua', ''] -> ['qu', 'a', '']
    if len(vowel) > 1 and \
            (first_consonant + vowel[0]).lower() in ['gi', 'qu']:
        first_consonant += vowel[0]
        vowel = vowel[1:]

    return Syllable(first_consonant, vowel, last_consonant)
