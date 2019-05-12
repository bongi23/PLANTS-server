import connexion
from flask import abort
from swagger_server import util
from time import time


def add_plant(plant):  # noqa: E501
    """Create a new plant

    This can be done by the sink # noqa: E501

    :param plant: a plant object
    :type plant: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:

        new_plant = connexion.request.get_json()  # noqa: E501

        plants = util.get_collection("plants")
        if plants.find_one({"microbit": new_plant["microbit"]}) is not None:
            abort(409)

        plants.insert(new_plant)

        return 'Success'
    else:
        abort(400)


def set_values(plant_id, data=None):  # noqa: E501
    """Set the sensed values

    Set sensed value for the microbit with plant_id. # noqa: E501

    :param plant_id: 
    :type plant_id: int
    :param data: 
    :type data: list | bytes

    :rtype: None
    """
    if connexion.request.is_json:

        plants = util.get_collection('plants')
        if plants.find_one({'microbit': plant_id}) is None:
            abort(404)

        sensed_data = util.get_collection('data')
        data = [d for d in connexion.request.get_json()]  # noqa: E501

        for d in data:
            sensed_data.insert({'microbit': plant_id, 'data': d, 'time': time()})
        return 'Success'
    else:
        abort(400)
