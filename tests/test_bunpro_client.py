import pytest

from pybunpro import BunproClient, SchemaError


class TestBunproClient(object):

    @pytest.fixture
    def api_key(self):
        return 'dqcfu2qchoic3ucdooeravhvyhn1rdur'

    @pytest.fixture
    def study_queue_information_dict(self, reviews_available,
                                     next_review_date_ts,
                                     reviews_available_next_hour,
                                     reviews_available_next_day):
        return dict(reviews_available=reviews_available,
                    next_review_date=next_review_date_ts,
                    reviews_available_next_hour=reviews_available_next_hour,
                    reviews_available_next_day=reviews_available_next_day)

    @pytest.fixture
    def mock_study_queue_response(self, user_information_dict,
                                  study_queue_information_dict):
        return dict(user_information=user_information_dict,
                    requested_information=study_queue_information_dict)

    @pytest.fixture
    def mock_recent_items_response(self, user_information_dict,
                                   grammar_point_dict):
        return dict(user_information=user_information_dict,
                    requested_information=[grammar_point_dict])

    @pytest.fixture
    def mock_bad_user_info_response(self, study_queue_information_dict):
        return dict(user_information=dict(),
                    requested_information=study_queue_information_dict)

    @pytest.fixture
    def mock_bad_requested_info_response(self, user_information_dict):
        return dict(user_information=user_information_dict,
                    requested_information=dict())

    def test_constructor(self, api_key):
        client = BunproClient(api_key)
        assert client._api_key == api_key
        assert client._base_url == f'https://bunpro.jp/api/user/{api_key}'

    def test_constructor_none_api_key_raises_exception(self):
        with pytest.raises(TypeError):
            BunproClient(None)

    def test_study_queue(self, requests_mock, api_key,
                         mock_study_queue_response, user_information,
                         study_queue):
        requests_mock.get(f'https://bunpro.jp/api/user/{api_key}/study_queue',
                          json=mock_study_queue_response)
        client = BunproClient(api_key)
        r_user_info, r_requested_info = client.study_queue()

        assert r_user_info == user_information
        assert r_requested_info == study_queue

    def test_study_queue_user_info_parse_error(self, requests_mock, api_key,
                                               mock_bad_user_info_response):
        requests_mock.get(f'https://bunpro.jp/api/user/{api_key}/study_queue',
                          json=mock_bad_user_info_response)
        client = BunproClient(api_key)

        with pytest.raises(SchemaError):
            client.study_queue()

    def test_study_queue_requested_info_parse_error(
            self, requests_mock, api_key, mock_bad_requested_info_response):
        requests_mock.get(f'https://bunpro.jp/api/user/{api_key}/study_queue',
                          json=mock_bad_requested_info_response)
        client = BunproClient(api_key)

        with pytest.raises(SchemaError):
            client.study_queue()

    def test_recent_items(self, requests_mock, api_key,
                          mock_recent_items_response, user_information,
                          grammar_point):
        requests_mock.get(f'https://bunpro.jp/api/user/{api_key}/recent_items',
                          json=mock_recent_items_response)
        client = BunproClient(api_key)
        r_user_info, r_requested_info = client.recent_items()

        assert r_user_info == user_information
        assert r_requested_info == [grammar_point]

    def test_recent_items_valid_limit(self, requests_mock, api_key,
                                      mock_recent_items_response,
                                      user_information, grammar_point):
        requests_mock.get(
            f'https://bunpro.jp/api/user/{api_key}/recent_items/1',
            json=mock_recent_items_response)
        client = BunproClient(api_key)
        r_user_info, r_requested_info = client.recent_items(limit=1)

        assert r_user_info == user_information
        assert r_requested_info == [grammar_point]

    def test_recent_items_negative_limit(self, api_key):
        client = BunproClient(api_key)
        with pytest.raises(ValueError):
            client.recent_items(limit=-10)

    def test_recent_items_large_limit(self, api_key):
        client = BunproClient(api_key)
        with pytest.raises(ValueError):
            client.recent_items(limit=100)

    def test_recent_items_user_info_parse_error(self, requests_mock, api_key,
                                                mock_bad_user_info_response):
        requests_mock.get(f'https://bunpro.jp/api/user/{api_key}/recent_items',
                          json=mock_bad_user_info_response)
        client = BunproClient(api_key)

        with pytest.raises(SchemaError):
            client.recent_items()

    def test_recent_items_requested_info_parse_error(
            self, requests_mock, api_key, mock_bad_requested_info_response):
        requests_mock.get(f'https://bunpro.jp/api/user/{api_key}/recent_items',
                          json=mock_bad_requested_info_response)
        client = BunproClient(api_key)

        with pytest.raises(SchemaError):
            client.recent_items()
