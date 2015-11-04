import sys
from socketIO_client import SocketIO, LoggingNamespace

__author__ = 'javier'
def main(argv):
    def on_bbb_response(*args):
        print('on_bbb_response', args)

    with SocketIO('localhost', 3000, LoggingNamespace) as socketIO:
        socketIO.emit('chat message', {'xxx': 'yyy'}, on_bbb_response)
        socketIO.wait_for_callbacks(seconds=1)


if __name__ == '__main__':
    main(sys.argv)
