from testnado.browser_session import wrap_browser_session

from tests.helpers import HandlerTestCase


class TestSignin(HandlerTestCase):

    @wrap_browser_session(discover_credentials=False)
    def test_index(self, driver):
        driver.get("/")
        driver.find_element_by_id("signin-email").send_keys("foo@bar.com")
        driver.find_element_by_id("signin-password").send_keys("foobar")
        driver.find_element_by_id("signin-submit").click()

        # should ultimately land on homepage
        self.assertTrue(driver.current_url.endswith("/?message=welcome"))
