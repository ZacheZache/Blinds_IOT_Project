from flask import Flask, render_template, jsonify
import dynamo_sensor_db

app = Flask(__name__)

@app.route("/updated_data", methods=['GET'])
def updated_data():
    entries = dynamo_sensor_db.get_all_devices('enviroment_data')
    device_data = dynamo_sensor_db.get_all_devices('device_data')

    device_list = sorted(device_data, key=lambda k: k['Id'])
    new_list = sorted(entries, key=lambda k: k['Id'])
    newlist = new_list[-10:]
    devicelist = device_list[-10:]
    azimuth_values = []
    date_values = []
    blind_positions = []
    device_dates = []
    sun_in_win = []

    for pos in devicelist:
        newpos = pos['blind_position']
        blind_positions.append(newpos)

    for date in devicelist:
        time = date['date']
        device_dates.append(time)

    for date in newlist:
        time = date['date']
        date_values.append(time)
        sunStatus = date['sunInWin']
        if sunStatus:
            sun_in_win.append(360)
        else:
            sun_in_win.append(0)


    for az in newlist:
        azimuth = az['azimuth']
        azimuth_values.append(azimuth)

    device_values = newlist[0]['device_id']
    device_name = newlist[0]['device_name']

    return jsonify(render_template('data_display.html',  max=360, blind_max=100, blindpositions=blind_positions,
                           blind_dates=device_dates, positions=azimuth_values, data_description=device_name,
                           times=date_values, devices=device_values, sun_status=sun_in_win, title='DEVICE DATA'))

@app.route('/')
def index():
    return render_template('index.html')




@app.route("/dashboard")
def test_data():
    entries = dynamo_sensor_db.get_all_devices('enviroment_data')
    device_data = dynamo_sensor_db.get_all_devices('device_data')

    device_list = sorted(device_data, key=lambda k: k['Id'])
    new_list = sorted(entries, key=lambda k: k['Id'])
    newlist = new_list[-10:]
    devicelist = device_list[-10:]
    azimuth_values = []
    date_values = []
    blind_positions = []
    device_dates = []
    sun_in_win = []

    for pos in devicelist:
        newpos = pos['blind_position']
        blind_positions.append(newpos)

    for date in devicelist:
        time = date['date']
        device_dates.append(time)

    for date in newlist:
        time = date['date']
        date_values.append(time)
        sunStatus = date['sunInWin']
        if sunStatus:
            sun_in_win.append(360)
        else:
            sun_in_win.append(0)


    for az in newlist:
        azimuth = az['azimuth']
        azimuth_values.append(azimuth)

    device_values = newlist[0]['device_id']
    device_name = newlist[0]['device_name']

    return render_template('dashboard.html', max=360, blind_max=100, blindpositions=blind_positions,
                           blind_dates=device_dates, positions=azimuth_values, data_description=device_name,
                           times=date_values, devices=device_values, sun_status=sun_in_win, title='DEVICE DATA')


if __name__ == '__main__':
    app.run()
