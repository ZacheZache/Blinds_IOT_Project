from flask import Flask, Markup, render_template
import dynamo_sensor_db
import json

app = Flask(__name__)

devices = [
    'Device 1'
]

blind_positions = [
    100, 0, 30, 25, 100, 100, 50
]

times = [
    1, 2, 3, 4, 5, 6, 7
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/dashboard")
def get_dashboard():
    devices = dynamo_sensor_db.get_all_devices('temp_data_test')
    for device in devices:
        print(device)
    return render_template('dashboard.html', devices=devices)


@app.route("/test_data")
def test_data():
    entries = dynamo_sensor_db.get_all_devices('enviroment_data')
    device_data = dynamo_sensor_db.get_all_devices('device_data')
    devicelist = sorted(device_data, key=lambda k: k['Id'])
    newlist = sorted(entries, key=lambda k: k['Id'])
    azimuth_values = []
    date_values = []
    blind_positions = []
    device_dates = []

    for pos in devicelist:
        newpos = pos['blind_position']
        blind_positions.append(newpos)

    for date in devicelist:
        time = date['date']
        device_dates.append(time)

    for date in newlist:
        time = date['date']
        date_values.append(time)

    for az in newlist:
        azimuth = az['azimuth']
        azimuth_values.append(azimuth)

    device_values = newlist[0]['device_id']
    device_name = newlist[0]['device_name']

    return render_template('test_data.html', max=360, blind_max=100, blindpositions=blind_positions,
                           blind_dates=device_dates, positions=azimuth_values, data_description=device_name,
                           times=date_values, devices=device_values, title='DEVICE DATA')


if __name__ == '__main__':
    app.run()
