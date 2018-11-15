from devicehive import DeviceHiveApi

url = 'http://192.168.31.82/api/rest'
refresh_token = 'eyJhbGciOiJIUzI1NiJ9.eyJwYXlsb2FkIjp7ImEiOlswXSwiZSI6MTU1ODAyNTQ4NDEyMywidCI6MCwidSI6MSwibiI6WyIqIl0sImR0IjpbIioiXX19.KcZn9s0PjyLvHY-jZ5xc2JKQnqZrqs1ky2oOtVJ4WgQ'
device_hive_api = DeviceHiveApi(url, refresh_token=refresh_token)
device_hive_api = DeviceHiveApi(url, refresh_token=refresh_token)
device_id = 'myPC-1'
device = device_hive_api.put_device(device_id)
device.name = 'myPC'
device.data = {'key': 'value'}
device.save()
devices = device_hive_api.list_devices()
for device in devices:
    print('Device: %s, name: %s, data: %s' % (device.id, device.name,
                                              device.data))
    # device.remove()
