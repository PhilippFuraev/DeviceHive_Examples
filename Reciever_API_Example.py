from devicehive import Handler
from devicehive import DeviceHive


class ReceiverHandler(Handler):

    def __init__(self, api, device_id='myPC-1',
                 accept_command_names=['Turn on TV', 'Turn off TV']):
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
        if notification.notification[5:7] == 'on':
            self._device.data = {'TV': 'ON'}
            print("Your very smart TV turned ON!")
            self._device.save()
        else:
            if (notification.notification[5:8] == 'off'):
                self._device.data = {'TV': 'OFF'}
                print("Your very smart TV turned OFF")
                self._device.save()


url = 'ws://playground.devicehive.com/api/websocket'
refresh_token = 'your refresh token'
dh = DeviceHive(ReceiverHandler)
dh.connect(url, refresh_token=refresh_token)
