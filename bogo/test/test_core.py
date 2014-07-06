from __future__ import unicode_literals
from nose.tools import eq_
from bogo import core
from bogo.syllable import Syllable
from bogo import accent
from bogo import mark


class TestAddCharTransformation:

    def test_add_simple_char(self):
        t = core.AddCharTransformation('a', 'a')
        syl = Syllable('', '', '')

        result = t.perform(syl)

        eq_(result, Syllable('', 'a', ''))


class TestAddToneMarkTransformation:

    def test_add_simple_tone(self):
        trans = core.AddToneMarkTransformation('s', accent.Accent.ACUTE)
        syl = Syllable('', 'a', '')
        result = trans.perform(syl)

        eq_(result, Syllable('', 'á', ''))


class TestAddCharMarkTransformation:

    def test_add_simple_mark(self):
        trans = core.AddCharMarkTransformation('a', mark.Mark.HAT)
        syl = Syllable('', 'a', '')
        result = trans.perform(syl)

        eq_(result, Syllable('', 'â', ''))


class TestRule:

    def test_parse_add_char(self):
        result = core.Rule.parse_rule_action('<ư', 'w')

        eq_(type(result), core.AddCharTransformation)
        eq_(result.char, 'ư')
        eq_(result.key, 'w')

    def test_parse_add_tone(self):
        result = core.Rule.parse_rule_action('?', 'r')

        eq_(type(result), core.AddToneMarkTransformation)
        eq_(result.tone, accent.Accent.HOOK)
        eq_(result.key, 'r')

    def test_parse_add_mark(self):
        result = core.Rule.parse_rule_action('^', 'a')

        eq_(type(result), core.AddCharMarkTransformation)
        eq_(result.mark, mark.Mark.HAT)
        eq_(result.key, 'a')

    def test_transformations_from_key_rule_key(self):
        rule = core.Rule({'w': ['*', '(']})
        trans_list = rule.transformations_from_key('w')

        eq_(len(trans_list), 2)
        eq_(type(trans_list[0]), core.AddCharMarkTransformation)
        eq_(type(trans_list[1]), core.AddCharMarkTransformation)

    def test_transformations_from_key_non_rule_key(self):
        rule = core.Rule({'w': ['*', '(']})
        trans_list = rule.transformations_from_key('a')

        eq_(len(trans_list), 1)
        eq_(type(trans_list[0]), core.AddCharTransformation)


class TestBoGo:
    def test_add_key_add_char(self):
        b = core.BoGo(core.Rule({}))
        b.add_key('a')

        eq_(b.result(), 'a')
        eq_(b.raw_string(), 'a')

    def test_add_key_add_tone(self):
        b = core.BoGo(core.Rule({'s': '/'}))
        b.add_key('a')
        b.add_key('s')

        eq_(b.result(), 'á')
        eq_(b.raw_string(), 'as')
