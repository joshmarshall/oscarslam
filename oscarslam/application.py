import os
from tornado.web import Application as TornadoApplication

from oscarslam import config
from oscarslam.messages import MESSAGES
import oscarslam.handlers.admin_handler
import oscarslam.handlers.leaders_handler
import oscarslam.handlers.logout_handler
import oscarslam.handlers.index_handler
import oscarslam.handlers.register_handler
import oscarslam.handlers.signin_handler
import oscarslam.handlers.vote_handler


ROUTES = [
    ("/", oscarslam.handlers.index_handler.IndexHandler),
    ("/admin", oscarslam.handlers.admin_handler.AdminHandler),
    ("/register", oscarslam.handlers.register_handler.RegisterHandler),
    ("/signin", oscarslam.handlers.signin_handler.SigninHandler),
    ("/leaders", oscarslam.handlers.leaders_handler.LeadersHandler),
    ("/logout", oscarslam.handlers.logout_handler.LogoutHandler),
    ("/vote", oscarslam.handlers.vote_handler.VoteHandler),
    ("/vote/([\w\-]+)", oscarslam.handlers.vote_handler.VoteIdHandler),
]


BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Application(TornadoApplication):

    def __init__(self, store):
        cookie_secret = config.COOKIE_SECRET
        view_path = os.path.join(BASE_DIR, "views")
        static_path = os.path.join(BASE_DIR, "static")
        super(Application, self).__init__(
            ROUTES, template_path=view_path, static_path=static_path,
            cookie_secret=cookie_secret, store=store, messages=MESSAGES,
            login_url="/?message=login_required", debug=config.DEBUG)
