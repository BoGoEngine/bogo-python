from nose.tools import eq_
from bogo.syllable import Syllable, parse_syllable


class TestSyllable():

    def test_parse_simple_syllable(self):
        parsed = parse_syllable('tuong')

        expected = Syllable('t', 'uo', 'ng')
        eq_(parsed, expected)

    def test_parse_qua(self):
        parsed = parse_syllable('qua')

        expected = Syllable('qu', 'a', '')
        eq_(parsed, expected)

    def test_parse_gia(self):
        parsed = parse_syllable('gia')

        expected = Syllable('gi', 'a', '')
        eq_(parsed, expected)

    def test_parse_gi(self):
        parsed = parse_syllable('gi')

        expected = Syllable('g', 'i', '')
        eq_(parsed, expected)

    def test_parse_rubbish(self):
        parsed = parse_syllable('ohmyfkinggod')

        expected = Syllable('ohmyfkingg', 'o', 'd')
        eq_(parsed, expected)
