from pybunpro import UserInformation


class TestUserInformation(object):

    def test_constructor(self, username, grammar_point_count,
                         ghost_review_count, creation_date):
        user_info = UserInformation(username, grammar_point_count,
                                    ghost_review_count, creation_date)
        assert user_info.username == username
        assert user_info.grammar_point_count == grammar_point_count
        assert user_info.ghost_review_count == ghost_review_count
        assert user_info.creation_date == creation_date
