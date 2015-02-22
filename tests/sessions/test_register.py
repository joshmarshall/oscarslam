from testnado.browser_session import wrap_browser_session

from oscarslam import config
from oscarslam.models.user import User

from tests.helpers import HandlerTestCase


class TestRegister(HandlerTestCase):

    @wrap_browser_session(discover_credentials=False)
    def test_index(self, driver):
        driver.get("/")
        driver.find_element_by_id("register-name").send_keys("Foo Bar")
        driver.find_element_by_id("register-email").send_keys(
            "foobar@email.com")
        driver.find_element_by_id("register-password").send_keys("foobar")
        driver.find_element_by_id("register-submit").click()
        user = User.use(self.store).store.fetch("foobar@email.com")
        self.assertIsNotNone(user, "New user should be in database.")
        self.assertEqual("foobar@email.com", user.email)
        self.assertEqual("Foo Bar", user.name)
        self.assertTrue(user.authenticate("foobar"))
        # should ultimately land on homepage
        self.assertTrue(driver.current_url.endswith(
            "/contests/{0}".format(config.CONTEST_ID)))
