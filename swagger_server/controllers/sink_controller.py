import connexion
from swagger_server import util
from flask import abort
from swagger_server.controllers.sensors_controller import put_sensors
from swagger_server.workers import check_event


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
        plants.update_one({'microbit': plant['microbit']}, {"$set": plant})
        if hasattr(plant, 'sensors'):
            put_sensors(plant['microbit'], plant['sensors'])
        return 'Success'
    print(plant)
    plants.insert_one(plant)
    put_sensors(plant['microbit'], plant['sensors'])

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

        if len(events) != 0:
            check_event.delay(data, events)
    return 'Success'
