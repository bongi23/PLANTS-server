import connexion

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util
from flask import abort
from flask_pymongo import ObjectId


def subscribe(plant_id, event):  # noqa: E501
    """Register to sensors&#39; event

    This can be done by 3rd party app # noqa: E501

    :param plant_id: id of a plant
    :type plant_id: int
    :param event: event detail
    :type event: dict | bytes

    :rtype: InlineResponse200
    """
    if connexion.request.is_json:
        event = connexion.request.get_json()  # noqa: E501

        plant = util.get_collection('plants').find_one({'microbit': plant_id})

        if plant_id != event['microbit']:
            abort(400)

        if plant is None:
            abort(404)
        events = util.get_collection('events')
        event_id = events.insert_one(event)

        # TODO
        # inviare i dati relativi all'evento al sink

    return {'event_id': str(event_id.inserted_id)}


def unsubscribe(event_id):  # noqa: E501
    """Unregister to sensors&#39; event

    This can be done by 3rd party app # noqa: E501

    :param event_id: 
    :type event_id: str

    :rtype: None
    """
    events = util.get_collection('events')

    if(events.find_one({'_id': ObjectId(event_id)})) is None:
        abort(404)

    events.delete_one({'_id': ObjectId(event_id)})

    return 'Success'
