# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.data import Data  # noqa: E501
from swagger_server.models.plant import Plant  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSinkController(BaseTestCase):
    """SinkController integration test stubs"""

    def test_add_plant(self):
        """Test case for add_plant

        Create a new plant
        """
        plant = Plant()
        response = self.client.open(
            '/sink',
            method='PUT',
            data=json.dumps(plant),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_set_values(self):
        """Test case for set_values

        Set the sensed values
        """
        data = [Data()]
        response = self.client.open(
            '/sink/{plant_id}'.format(plant_id=789),
            method='POST',
            data=json.dumps(data),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
