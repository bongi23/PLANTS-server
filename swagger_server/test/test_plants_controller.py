# coding: utf-8

from __future__ import absolute_import
from swagger_server.test import BaseTestCase
from flask import json
from swagger_server.util import get_collection


class TestPlantsController(BaseTestCase):
    """PlantsController integration test stubs"""

    def test_get_plant(self):
        """Test case for get_plant

        Get info about a plant
        """
        plant = {'microbit': 10, 'description': 'a plant', 'network': 1, 'sensors': ['thermo'], 'sink': True,
                 'connected': True}

        response = self.client.open(
            '/sink',
            method='PUT',
            data=json.dumps(plant),
            content_type='application/json')
        self.assert200(response)

        response = self.client.open(
            '/plants/{plant_id}'.format(plant_id=10),
            method='GET',
            content_type='application/json')
        self.assert200(response)
        self.assertDictEqual(plant, response.json)

        get_collection('plants').delete_one({'microbit': 10})

        response = self.client.open(
            '/plants/{plant_id}'.format(plant_id=11),
            method='GET',
            content_type='application/json')
        self.assert404(response)

    def test_get_plants(self):
        """Test case for get_plants

        Get all the known plants
        """

        plants = []

        for i in range(5):
            plant = {'microbit': i, 'description': 'a plant', 'network': 1, 'sensors': ['thermo'], 'sink': True,
                     'connected': True}
            plants.append(plant)

            response = self.client.open(
                '/sink',
                method='PUT',
                data=json.dumps(plant),
                content_type='application/json')
            self.assert200(response)

        response = self.client.open(
            '/plants',
            method='GET')
        self.assert200(response)
        self.assertListEqual(plants, response.json)

        for i in range(5):
            get_collection('plants').delete_one({'microbit': i})


if __name__ == '__main__':
    import unittest
    unittest.main()
