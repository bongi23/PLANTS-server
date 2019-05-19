# coding: utf-8

from __future__ import absolute_import

from flask import json
from swagger_server.test import BaseTestCase
from swagger_server.util import get_collection


class TestSinkController(BaseTestCase):
    """SinkController integration test stubs"""

    def test_add_plant(self):
        """Test case for add_plant

        Create a new plant
        """
        plant = {'microbit': 10, 'description': 'a plant', 'network': '127.0.0.1', 'sensors': ['thermo'], 'sink': True,
                 'connected': True}

        response = self.client.open(
            '/sink',
            method='PUT',
            data=json.dumps(plant),
            content_type='application/json')
        self.assert200(response)

        # inserting plant with same id
        plant = {'microbit': 10, 'description': 'a plant', 'network': '127.0.0.1', 'sensors': ['thermo'], 'sink': True,
                 'connected': True}

        response = self.client.open(
            '/sink',
            method='PUT',
            data=json.dumps(plant),
            content_type='application/json')
        self.assertStatus(response, status_code=200)

        get_collection('plants').delete_one({'microbit': 10})

    def test_set_values(self):
        """Test case for set_values

        Set the sensed values
        """
        # insert plant
        plant = {'microbit': 10, 'description': 'a plant', 'network': '127.0.0.1', 'sensors': ['thermo'], 'sink': True,
                 'connected': True}

        response = self.client.open(
            '/sink',
            method='PUT',
            data=json.dumps(plant),
            content_type='application/json')
        self.assert200(response)

        # inserting data for plant 10
        data = {'sensor': 'a sensor', 'timestamp': 0, 'microbit': 10, 'value': 10}

        response = self.client.open(
            '/sink/{plant_id}'.format(plant_id=10),
            method='POST',
            data=json.dumps(data),
            content_type='application/json')
        self.assert200(response)

        get_collection('data').delete_one({'microbit': 10})

        # deleting the plant
        get_collection('plants').delete_one({'microbit': 10})

        # inserting data for plant 10 (not existing)
        data = {'sensor': 'a sensor', 'timestamp': 0, 'microbit': 10, 'value': 10}
        response = self.client.open(
            '/sink/{plant_id}'.format(plant_id=10),
            method='POST',
            data=json.dumps(data),
            content_type='application/json')
        self.assert404(response)


if __name__ == '__main__':
    import unittest
    unittest.main()
