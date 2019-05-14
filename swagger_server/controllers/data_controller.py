from swagger_server import util
from flask import abort


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

    query['microbit'] = plant_id

    if sensor is not None:
        query['sensor'] = sensor

        if min_value is None and max_value is not None:
            query['value'] = {'$lt': max_value}
        elif min_value is not None and max_value is None:
            query['value'] = {'$gt': min_value}
        if min_value is not None and max_value is not None:
            if min_value > max_value:
                abort(400)
            else:
                query['value'] = {'$and': [{'$lt': max_value}, {'$gt': min_value}]}

        if min_time is None and max_time is not None:
            query['timestamp'] = {'$lt': max_time}
        elif min_time is not None and max_time is None:
            query['timestamp'] = {'$gt': min_time}
        if min_time is not None and max_time is not None:
            if min_time > max_time:
                abort(400)
            else:
                query['timestamp'] = {'$and': [{'$lt': max_time}, {'$gt': min_time}]}

    data = util.get_collection('data')
    res = []
    for d in data.find(query).limit(10):
        del d['_id']
        res.append(d)
    return res
