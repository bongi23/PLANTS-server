from swagger_server import util
from flask import abort
import requests


def get_plant(plant_id):  # noqa: E501
    """Get info about a plant
    This can be done by 3rd party app # noqa: E501
    :param plant_id: id of a plant
    :type plant_id: int
    :rtype: Plant
    """
    plants = util.get_collection('plants')
    p = plants.find_one({'microbit': plant_id})

    if p is None:
        abort(404)
    del p['_id']

    return p


def get_plants():  # noqa: E501
    """Get all the known plants
    This can be done by 3rd party app # noqa: E501
    :rtype: List[Plant]
    """

    """all_plants = util.get_collection('plants').find({})
    res = []
    for p in all_plants:
        del p['_id']
        res.append(p)
    return res"""

    all_plants = util.get_collection('plants').find({})
    res = []
    for p in all_plants:
        del p['_id']
        res.append(p)
    return res
