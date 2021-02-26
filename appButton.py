from flask import Flask, Markup, render_template
import dynamo_sensor_db

app = Flask(__name__)

devices = [
    'Device 1'
]

blind_positions = [
    100, 0, 30, 25, 100, 100, 50
]

set_blind_position_values = [
    0, 25, 50, 75, 100
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
    blind_values = blind_positions
    time_values = times
    device_values = devices
    return render_template('test_data.html', max=100, positions=blind_values, times=time_values, devices=device_values, title='DEVICE DATA')

@app.route("/button")
def button():
    #set_blind_positions = set_blind_position_values
    return render_template('button.html')

if __name__ == '__main__':
    app.run()
