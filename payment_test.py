import random
import unittest
from datetime import date, timedelta

from payment_service import PaymentService
from esusu_db import create_payment_db


class PaymentServiceTest(unittest.TestCase):

    def setUp(self):
        self.db_path = ":memory:"
        self.conn = create_payment_db(self.db_path)
        self.payment_service = PaymentService(self.conn)

    def test_add_payment(self):
        expected_tenant_id = 2
        expected_amount = 123456
        expected_date = date.fromisoformat("2012-02-29")
        expected_payment_id = self.payment_service.add_payment(expected_tenant_id, expected_amount/100,
                                                               expected_date.isoformat())
        actual = self.payment_service.get_payment(expected_payment_id)
        self.assertEqual(6, len(actual))
        self.assertEqual(expected_payment_id, actual["Payment_ID"])
        self.assertEqual(expected_tenant_id, actual["Tenant_ID"])
        self.assertEqual(expected_amount, actual["Amount"])
        self.assertEqual(expected_date.year, actual["Year"])
        self.assertEqual(expected_date.month, actual["Month"])
        self.assertEqual(expected_date.day, actual["Day"])

    def test_add_payment_bad_amount(self):
        with self.assertRaises(ValueError):
            self.payment_service.add_payment(1, 0, "1999-12-31")
        with self.assertRaises(ValueError):
            self.payment_service.add_payment(1, -1000, "1999-12-31")

    def test_add_payment_bad_date(self):
        tomorrow = date.today() + timedelta(days=1)
        with self.assertRaises(ValueError):
            self.payment_service.add_payment(1, 1000, tomorrow.isoformat())
        with self.assertRaises(ValueError):
            self.payment_service.add_payment(1, 1000, "not-a-valid-date")

    def test_get_payment_history(self):
        payment_list = [
            (1, 100.25, "2001-03-15"),  # tenant 1
            (1, 200.33, "2002-12-25"),
            (1, 300.17, "2007-01-01"),
            (2, 100.01, "1985-04-03"),  # tenant 2
            (2, 25.55, "1985-04-29"),
            (2, 300.11, "2010-07-18"),
            (2, 75.99, "2010-07-18")
        ]
        random.shuffle(payment_list)  # make sure order of insertion is irrelevant
        for p in payment_list:
            self.payment_service.add_payment(*p)

        # tenant 1 has no partial payments
        payment1 = self.payment_service.get_payment_history(1)
        self.assertEqual([(100.25, '2001-03-15'), (200.33, '2002-12-25'), (300.17, '2007-01-01')], payment1)

        # tenant 2 has partial payments
        payment2 = self.payment_service.get_payment_history(2)
        self.assertEqual([(125.56, '1985-04-03'), (376.10, '2010-07-18')], payment2)

        # tenant 3 has no payments
        payment3 = self.payment_service.get_payment_history(3)
        self.assertEqual(0, len(payment3))


if __name__ == '__main__':
    unittest.main()
