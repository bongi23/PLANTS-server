import connexion
import six

from swagger_server.models.event_parameter import EventParameter  # noqa: E501
from swagger_server import util


def subscribe(plant_id, event=None):  # noqa: E501
    """Register to sensors&#39; event

    This can be done by 3rd party app # noqa: E501

    :param plant_id: id of a plant
    :type plant_id: int
    :param event: event detail
    :type event: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        event = EventParameter.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def unsubscribe(plant_id):  # noqa: E501
    """Unregister to sensors&#39; event

    This can be done by 3rd party app # noqa: E501

    :param plant_id: id of a plant
    :type plant_id: int

    :rtype: None
    """
    return 'do some magic!'
