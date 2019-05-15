import connexion
from swagger_server import util
from flask import abort
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
    if plants.find_one({'microbit': plant['microbit']}) is not None:
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
        if data['microbit'] != plant_id:
            abort(400)

        data = connexion.request.get_json()  # noqa: E501
        data_coll = util.get_collection('data')
        data_coll.insert_one(data)
        del data['_id']

        check_event.delay(data)
    return 'Success'


@celery.task()  # pragma: no cover
def notify(address):  # pragma no cover
    pass


@celery.task()  # pragma: no cover
def check_event(data):  # pragma: no cover
    events = util.get_collection('events').find({'microbit': data['microbit']})
    match_value = False

    for e in events:
        if data['sensor'] == e['sensor']:
            e = e['data']
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

            if match_value:
                notify.delay(e['return_address'], data)
