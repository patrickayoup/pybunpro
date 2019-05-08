from pybunpro import UserInformationSchema


class TestUserInformationSchema(object):

    def test_dump(self, user_information, user_information_dict):
        schema = UserInformationSchema()
        result, errors = schema.dump(user_information)

        assert errors == dict()
        assert result == user_information_dict

    def test_load(self, user_information, user_information_dict):
        schema = UserInformationSchema()
        result, errors = schema.load(user_information_dict)

        assert errors == dict()
        assert result == user_information
