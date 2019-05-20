import connexion

from swagger_server import util
from flask import abort
import requests

event_counter = 0


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
            print('qua')
            abort(400)

        if plant is None:
            abort(404)

        global event_counter
        event_counter += 1

        events = util.get_collection('events')
        event['id'] = event_counter
        events.insert_one(event)

        resp = requests.put(plant['network']+'/sensing/{0}/{1}'.format(plant_id, event_counter), params=event['data'])
        print(resp.url)

    return {'event_id': event_counter}


def unsubscribe(event_id):  # noqa: E501
    """Unregister to sensors&#39; event

    This can be done by 3rd party app # noqa: E501

    :param event_id: 
    :type event_id: str

    :rtype: None
    """
    events = util.get_collection('events')
    plants = util.get_collection('plants')

    evt = events.find_one({'id': event_id})
    if evt is None:
        abort(404)

    plant = plants.find_one({'microbit': evt['microbit']})
    resp = requests.delete(plant['network']+'/sensing/{0}/{1}'.format(plant['microbit'], event_counter))

    print(resp)

    events.delete_one({'id': event_id})

    return 'Success'
