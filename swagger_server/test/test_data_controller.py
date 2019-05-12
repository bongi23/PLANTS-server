# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.data import Data  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDataController(BaseTestCase):
    """DataController integration test stubs"""

    def test_get_data(self):
        """Test case for get_data

        Get data of a plant
        """
        response = self.client.open(
            '/plants/{plant_id}/data'.format(plant_id=789, sensor='sensor_example', min_value=56, max_value=56, min_time=789, max_time=789),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
