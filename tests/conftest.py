from datetime import datetime

import pytest

from pybunpro import UserInformation, StudyQueue


@pytest.fixture
def username():
    return 'username'


@pytest.fixture
def grammar_point_count():
    return 10


@pytest.fixture
def ghost_review_count():
    return 2


@pytest.fixture
def creation_date():
    return datetime(2017, 12, 25, 21, 3, 51)


@pytest.fixture
def creation_date_ts(creation_date):
    return datetime.timestamp(creation_date)


@pytest.fixture
def user_information(username, grammar_point_count,
                     ghost_review_count, creation_date):
    return UserInformation(username, grammar_point_count,
                           ghost_review_count, creation_date)


@pytest.fixture
def user_information_dict(username, grammar_point_count,
                          ghost_review_count, creation_date_ts):
    return dict(username=username, grammar_point_count=grammar_point_count,
                ghost_review_count=ghost_review_count,
                creation_date=creation_date_ts)


@pytest.fixture
def reviews_available():
    return 7


@pytest.fixture
def next_review_date_ts():
    return 1557279000


@pytest.fixture
def next_review_date(next_review_date_ts):
    return datetime.fromtimestamp(next_review_date_ts)


@pytest.fixture
def reviews_available_next_hour():
    return 8


@pytest.fixture
def reviews_available_next_day():
    return 12


@pytest.fixture
def study_queue(reviews_available, next_review_date,
                reviews_available_next_hour, reviews_available_next_day):
    return StudyQueue(reviews_available, next_review_date,
                      reviews_available_next_hour,
                      reviews_available_next_day)

@pytest.fixture
def study_queue_dict(reviews_available, next_review_date_ts,
                     reviews_available_next_hour, reviews_available_next_day):
    return dict(reviews_available=reviews_available,
                next_review_date=next_review_date_ts,
                reviews_available_next_hour=reviews_available_next_hour,
                reviews_available_next_day=reviews_available_next_day)
