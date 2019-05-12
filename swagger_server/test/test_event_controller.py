# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.event20parameter import Event20parameter  # noqa: E501
from swagger_server.test import BaseTestCase


class TestEventController(BaseTestCase):
    """EventController integration test stubs"""

    def test_subscribe(self):
        """Test case for subscribe

        Register to sensors' event
        """
        event = Event20parameter()
        response = self.client.open(
            '/subscribe/{plant_id}'.format(plant_id=789),
            method='POST',
            data=json.dumps(event),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_unsubscribe(self):
        """Test case for unsubscribe

        Unregister to sensors' event
        """
        response = self.client.open(
            '/unsubscribe/{plant_id}'.format(plant_id=789),
            method='PUT')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
