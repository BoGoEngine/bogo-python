from nose.tools import eq_
from bogo.syllable import Syllable


class TestSyllable():

    def test_parse_simple_syllable(self):
        parsed = Syllable.new_from_string('tuong')

        expected = Syllable('t', 'uo', 'ng')
        eq_(parsed, expected)

    def test_parse_qua(self):
        parsed = Syllable.new_from_string('qua')

        expected = Syllable('qu', 'a', '')
        eq_(parsed, expected)

    def test_parse_gia(self):
        parsed = Syllable.new_from_string('gia')

        expected = Syllable('gi', 'a', '')
        eq_(parsed, expected)

    def test_parse_gi(self):
        parsed = Syllable.new_from_string('gi')

        expected = Syllable('g', 'i', '')
        eq_(parsed, expected)

    def test_parse_rubbish(self):
        parsed = Syllable.new_from_string('ohmyfkinggod')

        expected = Syllable('ohmyfkingg', 'o', 'd')
        eq_(parsed, expected)

    def test_append_initial_consonant(self):
        s = Syllable('c', '', '')
        s = s.append_char('c')
        
        expected = Syllable('cc', '', '')
        eq_(s, expected)
        
    def test_append_initial_consonant_empty(self):
        s = Syllable('', '', '')
        s = s.append_char('c')
        
        expected = Syllable('c', '', '')
        eq_(s, expected)
    
    def test_append_vowel(self):
        s = Syllable('c', 'a', '')
        s = s.append_char('a')
        
        expected = Syllable('c', 'aa', '')
        eq_(s, expected)
    
    def test_append_vowel_empty(self):
        s = Syllable('', '', '')
        s = s.append_char('a')
        
        expected = Syllable('', 'a', '')
        eq_(s, expected)
    
    def test_append_final_consonant(self):
        s = Syllable('c', 'a', 'c')
        s = s.append_char('c')
        
        expected = Syllable('c', 'a', 'cc')
        eq_(s, expected)