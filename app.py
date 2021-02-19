from flask import Flask, render_template
import dynamo_sensor_db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/dashboard")
def get_dashboard():
    devices = dynamo_sensor_db.get_all_devices()
    return render_template('dashboard.html', devices=devices)


if __name__ == '__main__':
    app.run()
