import json
import mock
import tempfile
import oscarslam.categories
import unittest
from tests import samples


class TestCategories(unittest.TestCase):

    def setUp(self):
        super(TestCategories, self).setUp()
        with tempfile.NamedTemporaryFile(suffix=".json") as temp_fp:
            temp_fp.write(json.dumps(samples.SIMPLE_DATA))
            temp_fp.flush()
            with mock.patch("oscarslam.config") as mock_config:
                mock_config.CATEGORIES_PATH = temp_fp.name
                reload(oscarslam.categories)

    def tearDown(self):
        super(TestCategories, self).tearDown()
        reload(oscarslam.categories)

    def test_categories(self):
        categories = oscarslam.categories.CATEGORIES
        self.assertEqual(1, len(categories))
        self.assertEqual("Best Picture", categories[0].title)

    def test_nominees(self):
        category = oscarslam.categories.CATEGORIES[0]
        self.assertEqual(1, len(category.nominees))
        self.assertEqual("Foo", category.nominees[0].title)
        nominees = category.nominees
        self.assertEqual(nominees.get("foo").key, nominees[0].key)
