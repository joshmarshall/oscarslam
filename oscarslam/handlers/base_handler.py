from tornado.web import RequestHandler
from oscarslam.models.user import User, Token


class BaseHandler(RequestHandler):

    def prepare(self):
        self.message = self.get_argument("message", None)

    def get_current_user(self):
        token_value = self.get_secure_cookie("token")
        if not token_value:
            return None

        token = self.store.fetch(Token, token_value)
        if not token:
            return None

        user = self.store.fetch(User, token.email)
        if not user:
            return None

        return user

    @property
    def store(self):
        return self.application.settings["store"]

    def render(self, *args, **kwargs):
        kwargs.setdefault("message", self.message)
        kwargs.setdefault("_m", self._render_message)
        kwargs.setdefault("_k", self._render_message_class)
        return super(BaseHandler, self).render(*args, **kwargs)

    def _render_message(self, message):
        message = self._get_message(message)["text"]
        for key, func in _REPLACEMENTS.items():
            if key in message:
                message = message.replace(key, func(self))
        return message

    def _render_message_class(self, message):
        message_class = self._get_message(message)["class"]
        return message_class

    def _get_message(self, message):
        return self.application.settings["messages"].get(
            message, {"text": "", "class": ""})


_REPLACEMENTS = {
    "$USER": lambda h: getattr(h.current_user, "name", "")
}
