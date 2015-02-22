from testnado.browser_session import wrap_browser_session

from tests.helpers import HandlerTestCase


class TestResetPassword(HandlerTestCase):

    @wrap_browser_session(discover_credentials=False)
    def test_index_password_reset(self, driver):
        driver.get("/")
        checkbox = driver.find_element_by_id("signin-reset")
        checkbox.click()
        form = driver.find_element_by_id("signin-form")
        self.assertTrue(
            form.get_attribute("action").endswith("/reset_password"))
        button = driver.find_element_by_id("signin-submit")
        self.assertEqual("Reset Password", button.get_attribute("value"))
        password_input = driver.find_element_by_id("signin-password")
        self.assertFalse(password_input.is_displayed())

        checkbox.click()
        # make sure it goes back
        self.assertTrue(form.get_attribute("action").endswith("/signin"))
        self.assertEqual("Sign In", button.get_attribute("value"))
        self.assertTrue(password_input.is_displayed())

    @wrap_browser_session(discover_credentials=False)
    def test_index_password_reset_no_user(self, driver):
        driver.get("/")
        driver.find_element_by_id("signin-reset")
        driver.find_element_by_id("signin-submit").click()

        self.assertTrue(driver.current_url.endswith("/?message=unknown_user"))

    @wrap_browser_session(discover_credentials=False)
    def test_reset_password_sends_email(self, driver):
        self._mailgun_handler = lambda x: x.finish({})

        driver.get("/")
        driver.find_element_by_id("signin-email").send_keys(self.user.email)
        driver.find_element_by_id("signin-reset").click()
        driver.find_element_by_id("signin-submit").click()

        self.assertTrue(driver.current_url.endswith("/?message=reset_sent"))

    @wrap_browser_session(discover_credentials=False)
    def test_reset_password_form(self, driver):
        base_url = "http://localhost:{0}/reset_password".format(
            self.get_http_port())
        signed_url = self.user.generate_reset_password_url(base_url)
        signed_path = signed_url.split(str(self.get_http_port()))[1]
        driver.get(signed_path)

        driver.find_element_by_id("reset-password").send_keys("SECRET")
        driver.find_element_by_id("reset-submit").click()

        self.assertTrue(
            driver.current_url.endswith("/?message=password_reset"))
