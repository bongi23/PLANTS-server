import connexion
import six

from swagger_server.models.plant import Plant  # noqa: E501
from swagger_server import util


def get_plant(plant_id):  # noqa: E501
    """Get info about a plant

    This can be done by 3rd party app # noqa: E501

    :param plant_id: id of a plant
    :type plant_id: int

    :rtype: Plant
    """
    return 'do some magic!'
