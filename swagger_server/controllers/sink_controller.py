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
        plant = Plant.from_dict(connexion.request.get_json())  # noqa: E501
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
        plants = util.get_collection('plants')
        if plants.find_one({'microbit': plant_id}) is None:
            abort(404)
        data = connexion.request.get_json()  # noqa: E501
        data_coll = util.get_collection('data')
        data_coll.insert_one(data)

        result = add_together.delay(23, 42)
        result.wait()  # 65
    return 'do some magic!'


@celery.task()
def add_together(a, b):
    print('ciao')
    return a + b
