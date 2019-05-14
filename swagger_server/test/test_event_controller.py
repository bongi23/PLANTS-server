# coding: utf-8

from __future__ import absolute_import

from flask import json
from swagger_server.test import BaseTestCase
from swagger_server.util import get_collection
from flask_pymongo import ObjectId


class TestEventController(BaseTestCase):
    """EventController integration test stubs"""

    def test_subscribe(self):
        """Test case for subscribe

        Register to sensors' event
        """
        id = 423569
        plant = {'microbit': id, 'description': 'a plant', 'network': 1}

        response = self.client.open(
            '/sink',
            method='PUT',
            data=json.dumps(plant),
            content_type='application/json')
        self.assert200(response)

        event = {
            "data": {
                "frequency": 0,
                "max_value": 0,
                "min_value": 0,
                "sensor": "string"
            },
            "microbit": id,
            "return_address": "string"
        }

        response = self.client.open(
            '/plants/{plant_id}/event'.format(plant_id=id),
            method='PUT',
            data=json.dumps(event),
            content_type='application/json')
        self.assert200(response)

        event_id = response.json['event_id']

        response = self.client.open(
            '/plants/{plant_id}/event'.format(plant_id=id+1),
            method='PUT',
            data=json.dumps(event),
            content_type='application/json')
        self.assertStatus(response, status_code=400)

        get_collection('plants').delete_one({'microbit': id})

        response = self.client.open(
            '/plants/{plant_id}/event'.format(plant_id=id),
            method='PUT',
            data=json.dumps(event),
            content_type='application/json')
        self.assert404(response)

        get_collection('events').delete_one({'_id': ObjectId(event_id)})

    def test_unsubscribe(self):
        """Test case for unsubscribe

        Unregister to sensors' event
        """
        id = 423569
        plant = {'microbit': id, 'description': 'a plant', 'network': 1}

        response = self.client.open(
            '/sink',
            method='PUT',
            data=json.dumps(plant),
            content_type='application/json')
        self.assert200(response)

        event = {
            "data": {
                "frequency": 0,
                "max_value": 0,
                "min_value": 0,
                "sensor": "string"
            },
            "microbit": id,
            "return_address": "string"
        }

        response = self.client.open(
            '/plants/{plant_id}/event'.format(plant_id=id),
            method='PUT',
            data=json.dumps(event),
            content_type='application/json')
        self.assert200(response)

        event_id = response.json['event_id']

        response = self.client.open(
            '/plants/event/{event_id}'.format(event_id=event_id),
            method='DELETE')
        self.assert200(response)

        self.assertEqual(None, get_collection('events').find_one({'_id': ObjectId(event_id)}))


if __name__ == '__main__':
    import unittest
    get_collection('plants').delete_many({})
    get_collection('events').delete_many({})
    get_collection('data').delete_many({})
    unittest.main()
