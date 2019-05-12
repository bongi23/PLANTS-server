# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.data import Data  # noqa: E501
from swagger_server.models.filter import Filter  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDataController(BaseTestCase):
    """DataController integration test stubs"""

    def test_get_data(self):
        """Test case for get_data

        Get data of a plant
        """
        filter = Filter()
        response = self.client.open(
            '/data/{plant_id}'.format(plant_id=789),
            method='GET',
            data=json.dumps(filter),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
