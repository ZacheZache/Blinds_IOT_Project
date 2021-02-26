import dynamo_sensor_db
import json

def main():
    devices = dynamo_sensor_db.get_all_devices('device_data')

    for device in devices:
        print(device)


if __name__ == '__main__':
    main()
