from pybunpro import GrammarPoint


class TestGrammarPoint(object):

    def test_constructor(self, grammar_point_item, created_at_date,
                         updated_at_date):
        grammar_point = GrammarPoint(grammar_point_item, created_at_date,
                                     updated_at_date)

        assert grammar_point.grammar_point == grammar_point_item
        assert grammar_point.created_at_date == created_at_date
        assert grammar_point.updated_at_date == updated_at_date
