import connexion

from swagger_server import util
from flask import abort, make_response
import requests
from threading import Lock

event_counter = 0
event_counter_lock = Lock()


def subscribe(microbit_id, event):  # noqa: E501
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

        plant = util.get_collection('plants').find_one({'microbit': microbit_id})

        if microbit_id != event['microbit']:
            print('Microbit gone')
            abort(400)

        if plant is None:
            abort(404)

        with event_counter_lock:
            global event_counter
            event_counter += 1
            tmp = event_counter

        events = util.get_collection('events')
        event['id'] = tmp
        try:
            resp = requests.put(plant['network']+'/sensing/{0}/{1}'.format(microbit_id, tmp), params=event['data'])
        except Exception as e:
            print(e)
            resp = None

        if resp is not None and resp.status_code == 200:
            events.insert_one(event)

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

    evt = events.find_one({'id': int(event_id)})
    if evt is None:
        abort(404)

    plant = plants.find_one({'microbit': evt['microbit']})
    try:
        resp = requests.delete(plant['network']+'/sensing/{0}/{1}'.format(plant['microbit'], evt['id']))
        print('Delete event response code:' + str(resp.status_code))
    except Exception as e:
        print("Exception in delete event:" + str(e))

    if resp.status_code == 200 or resp.status_code == 410:
        events.delete_one({'id': event_id})

    return 'Success'


def get_event(microbit_id, sensor=None):

    events = util.get_collection('events')

    res = []
    if sensor is not None:
        query = {'$and': [{'microbit': microbit_id}, {'data.sensor': sensor}]}
    else:
        query = {'microbit': microbit_id}

    for evt in events.find(query):
        del evt['_id']
        res.append(evt)

    return res
