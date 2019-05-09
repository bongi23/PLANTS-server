import connexion
import six

from swagger_server.models.data import Data  # noqa: E501
from swagger_server.models.plant import Plant  # noqa: E501
from swagger_server import util


def add_plant(plant):  # noqa: E501
    """Create a new plant

    This can be done by the sink # noqa: E501

    :param plant: a plant object
    :type plant: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        plant = Plant.from_dict(connexion.request.get_json())  # noqa: E501
        util.get_db().plants.insert(plant.to_dict())
    return 'do some magic!'


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
        data = [Data.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'
