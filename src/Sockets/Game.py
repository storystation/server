import json
from json import JSONDecodeError

from geventwebsocket import WebSocketApplication


class GameSocketHandler(WebSocketApplication):

    def on_open(self):
        print("Client connected")

    def on_message(self, message, **kwargs):
        if message is None:
            return

        try:
            message = json.loads(message)
            if message['type'] == 'init_module':
                self.init_module(message)
            elif message['type'] == 'end_module':
                self.end_module(message)
            elif message['type'] == 'timeout':
                self.send_timeout(message)
            elif message['type'] == 'is_ready':
                self.poll_ready(message)
            elif message['type'] == 'echo':
                self.ws.send(json.dumps(message))

        except KeyError as e:
            print("You must provide a key: %s" % e)
        except JSONDecodeError as e:
            print('An error occurred when decoding json. Please provide a valid json string.')

    def send_timeout(self, message):
        if 'sender' in message and message['sender'] == 'site':
            self.broadcast({
                'target': 'board',
                'type': 'timeout'
            })

    def poll_ready(self, message):
        target = ''
        if message['sender'] == 'site':
            target = 'board'
        elif message['sender'] == 'board':
            target = 'site'
        self.broadcast({
            'target': target,
            'type': 'is_ready',
            'message': message['message']
        })

    def init_module(self, message):
        if message['sender'] == 'site':
            response = {
                'target': 'board',
                'module': message['module']
            }
            self.broadcast(response)

    def end_module(self, message):
        if message['sender'] == 'board':
            response = {
                'target': 'site',
                'type': message['type'],
                'message': message['message']
            }
            self.broadcast(message)

    def send_client_list(self, message):
        current_client = self.ws.handler.active_client
        current_client.nickname = message['nickname']

        self.ws.send(json.dumps({
            'msg_type': 'update_clients',
            'clients': [
                getattr(client, 'nickname', 'anonymous')
                for client in self.ws.handler.server.clients.values()
            ]
        }))

    def broadcast(self, message: dict):
        """
        Broadcast the message as json string to every connected clients

        :param message: The message that will be parsed and sent
        """
        for client in self.ws.handler.server.clients.values():
            client.ws.send(json.dumps(message))

    def on_close(self, reason):
        print("Someone has left the game")
