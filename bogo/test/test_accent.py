# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from nose.tools import eq_
from bogo.accent import add_accent, add_accent_char, Accent
from bogo.syllable import Syllable


class TestAddAccentChar():
    
    def test_empty_char(self):
        result = add_accent_char('', Accent.GRAVE)
        expected = ''
        eq_(result, expected)
        
    def test_out_of_range_accent(self):
        result = add_accent_char('a', 293432)
        expected = 'a'
        eq_(result, expected)
        
    def test_normal_accent(self):
        result = add_accent_char('a', Accent.ACUTE)
        expected = 'á'
        eq_(result, expected)
    
    def test_upper_case(self):
        eq_(add_accent_char('A', Accent.ACUTE), 'Á')
        

class TestAddAccent():
    def test_remove_accent(self):
        s = Syllable('c', 'á', 'c')
        
        result = add_accent(s, Accent.NONE)
        expected = Syllable('c', 'a', 'c')
        
        eq_(result, expected)
        
    def test_e_hat(self):
        s = Syllable('ch', 'uyê', 'n')
        
        result = add_accent(s, Accent.HOOK)
        expected = Syllable('ch', 'uyể', 'n')
        
        eq_(result, expected)
        
    def test_o_horn(self):
        s = Syllable('ch', 'ươ', 'ng')
        
        result = add_accent(s, Accent.HOOK)
        expected = Syllable('ch', 'ưở', 'ng')
        
        eq_(result, expected)
        
    def test_double_vowel_no_final_consonant(self):
        s = Syllable('c', 'ua', '')
        
        result = add_accent(s, Accent.HOOK)
        expected = Syllable('c', 'ủa', '')
        
        eq_(result, expected)
        
    def test_double_vowel_with_final_consonant(self):
        s = Syllable('c', 'uô', 'ng')
        
        result = add_accent(s, Accent.GRAVE)
        expected = Syllable('c', 'uồ', 'ng')
        
        eq_(result, expected)
        
    def test_single_vowel(self):
        s = Syllable('c', 'a', '')
        
        result = add_accent(s, Accent.ACUTE)
        expected = Syllable('c', 'á', '')
        
        eq_(result, expected)
        
        s = Syllable('c', 'a', 'n')
        
        result = add_accent(s, Accent.ACUTE)
        expected = Syllable('c', 'á', 'n')
        
        eq_(result, expected)
        
        