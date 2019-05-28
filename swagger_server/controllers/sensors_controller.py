import requests
from swagger_server import util
from flask import abort


def update_sensing_time(microbit_id, sensor_name, sensing_time):

    plant = util.get_collection('plants').find_one({'microbit': microbit_id})

    if plant is None:
        abort(404)

    sink_address = plant['network']

    try:
        resp_code = requests.put(sink_address+'/sensing/{0}/{1}/time'.format(microbit_id, sensor_name),
                            params={'sampling_rate': sensing_time}).status_code
        print("Sensing "+str(resp_code))
    except Exception as e:
        resp_code = 500
        print(e)

    if resp_code == 200:
        sensors = util.get_collection('sensors')
        sensors.update_one({'$and': [{'microbit': microbit_id}, {'sensor': sensor_name}]},
                           {'$set': {'sampling_rate': sensing_time}})

    return resp_code


def get_sensors(microbit_id, sensor=None):

    sensors = util.get_collection('sensors')

    if sensor is not None:
        query = {'$and': [{'microbit': microbit_id}, {'sensor': sensor}]}
    else:
        query = {'microbit': microbit_id}

    res = []
    print(query)
    for s in sensors.find(query):
        del s['_id']
        res.append(s)

    return res


def put_sensors(plant_id, sensor_list):

    sensors_coll = util.get_collection('sensors')

    sensors = []
    for s in sensor_list:
        if sensors_coll.find_one({'$and': [{'microbit': plant_id}, {'sensor': s}]}) is None:
            sensors.append({
                'sensor': s,
                'microbit': plant_id,
                'sampling_rate': 1000
            })
    if len(sensors) > 0:
        sensors_coll.insert_many(sensors)
