import sys
import threading
from socketIO_client import SocketIO, BaseNamespace
import time

__author__ = 'javier'

class RTMessenger:
    def __init__(self, host, port, callback=None):
        self.on_connect_callback = callback
        self.subscribed_callbacks = {}
        self.message_callbacks = {}
        self.presence_callbacks={}
        self.socketIO = SocketIO(host, port)
        self.socketIO.on('connect', self.on_connect)
        self.socketIO.on('subscribed', self.on_subscribed)
        waiter = threading.Thread(target=self.waiter)
        waiter.daemon = True
        waiter.start()

    def on_message(self, message):
        channel = message['channel']
        if message['presence']:
            callback = self.presence_callbacks[channel]
            if callback is not None:
                callback(channel, message['message'])
        else:
            callback = self.message_callbacks[channel]
            if callback is not None:
                callback(channel, message['message'])

    def on_connect(self):
        if self.on_connect_callback is not None:
            self.on_connect_callback()

    def on_subscribed(self, message):
        channel = message['channel']
        callback = self.subscribed_callbacks[channel]
        if callback is not None:
            callback(channel)

    def waiter(self):
        self.socketIO.wait()

    def subscribe(self, channel, message_callback,presence_callback=None, callback=None):
        self.socketIO.emit(
            'request',
            {
                'action': 'subscribe',
                'channel': channel
            }
        )
        self.subscribed_callbacks[channel] = callback
        self.message_callbacks[channel] = message_callback
        self.presence_callbacks[channel] = presence_callback
        self.socketIO.on(channel, self.on_message)

    def publish(self, channel, message):
        self.socketIO.emit(
            'request',
            {
                'action': 'message',
                'channel': channel,
                'message': message
            }
        )


def on_connect():
    print("Connected!")

def on_subscribe(channel):
    print("Subscribed to channel: "+channel)

def on_message(channel, message):
    print("Message received on channel "+channel+": "+str(message))

def on_presence(channel, message):
    print("Presence received on channel " + channel + ": " + str(message))

def main(argv):
    m = RTMessenger("rtmessenger-env.elasticbeanstalk.com", 80, on_connect)
    # m = RTMessenger("localhost", 3000, on_connect)
    m.subscribe("TestChannel", on_message, presence_callback=on_presence, callback=on_subscribe)
    m.publish("TestChannel", {"say": "hello world"})
    while True:
        time.sleep(10)

if __name__ == '__main__':
    main(sys.argv)
