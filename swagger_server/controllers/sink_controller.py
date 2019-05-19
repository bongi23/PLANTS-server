import connexion
from swagger_server import util
from flask import abort
from celery import Celery
import os

REDIS = os.environ['REDIS']


def make_celery():
    celery = Celery(
        __name__,
        backend=REDIS,
        broker=REDIS
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery()


def add_plant(plant):  # noqa: E501
    """Create a new plant

    This can be done by the sink # noqa: E501

    :param plant: a plant object
    :type plant: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        plant = connexion.request.get_json()  # noqa: E501
    plant['network'] = connexion.request.remote_addr

    plants = util.get_collection('plants')
    if plants.find_one({'microbit': plant['microbit']}) is not None:
        plants.update_one({'microbit': plant['microbit']}, {"$set": plant})
        return 'Success'

    plants.insert_one(plant)

    return 'Success'


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
        if data['microbit'] != plant_id:
            abort(400)

        data = connexion.request.get_json()  # noqa: E501
        data_coll = util.get_collection('data')
        data_coll.insert_one(data)
        del data['_id']

        events = []
        for e in util.get_collection('events').find({'microbit': data['microbit']}):
            del e['_id']
            events.append(e)

        check_event.delay(data, events)
    return 'Success'


@celery.task()  # pragma: no cover
def notify(address):  # pragma no cover
    print('notify')
    pass


@celery.task()  # pragma: no cover
def check_event(data, events):  # pragma: no cover
        match_value = False

        for e in events:
            event_param = e['data']

            if hasattr(event_param, 'sensor') is False:
                notify.delay(data)

            elif data['sensor'] == event_param['sensor']:
                if hasattr(event_param, 'min_value') and hasattr(event_param, 'max_value'):
                    if event_param['min_value'] <= data['value'] <= event_param['max_value']:
                        match_value = True
                elif hasattr(event_param, 'min_value'):
                    if event_param['min_value'] <= data['value']:
                        match_value = True
                elif hasattr(event_param, 'max_value'):
                    if event_param['max_value'] >= data['value']:
                        match_value = True
                else:
                    match_value = True

                if match_value:
                    notify.delay(e['return_address'], data)
