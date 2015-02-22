import os
from tornado.web import Application as TornadoApplication, RedirectHandler

from oscarslam import config
from oscarslam.messages import MESSAGES
from oscarslam.handlers.admin_handler import AdminHandler
from oscarslam.handlers.contest_handler import ContestHandler
from oscarslam.handlers.events_handler import EventsHandler
from oscarslam.handlers.leaders_handler import LeadersHandler
from oscarslam.handlers.logout_handler import LogoutHandler
from oscarslam.handlers.index_handler import IndexHandler
from oscarslam.handlers.register_handler import RegisterHandler
from oscarslam.handlers.reset_password_handler import ResetPasswordHandler
from oscarslam.handlers.signin_handler import SigninHandler
from oscarslam.handlers.vote_handler import VoteHandler, VoteRedirectHandler


ROUTES = [
    ("/", IndexHandler),
    ("/contests", RedirectHandler, {
        "url": "/contests/{0}".format(config.CONTEST_ID),
        "permanent": False
    }),
    ("/contests/([\w\-]+)", ContestHandler),
    ("/contests/([\w\-]+)/events", EventsHandler),
    ("/contests/([\w\-]+)/leaders", LeadersHandler),
    ("/contests/([\w\-]+)/votes", VoteRedirectHandler),
    ("/contests/([\w\-]+)/votes/([\w\-]+)", VoteHandler),
    ("/admin", RedirectHandler, {
        "url": "/admin/{0}".format(config.CONTEST_ID),
        "permanent": False
    }),
    ("/admin/([\w\-]+)", AdminHandler),
    ("/register", RegisterHandler),
    ("/reset_password", ResetPasswordHandler),
    ("/signin", SigninHandler),
    ("/logout", LogoutHandler),
]


BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Application(TornadoApplication):

    def __init__(self, store, mailgun, queue):
        cookie_secret = config.COOKIE_SECRET
        view_path = os.path.join(BASE_DIR, "views")
        static_path = os.path.join(BASE_DIR, "static")
        super(Application, self).__init__(
            ROUTES, template_path=view_path, static_path=static_path,
            cookie_secret=cookie_secret, store=store, messages=MESSAGES,
            login_url="/?message=login_required", mailgun=mailgun,
            debug=config.DEBUG, queue=queue)
