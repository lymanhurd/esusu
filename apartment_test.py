import unittest

from apartment_service import ApartmentService
from esusu_db import create_apartment_db


class ApartmentServiceTest(unittest.TestCase):

    def setUp(self):
        self.db_path = ":memory:"
        self.conn = create_apartment_db(self.db_path)
        self.apartment_service = ApartmentService(self.conn)

    def test_add_apartment(self):
        expected = {"Property_ID": 2, "Unit": 3}
        apartment_id = self.apartment_service.add_apartment(expected)
        expected["Apartment_ID"] = apartment_id
        actual = self.apartment_service.get_apartment(apartment_id)
        self.assertDictEqual(expected, actual)

    def test_add_property(self):
        expected = {"Manager_ID": 1, "Name": "Fawlty Towers", "Address": "Antarctica"}
        property_id = self.apartment_service.add_property(expected)
        expected["Property_ID"] = property_id
        actual = self.apartment_service.get_property(property_id)
        self.assertDictEqual(expected, actual)

    def test_add_tenant(self):
        expected = {"Apartment_ID": 1, "Name": "Basil", "DateOfBirth": "1970-01-01", "EncryptedSSN": "xyzzy",
                    "IsPrimary": 1}
        tenant_id = self.apartment_service.add_tenant(expected)
        expected["Tenant_ID"] = tenant_id
        actual = self.apartment_service.get_tenant(tenant_id)
        self.assertDictEqual(expected, actual)

    def test_update_apartment(self):
        original = {"Property_ID": 2, "Unit": 3}
        apartment_id = self.apartment_service.add_apartment(original)
        updated = {"Apartment_ID": apartment_id, "Property_ID": 3, "Unit": 5}
        self.apartment_service.update_apartment(updated)
        actual = self.apartment_service.get_apartment(apartment_id)
        self.assertDictEqual(updated, actual)

    def test_update_property(self):
        original = {"Manager_ID": 1, "Name": "Fawlty Towers", "Address": "Antarctica"}
        property_id = self.apartment_service.add_property(original)
        updated = {"Property_ID": property_id, "Manager_ID": 2, "Name": "Empire State Building", "Address": "Manhattan"}
        self.apartment_service.update_property(updated)
        actual = self.apartment_service.get_property(property_id)
        self.assertDictEqual(updated, actual)

    def test_update_tenant(self):
        original = {"Apartment_ID": 1, "Name": "Basil", "DateOfBirth": "1970-01-01", "EncryptedSSN": "xyzzy",
                    "IsPrimary": 1}
        tenant_id = self.apartment_service.add_tenant(original)
        updated = {"Apartment_ID": 2, "Tenant_ID": tenant_id, "Name": "Felicity", "DateOfBirth": "1990-06-06",
                   "EncryptedSSN": "xxxyyyzzz", "IsPrimary": 0}
        self.apartment_service.update_tenant(updated)
        actual = self.apartment_service.get_tenant(tenant_id)
        self.assertDictEqual(updated, actual)


if __name__ == '__main__':
    unittest.main()
