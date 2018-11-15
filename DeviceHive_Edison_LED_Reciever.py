from devicehive import Handler
from devicehive import DeviceHive
import mraa


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
        if notification.notification[4:6] == 'ON':
            self._device.data = {'LED': 'ON'}
            led.write(1)
            print("LED is ON!")
            self._device.save()
        else:
            if (notification.notification[4:7] == 'OFF'):
                self._device.data = {'LED': 'OFF'}
                led.write(0)
                print("LED is OFF")
                self._device.save()


url = 'https://playground.devicehive.com/api/rest'
refresh_token = 'eyJhbGciOiJIUzI1NiJ9.eyJwYXlsb2FkIjp7ImEiOlsyLDMsNCw1LDYsNyw4LDksMTAsMTEsMTIsMTUsMTYsMTddLCJlIjoxNTU4MDMyMjExMzE3LCJ0IjowLCJ1IjozNTA5LCJuIjpbIjM0NjYiXSwiZHQiOlsiKiJdfX0.UmmgbuogE8DWNnHppUIUxH7t6BRzfoHd8v93BMcSTUY'
dh = DeviceHive(ReceiverHandler)
dh.connect(url, refresh_token=refresh_token)
