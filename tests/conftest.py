from datetime import datetime

import pytest

from pybunpro import UserInformation, StudyQueue, GrammarPoint


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


@pytest.fixture
def grammar_point_item():
    return 'でも'


@pytest.fixture
def created_at_date():
    return datetime(2019, 5, 11)


@pytest.fixture
def created_at_date_ts(created_at_date):
    return datetime.timestamp(created_at_date)


@pytest.fixture
def updated_at_date():
    return datetime(2019, 5, 11)


@pytest.fixture
def updated_at_date_ts(updated_at_date):
    return datetime.timestamp(updated_at_date)


@pytest.fixture
def grammar_point(grammar_point_item,
                  created_at_date, updated_at_date):
    return GrammarPoint(grammar_point_item, created_at_date,
                        updated_at_date)


@pytest.fixture
def grammar_point_dict(grammar_point_item, created_at_date_ts,
                       updated_at_date_ts):
    return dict(grammar_point=grammar_point_item,
                created_at_date=created_at_date_ts,
                updated_at_date=updated_at_date_ts)
