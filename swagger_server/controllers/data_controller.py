import connexion
import six

from swagger_server.models.data import Data  # noqa: E501
from swagger_server.models.filter import Filter  # noqa: E501
from swagger_server import util


def get_data(plant_id, filter=None):  # noqa: E501
    """Get data of a plant

    This can be done by 3rd party app # noqa: E501

    :param plant_id: id of a plant
    :type plant_id: int
    :param filter: filters for data
    :type filter: dict | bytes

    :rtype: List[Data]
    """
    if connexion.request.is_json:
        filter = Filter.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
