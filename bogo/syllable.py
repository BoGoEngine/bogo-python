import collections
from bogo import utils


class Syllable(collections.namedtuple('Syllable',
                           ['initial_consonant', 'vowel', 'final_consonant'])):

    @staticmethod
    def new_from_string(string):
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


    def append_char(self, char):
        """
        Append a character to `comps` following this rule: a vowel is added
        to the vowel part if there is no last consonant, else to the last
        consonant part; a consonant is added to the first consonant part
        if there is no vowel, and to the last consonant part if the
        vowel part is not empty.

        >>> transform(['', '', ''])
        ['c', '', '']
        >>> transform(['c', '', ''], '+o')
        ['c', 'o', '']
        >>> transform(['c', 'o', ''], '+n')
        ['c', 'o', 'n']
        >>> transform(['c', 'o', 'n'], '+o')
        ['c', 'o', 'no']
        """
        initial_consonant = self.initial_consonant
        vowel = self.vowel
        final_consonant = self.final_consonant

        if utils.is_vowel(char):
            if not self.final_consonant:
                vowel = self.vowel + char
            else:
                final_consonant = self.final_consonant + char
        else:
            if not self.final_consonant and not self.vowel:
                initial_consonant = self.initial_consonant + char
            else:
                final_consonant = self.final_consonant + char

        return Syllable(initial_consonant, vowel, final_consonant)
