from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple, Optional
import logging

import pytz

import requests
from requests import HTTPError
from marshmallow import Schema, fields, post_load

# Because this is a library, we don't want to force logs on people if they
# don't configure logging themselves. This is why we have a null handler.
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


@dataclass
class UserInformation(object):
    """
    A Bunpro user's account information
    """
    username: str
    grammar_point_count: int
    ghost_review_count: int
    creation_date: datetime


@dataclass
class StudyQueue(object):
    """
    A Bunpro user's study queue
    """
    reviews_available: int
    next_review_date: datetime
    reviews_available_next_hour: int
    reviews_available_next_day: int


@dataclass
class GrammarPoint(object):
    """
    A single grammar point in Bunpro
    """
    grammar_point: str
    created_at_date: datetime
    updated_at_date: datetime


class SchemaError(Exception):
    """
    Raised when there is an error with a schema
    """
    def __init__(self, message: str, error: dict):
        """
        :param message: The error message to use
        :param error: A dictionary with errors
        """
        self.message = message
        self.error = error


class BunproAPIError(Exception):
    """
    Raised when there is an error returned from the Bunpro API
    """
    def __init__(self, error: HTTPError):
        """
        :param error: The original HTTPError
        """
        self._error = error

    @property
    def status_code(self) -> int:
        """
        The status code of the error response
        """
        return self._error.response.status_code

    @property
    def errors(self) -> List[str]:
        """
        The error messages returned form the Bunpro API
        """
        return [e.get('message')
                for e in self._error.response.json().get('errors', [])]


class Timestamp(fields.Field):
    """
    A converter field which converts to and from int timestamp/datetime
    All datetimes are in UTC timezone
    """

    def _serialize(self, value: datetime, attr: str, obj: object) -> float:
        """
        Converts a datetime value to a timestamp
        :param value: The value to serialize
        :param attr: The key on the object of the value
        :param obj: The object the value comes from
        :return: The value as a timestamp
        """
        return datetime.timestamp(value)

    def _deserialize(self, value: int, attr: str, data: dict) -> datetime:
        """
        Converts an integer timestamp to a datetime
        :param value: The value to deserialize
        :param attr: The key on the dict of the value
        :param data: The data dict
        :return: The value as a datetime
        """
        return datetime.fromtimestamp(value, tz=pytz.utc)


class UserInformationSchema(Schema):
    """
    Schema representing Bunpro account information
    """
    username = fields.Str(required=True)
    grammar_point_count = fields.Int(required=True)
    ghost_review_count = fields.Int(required=True)
    creation_date = Timestamp(required=True)

    @post_load
    def make_user_information(self, data: dict) -> UserInformation:
        """
        Converts the data dictionary to a UserInformation instance
        :param data: The loaded information
        :return: The UserInformation instance
        """
        return UserInformation(**data)


class StudyQueueSchema(Schema):
    """
    Schema representing a user's study queue
    """
    reviews_available = fields.Int(required=True)
    next_review_date = Timestamp(required=True)
    reviews_available_next_hour = fields.Int(required=True)
    reviews_available_next_day = fields.Int(required=True)

    @post_load
    def make_study_queue(self, data: dict) -> StudyQueue:
        """
        Converts the data dictionary to a StudyQueue instance
        :param data: The loaded information
        :return: The StudyQueue instance
        """
        return StudyQueue(**data)


class GrammarPointSchema(Schema):
    """
    Schema representing a grammar point
    """
    grammar_point = fields.String(required=True)
    created_at_date = Timestamp(required=True)
    updated_at_date = Timestamp(required=True)

    @post_load
    def make_grammar_point(self, data: dict) -> GrammarPoint:
        """
        Converts the data dictionary to a GrammarPoint instance
        :param data: The loaded information
        :return: The GrammarPoint instance
        """
        return GrammarPoint(**data)


class BunproClient(object):
    """
    Bunpro REST API Client
    """

    def __init__(self, api_key: str = None):
        """
        :param api_key: The Bunpro API key to use
        """
        self._base_url = 'https://bunpro.jp/api/user'

        self._user_base_url: Optional[str] = None

        if api_key:
            self._user_base_url = f'{self._base_url}/{api_key}'

        self._user_information_schema = UserInformationSchema()
        logger.debug('Initialized client with base url: %s',
                     self._user_base_url)

    def _get_base_url(self, api_key: str = None) -> str:
        """
        Determines the base URL to use
        :param api_key: The user's API key
        :return: The base API to use
        :raises ValueError: If there is no default API key and the user does
        not provide one.
        """
        if api_key:
            return f'{self._base_url}/{api_key}'
        elif self._user_base_url:
            return self._user_base_url
        else:
            raise ValueError('A Bunpro API key is required. '
                             'Please see https://www.bunpro.jp/api '
                             'for more info.')

    def study_queue(self, api_key: str = None) \
            -> Tuple[UserInformation, StudyQueue]:
        """
        Gets the user's study queue
        :param api_key: The API key to use

        :return: The user info and study queue
        :raises BunproAPIError: If there is an error response from the API
        :raises SchemaError: If the response cannot be parsed
        """
        base_url = self._get_base_url(api_key)
        url = f'{base_url}/study_queue'
        resp = requests.get(url)
        logger.debug('GET request to %s', url)

        try:
            resp.raise_for_status()
        except HTTPError as e:
            logger.error('API Error: %s', e)
            raise BunproAPIError(e)

        resp_json = resp.json()

        schema = StudyQueueSchema()

        user_info, user_error = self._user_information_schema.load(
            resp_json['user_information'])
        queue_info, queue_error = schema.load(
            resp_json['requested_information'])

        if user_error:
            logger.error('Error parsing user info: %s',
                         resp_json['user_information'])
            raise SchemaError('An error occurred parsing the user information',
                              user_error)
        elif queue_error:
            logger.error('Error parsing queue info: %s',
                         resp_json['requested_information'])
            raise SchemaError('An error occured parsing the queue information',
                              queue_error)

        return user_info, queue_info

    def recent_items(self, limit: int = None, api_key: str = None) \
            -> Tuple[UserInformation, List[GrammarPoint]]:
        """
        Gets the recently added grammer

        :param limit: The maximum number of items to return. 1 to 50 inclusive.
        :param api_key: The API key to use
        :return: The user information and recent grammar points
        :raises BunproAPIError: If there is an error response from the API
        :raises SchemaError: If the response cannot be parsed
        """
        if limit and (limit < 1 or limit > 50):
            raise ValueError('Limit must be 1 to 50 (inclusive)')

        base_url = self._get_base_url(api_key)
        url = f'{base_url}/recent_items'

        if limit:
            url += f'/{limit}'

        resp = requests.get(url)
        logger.debug('GET request to %s', url)

        try:
            resp.raise_for_status()
        except HTTPError as e:
            logger.error('API Error: %s', e)
            raise BunproAPIError(e)

        resp_json = resp.json()

        schema = GrammarPointSchema(many=True)

        user_info, user_error = self._user_information_schema.load(
            resp_json['user_information'])
        recent_info, recent_error = schema.load(
            resp_json['requested_information'])

        if user_error:
            logger.error('Error parsing user info: %s',
                         resp_json['user_information'])
            raise SchemaError('An error occurred parsing the user information',
                              user_error)
        elif recent_error:
            logger.error('Error parsing recent items info: %s',
                         resp_json['requested_information'])
            raise SchemaError('An error occured parsing the recent '
                              'items information', recent_error)

        return user_info, recent_info
