from testnado.browser_session import wrap_browser_session

from tests.helpers import HandlerTestCase


class TestIndex(HandlerTestCase):

    @wrap_browser_session()
    def test_index_authorized(self, driver):
        driver.get("/")
        categories = driver.find_elements_by_css_selector(".category")
        self.assertEqual(24, len(categories))
