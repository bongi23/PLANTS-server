from swagger_server import util
from flask import abort
import pymongo


def get_data(plant_id, sensor=None, min_value=None, max_value=None, min_time=None, max_time=None):  # noqa: E501
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

    Result is a list of json like:

    {
        sensor: string
        value: int
        time: int
    }

    """
    plant = util.get_collection('plants').find_one({'microbit': plant_id})
    if plant is None:
        abort(404)
    query = dict()
    query['$and'] = []
    query['$and'].append({'microbit': plant_id})

    if sensor is not None:
        query['$and'].append({'sensor': sensor})

        if min_value is not None and max_value is not None:
            if min_value > max_value:
                abort(400)

        if max_value is not None:
            query['$and'].append({'value': {'$lte': max_value}})
        if min_value is not None:
            query['$and'].append({'value': {'$gte': min_value}})

        if min_time is not None and max_time is not None:
            if min_time > max_time:
                abort(400)

        if max_time is not None:
            query['$and'].append({'timestamp': {'$lte': max_time}})
        if min_time is not None:
            query['$and'].append({'timestamp': {'$gte': min_time}})

    data = util.get_collection('data')
    res = []
    for d in data.find(query).limit(10).sort('timestamp', pymongo.DESCENDING):
        del d['_id']
        res.append(d)
    return res
