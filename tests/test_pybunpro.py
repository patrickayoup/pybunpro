import pytest

from click.testing import CliRunner

from pybunpro.__main__ import cli


class TestPyBunpro(object):

    @pytest.fixture
    def runner(self):
        return CliRunner()

    def test_study_queue(self, requests_mock, api_key, runner,
                         mock_study_queue_response,
                         user_information,
                         study_queue):
        requests_mock.get(f'https://bunpro.jp/api/user/{api_key}/study_queue',
                          json=mock_study_queue_response)

        result = runner.invoke(cli, ['--api-key', api_key,
                                     'study-queue'])
        assert result.exit_code == 0
        assert str(user_information) in result.output
        assert str(study_queue) in result.output

    def test_study_queue_error(self, requests_mock, api_key, runner,
                               error_response):
        requests_mock.get(f'https://bunpro.jp/api/user/{api_key}/study_queue',
                          json=error_response, status_code=400)

        result = runner.invoke(cli, ['--api-key', api_key,
                                     'study-queue'])
        assert result.exit_code == 1
        assert 'User does not exist' in result.output

    def test_recent_items(self, requests_mock, api_key, runner,
                          mock_recent_items_response,
                          user_information,
                          grammar_point):
        requests_mock.get(f'https://bunpro.jp/api/user/{api_key}/recent_items',
                          json=mock_recent_items_response)

        result = runner.invoke(cli, ['--api-key', api_key,
                                     'recent-items'])
        assert result.exit_code == 0
        assert str(user_information) in result.output
        assert str([grammar_point]) in result.output

    def test_recent_items_error(self, requests_mock, api_key, runner,
                                error_response):
        requests_mock.get(f'https://bunpro.jp/api/user/{api_key}/recent_items',
                          json=error_response, status_code=400)

        result = runner.invoke(cli, ['--api-key', api_key,
                                     'recent-items'])
        assert result.exit_code == 1
        assert 'User does not exist' in result.output

    def test_debug_mode(self, requests_mock, api_key, runner,
                        mock_recent_items_response,
                        user_information,
                        grammar_point,
                        caplog):
        requests_mock.get(f'https://bunpro.jp/api/user/{api_key}/recent_items',
                          json=mock_recent_items_response)

        result = runner.invoke(cli, ['--api-key', api_key,
                                     '--debug',
                                     'recent-items'])
        assert result.exit_code == 0
        assert 'Debug Mode Enabled' in caplog.text
