import sys
from socketIO_client import SocketIO, LoggingNamespace
import time

__author__ = 'javier'
class messenger:
    socketIO = None

    def __init__(self, host, port):
        self.socketIO = SocketIO(host, port, LoggingNamespace)

    def subscribe(self, channel_name):
        self.socketIO.emit(
            'request',
            {
                'action': 'subscribe',
                'channel': channel_name
            },
            self.on_request_response
        )
        self.socketIO.wait_for_callbacks()

    def on_request_response(self, *args):
        print('on_bbb_response', args)

def main(argv):
    m = messenger("localhost", 3000)
    m.subscribe("TestChannel")
    while True:
        time.sleep(10)

if __name__ == '__main__':
    main(sys.argv)
