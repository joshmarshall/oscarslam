import json

from tornado.websocket import WebSocketHandler


class EventsHandler(WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self, contest_id):
        self.application.settings["queue"].add_subscriber(self.on_events)

    def on_events(self, messages):
        if len(messages):
            message = messages[-1]
            self.write_message(json.dumps(message))
