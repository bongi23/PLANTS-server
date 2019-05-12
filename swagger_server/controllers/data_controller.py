import connexion
import six

from swagger_server.models.data import Data  # noqa: E501
from swagger_server import util
from flask import abort


def get_data(plant_id, sensor, min_value, max_value, min_time, max_time):  # noqa: E501
    """Get data of a plant

    This can be done by 3rd party app # noqa: E501

    :param plant_id: id of a plant
    :type plant_id: int
    :param sensor: 
    :type sensor: str
    :param min_value: 
    :type min_value: int
    :param max_value: 
    :type max_value: int
    :param min_time: 
    :type min_time: int
    :param max_time: 
    :type max_time: int

    :rtype: List[Data]
    """
    plant = util.get_collection('plants').find_one({'microbit': plant_id})
    if plant is None:
        abort(404)
    query = dict()
    query['sensor'] = sensor

    if min_value > max_value or max_time < min_time:
        abort(400)

    elif min_value == 0 and max_value != 0:
        query['value'] = {'$lt': max_value}
    elif min_value != 0 and max_value == 0:
        query['value'] = {'$gt': min_value}
    elif min_value != 0 and max_value != 0:
        query['value'] = {'$and': [{'$lt': max_value}, {'$gt': min_value}]}

    if min_time == 0 and max_time > 0:
        query['time'] = {'$lt': max_value}
    elif min_time > 0 and max_value == 0:
        query['time'] = {'$gt': min_value}
    elif min_value != 0 and max_value != 0:
        query['time'] = {'$and': [{'$lt': max_value}, {'$gt': min_value}]}

    data = util.get_collection('data')
    res = []
    for d in data.find(query):
        del d['_id']
        res.append(d)
    return res
