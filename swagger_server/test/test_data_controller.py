# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.data import Data  # noqa: E501
from swagger_server.test import BaseTestCase
from swagger_server.util import get_collection
from time import time


class TestDataController(BaseTestCase):
    """DataController integration test stubs"""

    def test_get_data(self):
        """Test case for get_data

        Get data of a plant
        """
        plant = {'microbit': 10, 'description': 'a plant', 'network': 1, 'sensors': ['thermo'], 'sink': True,
                 'connected': True}

        response = self.client.open(
            '/sink',
            method='PUT',
            data=json.dumps(plant),
            content_type='application/json')
        self.assert200(response)

        data = []

        before = time()

        for i in range(10):
            data_sensed = {'microbit': 10, 'sensor': 'thermometer', 'value': 20+i, 'timestamp': time()}
            data.append(data_sensed)

        after = time()

        for d in data:
            get_collection('data').insert(d)
            del d['_id']

        query_string = [('sensor', 'thermometer'),
                        ('min_value', 20),
                        ('max_value', 30)]

        response = self.client.open(
            '/plants/{plant_id}/data'.format(plant_id=10),
            method='GET',
            query_string=query_string)
        self.assert200(response)
        for d in data:
            self.assertIn(d, response.json)

        query_string = [('sensor', 'thermometer'),
                        ('min_time', before),
                        ('max_time', after)]

        response = self.client.open(
            '/plants/{plant_id}/data'.format(plant_id=10),
            method='GET',
            query_string=query_string)
        self.assert200(response)
        for d in data:
            self.assertIn(d, response.json)

        response = self.client.open(
            '/plants/{plant_id}/data'.format(plant_id=10),
            method='GET',
            query_string=[])
        self.assert200(response)
        for d in data:
            self.assertIn(d, response.json)

        get_collection('plants').delete_one({'microbit': 10})
        get_collection('data').delete_many({'microbit': 10})


if __name__ == '__main__':
    import unittest
    unittest.main()
