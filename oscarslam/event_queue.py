import time


class EventQueue(object):

    def __init__(self, rax_queue, ioloop):
        self.rax_queue = rax_queue
        self.ioloop = ioloop
        self.subscribers = []
        self.interval = 5
        self.last_time = time.time()
        self.ioloop.add_callback(self.fetch)

    def reconnect(self):
        self.ioloop.add_timeout(time.time() + 30, self.on_reconnect)

    def on_reconnect(self):
        future = self.rax_queue.connect()
        future.add_done_callback(self.on_connected)

    def on_connected(self, result):
        result = result.result()
        if result["status"] != "success":
            print("Could not connect to RAX: {}".format(result))
            return self.reconnect()
        self.ioloop.add_callback(self.fetch)

    def fetch(self):
        future = self.rax_queue.fetch_messages()
        future.add_done_callback(self.on_messages)

    def on_messages(self, result):
        result = result.result()
        if result["status"] != "success":
            if result["code"] in [401, 403]:
                print("Auth issue -- trying to connect again in 15 secs.")
                return self.reconnect()
            else:
                print("Issue requesting messages: {}".format(result))
                return self.ioloop.add_timeout(time.time() + 30, self.fetch)

        messages = result["messages"]

        for subscriber in self.subscribers[:]:
            try:
                subscriber(messages)
            except Exception:
                # this is overly protective, fix later...
                self.subscribers.remove(subscriber)

        self.ioloop.add_timeout(time.time() + self.interval, self.fetch)

    def add_subscriber(self, func):
        self.subscribers.append(func)

    def push(self, message):
        future = self.rax_queue.push_message(message, 60)
        future.add_done_callback(self.on_push)

    def on_push(self, result):
        result = result.result()
        if result["status"] != "success":
            print("Error sending message: {}".format(result))
