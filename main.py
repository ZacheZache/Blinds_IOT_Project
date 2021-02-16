import dynamo_sensor_db
import json

def main():
    dynamo_sensor_db.store_device_entry('Blind1', '100', 'Active')


if __name__ == '__main__':
    main()
