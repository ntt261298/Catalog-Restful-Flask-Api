import unittest

from main import app, db
from main.models.category import CategoryModel
from config import app_config
import main.controllers


class CategoriesApiTests(unittest.TestCase):
    category_name = 'Category 1'

    # Executed prior to each tests
    def setUp(self):
        with app.app_context():
            app.config.from_object(app_config['testing'])
            self.app = app.test_client()
            db.drop_all()
            db.create_all()
            self.create_categories()
            self.assertEqual(app.debug, False)

    # Executed after each tests
    def tearDown(self):
        with app.app_context():
            db.session.remove()

    # Helper methods
    def create_categories(self):
        # Create a new category
        new_category = CategoryModel(self.category_name)
        db.session.add(new_category)
        db.session.commit()
        return

    # Test
    def test_catalog_api_get_all_categories(self):
        response = self.app.get('/categories')

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
