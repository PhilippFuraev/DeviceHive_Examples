from devicehive import Handler
from devicehive import DeviceHive


class ReceiverHandler(Handler):

    def __init__(self, api, device_id='myPC-1',
                 accept_command_names=['LED ON', 'LED OFF']):
        Handler.__init__(self, api)
        self._device_id = device_id
        self._accept_command_names = accept_command_names
        self._device = None

    def handle_connect(self):
        self._device = self.api.put_device(self._device_id)
        self._device.subscribe_insert_commands(names=self._accept_command_names)
        self._device.subscribe_notifications()

    def handle_command_insert(self, command):
        print('Accept commands "%s"' % self._accept_command_names)
        command.status = 'accepted'
        command.save()

    def handle_notification(self, notification):
        print('Notification "%s" received' % notification.notification)
        led = mraa.Gpio(2)
        led.dir(mraa.DIR_OUT)
        if notification.notification[5:7] == 'on':
            self._device.data = {'LED': 'ON'}
            led.write(1)
            print("LED is ON!")
            self._device.save()
        else:
            if (notification.notification[5:8] == 'off'):
                self._device.data = {'TV': 'OFF'}
                led.write(0)
                print("LED is OFF")
                self._device.save()


url = 'http://192.168.31.82/api/rest'
refresh_token = 'eyJhbGciOiJIUzI1NiJ9.eyJwYXlsb2FkIjp7ImEiOlswXSwiZSI6MTU1ODAyNTQ4NDEyMywidCI6MCwidSI6MSwibiI6WyIqIl0sImR0IjpbIioiXX19.KcZn9s0PjyLvHY-jZ5xc2JKQnqZrqs1ky2oOtVJ4WgQ'
dh = DeviceHive(ReceiverHandler)
dh.connect(url, refresh_token=refresh_token)
