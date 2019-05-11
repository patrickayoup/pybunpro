from pybunpro import GrammarPointSchema


class TestGrammarPointSchema(object):

    def test_dump(self, grammar_point, grammar_point_dict):
        schema = GrammarPointSchema()
        result, errors = schema.dump(grammar_point)

        assert errors == dict()
        assert result == grammar_point_dict

    def test_load(self, grammar_point, grammar_point_dict):
        schema = GrammarPointSchema()
        result, errors = schema.load(grammar_point_dict)

        assert errors == dict()
        assert result == grammar_point
