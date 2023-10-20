from model.admin_model import AdminModel
from tests.integration.integration_base_test import IntegrationBaseTest


class AdminTest(IntegrationBaseTest):
    def test_crud_user(self):
        with self.app_context():
            admin = AdminModel("test@test.com", "1234")
            self.assertIsNotNone(admin.admin_exist(admin.email))

            admin.save_to_db()
            self.assertIsNotNone(admin.find_by_email(admin.email))




