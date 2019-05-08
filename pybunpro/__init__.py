from dataclasses import dataclass
from datetime import datetime

import requests
from marshmallow import Schema, fields, post_load


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


class Timestamp(fields.Field):
    """
    A converter field which converts to and from int timestamp/datetime
    """

    def _serialize(self, value: datetime, attr: str, obj) -> int:
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
        return datetime.fromtimestamp(value)


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


class BunproClient(object):

    def __init__(self, api_key: str):
        """
        :param api_key: The Bunpro API key to use
        :raises TypeError: If the provided API key is None
        """
        if not api_key:
            raise TypeError('A Bunpro API key is required. '
                            'Please see https://www.bunpro.jp/api '
                            'for more info.')
        self._api_key = api_key
        self._base_url = f'https://bunpro.jp/api/user/{self._api_key}'
        self._user_information_schema = UserInformationSchema()

    def study_queue(self):
        """
        Gets the user's study queue
        :return: The user info and study queue
        """
        url = f'{self._base_url}/study_queue'
        resp = requests.get(url)
        resp_json = resp.json()

        schema = StudyQueueSchema()

        user_info, user_error = self._user_information_schema.load(
            resp_json['user_information'])
        queue_info, queue_error = schema.load(
            resp_json['requested_information'])

        if user_error:
            raise SchemaError('An error occurred parsing the user information',
                              user_error)
        elif queue_error:
            raise SchemaError('An error occured parsing the queue information',
                              queue_error)

        return user_info, queue_info
