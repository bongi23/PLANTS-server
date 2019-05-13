import connexion

from swagger_server.models.data import Data  # noqa: E501
from swagger_server.models.plant import Plant  # noqa: E501
from swagger_server import util
from flask import abort, current_app , g
from celery import Celery


def make_celery():
    celery = Celery(
        __name__,
        backend='redis://localhost:6379',
        broker='redis://localhost:6379'
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

    plants = util.get_collection('plants')
    if plants.find({'microbit':plant['microbit']}) is not None:
        abort(409)

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
        data = connexion.request.get_json()  # noqa: E501
        data_coll = util.get_collection('data')
        data_coll.insert_one(data)

        check_event.delay(data)
    return 'Success'


@celery.task()
def notify(address):
    pass


@celery.task()
def check_event(data):
    events = util.get_collection('events').find({'microbit': data['microbit']})
    match_value = False
    match_time = False

    for e in events:
        if data['sensor'] == e['sensor']:
            if hasattr(e, 'min_value') and hasattr(e, 'max_value'):
                if e['min_value'] <= data['value'] <= e['max_value']:
                    match_value = True
            elif hasattr(e, 'min_value'):
                if e['min_value'] <= data['value']:
                    match_value = True
            elif hasattr(e, 'max_value'):
                if e['max_value'] >= data['value']:
                    match_value = True
            else:
                match_value = True

            if hasattr(e, 'min_time') and hasattr(e, 'max_time'):
                if e['min_time'] <= data['timestamp'] <= e['max_time']:
                    match_time = True
            elif hasattr(e, 'min_time'):
                if e['min_time'] <= data['timestamp']:
                    match_time = True
            elif hasattr(e, 'max_time'):
                if e['max_time'] >= data['timestamp']:
                    match_time = True
            else:
                match_time = True

            if hasattr(e, 'op'):
                if e['op'] == 'or':
                    res = match_value or match_time
            else:
                res = match_value and match_time

            if res:
                notify.delay(e['return_address'], data)
