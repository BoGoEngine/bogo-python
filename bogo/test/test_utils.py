# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from nose.tools import eq_
from bogo.utils import *


def test_separate():
    eq_(separate(''), ['', '', ''])

    eq_(separate('a'), ['', 'a', ''])
    eq_(separate('b'), ['b', '', ''])

    eq_(separate('aa'), ['', 'aa', ''])
    eq_(separate('ae'), ['', 'ae', ''])

    eq_(separate('bb'), ['bb', '', ''])
    eq_(separate('bc'), ['bc', '', ''])

    eq_(separate('ba'), ['b', 'a', ''])
    eq_(separate('baa'), ['b', 'aa', ''])
    eq_(separate('bba'), ['bb', 'a', ''])
    eq_(separate('bbaa'), ['bb', 'aa', ''])

    eq_(separate('bac'), ['b', 'a', 'c'])
    eq_(separate('baac'), ['b', 'aa', 'c'])
    eq_(separate('bbac'), ['bb', 'a', 'c'])
    eq_(separate('bbaacc'), ['bb', 'aa', 'cc'])

    eq_(separate('baca'), ['bac', 'a', ''])
    eq_(separate('bacaa'), ['bac', 'aa', ''])
    eq_(separate('bacaacaeb'), ['bacaac', 'ae', 'b'])

    eq_(separate('long'), ['l', 'o', 'ng'])
    eq_(separate('HoA'), ['H', 'oA', ''])
    eq_(separate('TruoNg'), ['Tr', 'uo', 'Ng'])
    eq_(separate('QuyÊn'), ['Qu', 'yÊ', 'n'])
    eq_(separate('Trùng'), ['Tr', 'ù', 'ng'])
    eq_(separate('uông'), ['', 'uô', 'ng'])
    eq_(separate('giƯờng'), ['gi', 'Ườ', 'ng'])
    eq_(separate('gi'), ['g', 'i', ''])
    eq_(separate('aoe'), ['', 'aoe', ''])
    eq_(separate('uo'), ['', 'uo', ''])
    eq_(separate('uong'), ['', 'uo', 'ng'])
    eq_(separate('nhếch'), ['nh', 'ế', 'ch'])
    eq_(separate('ếch'), ['', 'ế', 'ch'])
    eq_(separate('xẻng'), ['x', 'ẻ', 'ng'])
    eq_(separate('xoáy'), ['x', 'oáy', ''])
    eq_(separate('quây'), ['qu', 'ây', ''])


class TestKeepCase():
    
    def test_keep_lower(self):
        
        @keep_case
        def function(string):
            return string.upper()
        
        eq_(function("abc"), "abc")
        
    def test_keep_title(self):
        
        @keep_case
        def function(string):
            return string.upper()
        
        eq_(function("Abc"), "Abc")
        
    def test_keep_upper(self):
        
        @keep_case
        def function(string):
            return string.title()
        
        eq_(function("ABC"), "ABC")
    
    def test_multiple_arguments(self):
        
        @keep_case
        def function(string, arg1, arg2, kwarg1=True):
            return "{} {} {} {}".format(string, arg1, arg2, kwarg1)
        
        result = function("abc", 1, 2, 3)
        expected = "abc 1 2 3"
        
        eq_(result, expected)
        
    def test_normalize_case(self):
        """
        Test that the string argument is always normalized to lower case.
        """
        inner = [0]
        
        @keep_case
        def function(string):
            inner[0] = string
            return string
        
        function("ABC")
        eq_(inner[0], "abc")
        
    def test_unrecognized_case(self):
        @keep_case
        def function(string):
            return string
        
        eq_(function("aBcD"), "abcd")
