# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.plant import Plant  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPlantsController(BaseTestCase):
    """PlantsController integration test stubs"""

    def test_get_plant(self):
        """Test case for get_plant

        Get info about a plant
        """
        response = self.client.open(
            '/plants/{plant_id}'.format(plant_id=789),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
