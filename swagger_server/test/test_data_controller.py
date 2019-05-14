# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.data import Data  # noqa: E501
from swagger_server.test import BaseTestCase
from swagger_server.util import get_collection


class TestDataController(BaseTestCase):
    """DataController integration test stubs"""

    def test_get_data(self):
        """Test case for get_data

        Get data of a plant
        """
        pass


if __name__ == '__main__':
    import unittest
    get_collection('plants').delete_many({})
    get_collection('events').delete_many({})
    get_collection('data').delete_many({})
    unittest.main()
