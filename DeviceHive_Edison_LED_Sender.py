from devicehive import Handler
from devicehive import DeviceHive
from devicehive import DeviceHiveApi


class SenderHandler(Handler):

    def __init__(self, api, device_id,
                 accept_command_name,
                 num_notifications=1):
        Handler.__init__(self, api)
        self._device_id = device_id
        self._accept_command_name = accept_command_name
        self._num_notifications = num_notifications
        self._device = None

    def _send_notifications(self):
        for num_notification in range(self._num_notifications):
            notification = self._accept_command_name
            self._device.send_notification(notification)
            print('Sending notification "%s"' % notification)
        self.api.disconnect()

    def handle_connect(self):
        self._device = self.api.get_device(self._device_id)
        self._device.send_command(self._accept_command_name)
        print('Sending command "%s"' % self._accept_command_name)
        self._device.subscribe_update_commands([self._accept_command_name])

    def handle_command_update(self, command):
        if command.status == 'accepted':
            print('Command "%s" accepted' % self._accept_command_name)
            self._send_notifications()


url = 'https://playground.devicehive.com/api/rest'
refresh_token = 'eyJhbGciOiJIUzI1NiJ9.eyJwYXlsb2FkIjp7ImEiOlsyLDMsNCw1LDYsNyw4LDksMTAsMTEsMTIsMTUsMTYsMTddLCJlIjoxNTU4MDMyMjExMzE3LCJ0IjowLCJ1IjozNTA5LCJuIjpbIjM0NjYiXSwiZHQiOlsiKiJdfX0.UmmgbuogE8DWNnHppUIUxH7t6BRzfoHd8v93BMcSTUY'
while (True):
    message = input()
    dh = DeviceHive(SenderHandler, device_id="myPC-1", accept_command_name=message)
    dh.connect(url, refresh_token=refresh_token)
